import json
from pathlib import Path

import pytest

from modem_controller.catalog.storage import (
    NewerSchemaError,
    Settings,
    SettingsStore,
    StorageError,
    choose_settings_location,
)


def test_settings_round_trip_preserves_preferences_without_device_actions(
    tmp_path: Path,
) -> None:
    store = SettingsStore(tmp_path)
    settings = Settings(
        selected_profile="generic-at",
        selected_category="Network",
        connection={"port": "COM7", "baud_rate": "115200"},
        last_directories={"export": "C:/Reports"},
        favorites=("signal-quality",),
        profile_notes={"generic-at": "Adapter observed."},
    )

    store.save(settings)

    assert store.load() == type(store.load())(settings)


def test_missing_and_malformed_settings_recover_without_overwriting(
    tmp_path: Path,
) -> None:
    store = SettingsStore(tmp_path)

    assert not store.load().recovered
    store.path.write_text("not json", encoding="utf-8")

    result = store.load()

    assert result.recovered
    assert result.settings == Settings()
    assert store.path.read_text(encoding="utf-8") == "not json"


def test_newer_settings_schema_is_explicitly_rejected(tmp_path: Path) -> None:
    store = SettingsStore(tmp_path)
    store.path.write_text(json.dumps({"schema_version": 2}), encoding="utf-8")

    with pytest.raises(NewerSchemaError):
        store.load()


def test_sensitive_connection_values_are_not_persisted(tmp_path: Path) -> None:
    store = SettingsStore(tmp_path)

    with pytest.raises(StorageError, match="must not be persisted"):
        store.save(Settings(connection={"pin": "1234"}))


def test_explicit_portable_directory_or_user_fallback_is_selected(
    tmp_path: Path,
) -> None:
    portable = tmp_path / "portable"
    fallback = tmp_path / "user"

    location = choose_settings_location(
        tmp_path / "app", portable_directory=portable, user_directory=fallback
    )

    assert location.directory == portable
    assert location.portable
