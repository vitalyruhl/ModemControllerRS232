# Documentation index

- [Upgrade proposal](upgrade.md): agreed requirements, proposed behavior, technology
  tradeoffs, implementation order, and future acceptance criteria.
- [YAT evaluation template](../.Info/YAT/README.md): our MC/TC command pages and
  evaluation limits; the YAT application itself is not included.
- [Legacy project description](legacy/README.md): original application background.
- [AT command notes](Infos/AT-Befehle.txt) and
  [initialization strings](Infos/Init-Strings.md): historical reference material
  requiring model-specific review before reuse.
- [Modem reference collection](<Infos/Modem auch GSM/>): manuals, troubleshooting
  notes, and existing driver artifacts. These are reference files, not new
  application dependencies or instructions to install drivers.
- [Screenshots](images/): captures of the previous application.

## Scaffold responsibilities

All `.py` files are empty placeholders. The following describes intended ownership,
not implemented behavior or fixed public interfaces.

| Path under `src/modem_controller/` | Intended responsibility |
| --- | --- |
| `app.py` | Compose the application and connect the separate components. |
| `ui/main_window.py` | Main window layout and connection status. |
| `ui/terminal_view.py` | Text/hex presentation and input controls. |
| `ui/connection_panel.py` | Simple and advanced connection settings. |
| `ui/catalog_editor.py` | Command and profile editing interface. |
| `transport/serial_port.py` | Single-owner serial access, exact-byte I/O, and control lines. |
| `transport/capture.py` | Preserve raw sent/received data independently of display formatting. |
| `protocol/framing.py` | Incremental response framing and prompts without newline termination. |
| `protocol/at_session.py` | AT response state, deadlines, and unsolicited notifications. |
| `catalog/models.py` | GUI-independent command and profile data. |
| `catalog/storage.py` | Versioned catalog/profile persistence. |
| `catalog/legacy_import.py` | Previewable imports of the archived XML/VCE formats. |
| `workflows/connection_search.py` | Bounded, cancellable AT-only settings discovery. |
| `workflows/diagnostics.py` | Profile-aware diagnostic sequences and results. |

Package directories also contain empty `__init__.py` files. No executable entry
point or serial-port side effects are introduced by this scaffold.

## Reserved validation and tooling areas

- `tests/unit/`: future byte handling, framing, catalog, and workflow checks.
- `tests/integration/`: future simulated transport and component integration checks.
- `tests/fixtures/`: future synthetic or reviewed, sanitized response samples.
- `tools/`: future development and packaging utilities.

These directories contain only `.gitkeep` placeholders. No test suite exists yet;
an empty test directory must not be reported as passing application tests.
Real-device checks and Windows compatibility checks remain separate from unit
and simulator evidence.

## Migration map

| Previous location | Current location |
| --- | --- |
| `MC-Sourcecode/` | `.Old_Version/MC-Sourcecode/` |
| `ModemController_V1.0.1/` | `.Old_Version/ModemController_V1.0.1/` |
| `ModemController_V1.5.0.10/` | `.Old_Version/ModemController_V1.5.0.10/` |
| `ModemController_V1.5.0.10.7z` | `.Old_Version/ModemController_V1.5.0.10.7z` |
| `Infos/` | `docs/Infos/` |
| `Screenshot_2.jpg`, `Screenshot_3.jpg` | `docs/images/` |
| `README.md` | `docs/legacy/README.md`; new orientation README at the root |
| `upgrade.md` | `docs/upgrade.md` |

Git metadata, the license, shared agent configuration, and repository-wide
configuration remain at the root. Existing reference filenames and legacy source
contents are preserved; documentation links and current-path references are updated.
