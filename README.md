# ModemControllerRS232

A Windows modem terminal being prepared for a Python rewrite with PySide6 and
pySerial. The repository currently contains an **empty application scaffold**
and the preserved VB.NET application. The Python application is not runnable yet.

Read the [upgrade proposal](docs/upgrade.md) for the agreed requirements,
technology choices, connection search, terminal behavior, and validation plan.

## Repository layout

```text
.
|-- .Old_Version/            Preserved VB.NET sources and released applications
|-- docs/
|   |-- upgrade.md           Rewrite requirements and proposed implementation
|   |-- Infos/              Existing modem manuals, notes, and driver references
|   |-- images/             Legacy screenshots
|   `-- legacy/README.md     Original project description
|-- src/modem_controller/
|   |-- app.py              Future application composition
|   |-- ui/                 Desktop views and user interaction
|   |-- transport/          Serial-port access and byte capture
|   |-- protocol/           Response framing and AT session processing
|   |-- catalog/            Commands, profiles, persistence, and legacy import
|   `-- workflows/          Connection search and diagnostic sequences
|-- tests/                  Reserved unit and integration test directories
|-- tools/                  Reserved development and packaging utilities
`-- pyproject.toml          Initial Python package metadata
```

Every Python file is deliberately empty. Runtime dependencies, a Python version
baseline, executable entry points, GUI behavior, and hardware access have not been
implemented or validated. Version `0.0.0` is a scaffold marker, not a release.

The planned target is Windows 10 20H2 x64 and newer. Confirm and pin compatible
Python, Qt/PySide6, pySerial, and packaging versions before implementation.

## Existing application

The previous source tree and releases remain under [.Old_Version](.Old_Version/).
The original portable archive is
[ModemController_V1.5.0.10.7z](.Old_Version/ModemController_V1.5.0.10.7z).
See the [legacy description](docs/legacy/README.md) and
[documentation index](docs/README.md) for reference material.

Keep legacy sources and releases as migration references. Their runtime behavior
has not been retested after the directory move. Shortcuts containing absolute
paths may need local adjustment.

## Development boundaries

Keep GUI code separate from serial transport, protocol processing, catalog data,
and workflow orchestration. The [documentation index](docs/README.md) explains
the reserved modules and test areas.

Project-specific governance will be added separately. The supplied governance
example from another repository informed the separation of responsibilities only;
it has not been adopted as this repository's governance.

Only shared Serena and ProjectAtlas configuration is versioned. Their databases,
caches, local overrides, and generated machine-specific launcher files stay local.

## License

GNU General Public License v3.0. See [LICENSE](LICENSE).
