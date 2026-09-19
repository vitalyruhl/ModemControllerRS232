from importlib import import_module


def test_package_is_importable() -> None:
    module = import_module("modem_controller")

    assert module.__name__ == "modem_controller"
