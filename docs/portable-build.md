# Portable Windows Build

Build the folder bundle on Windows x64 with the locked project environment:

```powershell
uv sync --frozen
uv run python tools/build_portable.py
```

The recipe produces `dist/ModemController/` and `dist/ModemController.zip`.
Distribute the ZIP unchanged, then unpack it and start `ModemController.exe`.
The package embeds application resources such as the generic command catalog;
it does not embed reference installers, YAT binaries, archived customer material,
or local experiments.

Settings prefer a writable portable `data/` directory beside the application. If
that directory is unavailable, choose a writable per-user or user-selected location
in the application once the settings workflow is available.

## Pending acceptance evidence

The bundle recipe is automated, but clean-machine launch evidence remains pending:

- Windows 10 20H2 x64 without Python.
- Windows 11 x64.
- Folder relocation and a read-only installation directory.
- Startup with no serial device attached.

These are packaging checks only. They do not verify modem compatibility.