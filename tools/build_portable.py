"""Build a portable Windows bundle without embedding local reference material."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DIST_DIRECTORY = PROJECT_ROOT / "dist"
BUILD_DIRECTORY = PROJECT_ROOT / "build" / "pyinstaller"
BUNDLE_NAME = "ModemController"


def build_command() -> list[str]:
    return [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onedir",
        "--windowed",
        "--name",
        BUNDLE_NAME,
        "--collect-data",
        "modem_controller",
        "--distpath",
        str(DIST_DIRECTORY),
        "--workpath",
        str(BUILD_DIRECTORY),
        "--specpath",
        str(BUILD_DIRECTORY),
        str(PROJECT_ROOT / "src" / "modem_controller" / "app.py"),
    ]


def build() -> Path:
    subprocess.run(build_command(), check=True, cwd=PROJECT_ROOT)
    archive = shutil.make_archive(
        str(DIST_DIRECTORY / BUNDLE_NAME), "zip", DIST_DIRECTORY, BUNDLE_NAME
    )
    return Path(archive)


if __name__ == "__main__":
    print(build())
