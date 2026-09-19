"""Atomic persistence for user settings and catalog overlays."""

from __future__ import annotations

import json
import os
import tempfile
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

SETTINGS_SCHEMA_VERSION = 1
_SENSITIVE_KEYS = {"pin", "puk", "password", "secret"}


class StorageError(RuntimeError):
    """Base class for persistence failures that the UI can present to a user."""


class NewerSchemaError(StorageError):
    """Raised when data comes from an application version newer than this one."""


@dataclass(frozen=True, slots=True)
class Settings:
    selected_profile: str = "generic-at"
    selected_category: str = "Status"
    connection: dict[str, str] = field(default_factory=dict)
    last_directories: dict[str, str] = field(default_factory=dict)
    favorites: tuple[str, ...] = ()
    profile_notes: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {"schema_version": SETTINGS_SCHEMA_VERSION, **asdict(self)}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Settings:
        version = data.get("schema_version")
        if not isinstance(version, int):
            raise StorageError("settings schema_version is missing")
        if version > SETTINGS_SCHEMA_VERSION:
            raise NewerSchemaError("settings were created by a newer application")
        if version != SETTINGS_SCHEMA_VERSION:
            raise StorageError(f"unsupported settings schema version {version}")
        connection = _string_mapping(data, "connection")
        _reject_sensitive_values(connection)
        return cls(
            selected_profile=_string(data, "selected_profile", "generic-at"),
            selected_category=_string(data, "selected_category", "Status"),
            connection=connection,
            last_directories=_string_mapping(data, "last_directories"),
            favorites=tuple(_string_list(data, "favorites")),
            profile_notes=_string_mapping(data, "profile_notes"),
        )


@dataclass(frozen=True, slots=True)
class LoadResult:
    settings: Settings
    recovered: bool = False
    message: str = ""


@dataclass(frozen=True, slots=True)
class SettingsLocation:
    directory: Path
    portable: bool
    fallback_message: str = ""


class SettingsStore:
    """Reads and atomically writes settings without causing device-side effects."""

    def __init__(self, directory: Path, filename: str = "settings.json") -> None:
        self.directory = directory
        self.path = directory / filename

    def load(self) -> LoadResult:
        if not self.path.exists():
            return LoadResult(Settings())
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                raise StorageError("settings root must be an object")
            return LoadResult(Settings.from_dict(data))
        except NewerSchemaError:
            raise
        except (OSError, json.JSONDecodeError, StorageError) as error:
            return LoadResult(Settings(), recovered=True, message=str(error))

    def save(self, settings: Settings) -> None:
        self.directory.mkdir(parents=True, exist_ok=True)
        _reject_sensitive_values(settings.connection)
        payload = json.dumps(settings.to_dict(), indent=2, sort_keys=True) + "\n"
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{self.path.name}.", suffix=".tmp", dir=self.directory, text=True
        )
        temporary_path = Path(temporary_name)
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary_path, self.path)
        except OSError as error:
            raise StorageError(f"could not save settings: {error}") from error
        finally:
            temporary_path.unlink(missing_ok=True)

    def save_raw(self, payload: str) -> None:
        self.directory.mkdir(parents=True, exist_ok=True)
        temporary_path = self.path.with_suffix(self.path.suffix + ".tmp")
        try:
            temporary_path.write_text(payload, encoding="utf-8", newline="\n")
            os.replace(temporary_path, self.path)
        except OSError as error:
            raise StorageError(f"could not export catalog: {error}") from error
        finally:
            temporary_path.unlink(missing_ok=True)


def choose_settings_location(
    application_directory: Path,
    *,
    portable_directory: Path | None = None,
    user_directory: Path,
) -> SettingsLocation:
    """Prefer an explicit writable portable path, otherwise use a visible fallback."""

    candidate = portable_directory or application_directory / "data"
    try:
        candidate.mkdir(parents=True, exist_ok=True)
        probe = candidate / ".write-probe"
        probe.write_text("", encoding="utf-8")
        probe.unlink()
        return SettingsLocation(candidate, portable=True)
    except OSError:
        user_directory.mkdir(parents=True, exist_ok=True)
        return SettingsLocation(
            user_directory,
            portable=False,
            fallback_message=(
                "Portable settings are unavailable; using the selected user directory."
            ),
        )


def export_catalog_json(catalog: Any, destination: Path) -> None:
    """Export a validated native catalog object with atomic replacement."""

    SettingsStore(destination.parent, destination.name).save_raw(catalog.to_json())


def _string(data: dict[str, Any], key: str, default: str) -> str:
    value = data.get(key, default)
    if not isinstance(value, str):
        raise StorageError(f"{key} must be text")
    return value


def _string_mapping(data: dict[str, Any], key: str) -> dict[str, str]:
    value = data.get(key, {})
    if not isinstance(value, dict) or not all(
        isinstance(name, str) and isinstance(item, str) for name, item in value.items()
    ):
        raise StorageError(f"{key} must be a string mapping")
    return dict(value)


def _string_list(data: dict[str, Any], key: str) -> list[str]:
    value = data.get(key, [])
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise StorageError(f"{key} must be a string list")
    return value


def _reject_sensitive_values(values: dict[str, str]) -> None:
    if _SENSITIVE_KEYS & {key.casefold() for key in values}:
        raise StorageError("PIN, PUK, and passwords must not be persisted")
