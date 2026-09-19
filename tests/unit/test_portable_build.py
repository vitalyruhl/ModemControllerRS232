import importlib.util
from pathlib import Path

SCRIPT_PATH = Path(__file__).parents[2] / "tools" / "build_portable.py"
SPEC = importlib.util.spec_from_file_location("build_portable", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
build_portable = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(build_portable)


def test_portable_build_uses_onedir_and_collects_application_data() -> None:
    command = build_portable.build_command()

    assert command[:3] == [command[0], "-m", "PyInstaller"]
    assert "--onedir" in command
    assert "--windowed" in command
    assert "--collect-data" in command
    assert command[command.index("--collect-data") + 1] == "modem_controller"
    assert command[command.index("--name") + 1] == build_portable.BUNDLE_NAME
    assert (
        Path(command[-1])
        == build_portable.PROJECT_ROOT / "src" / "modem_controller" / "app.py"
    )
