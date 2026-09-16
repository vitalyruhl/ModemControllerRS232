# Modem Controller upgrade proposal

Status: agreed direction and requirements; empty Python scaffold created, with no
application behavior implemented.
Discussion date: 2026-09-16.
Preparation branch: `docs/python-modem-upgrade-plan`.

## Purpose and scope

Replace the existing VB.NET Windows Forms utility with a maintainable desktop
application developed in VS Code. Preserve the large terminal text area, free AT
command entry, clickable command help, modem presets, and portable distribution.
Add the serial inspection and recovery functions that currently require HTerm,
without exposing all expert controls during ordinary use.

This document records the discussion for a later implementation session. This
preparation now includes documentation, agent configuration, an empty Python
package scaffold, and relocation of the legacy project. It does not implement
application behavior, access a serial port, or change a modem. See
[the documentation index](README.md) for the current layout and migration map.

## Agreed constraints

- Target Windows 10 20H2 and newer Windows systems, including Windows 11.
- Windows x64 is sufficient. A 32-bit build is optional, not an acceptance gate.
  Windows on ARM and Windows versions older than the stated baseline are not
  currently promised targets.
- Develop, debug, and maintain the application in VS Code.
- Do not continue with VB or select PowerShell for the GUI. C# is outside the
  user's preferred scope, although C# itself does not require Visual Studio.
- Preserve a practical, simple desktop interface and a prominent terminal.
- Prioritize MC93, the user-described TC55i, and similar current cellular modems.
  Stollmann ISDN devices are no longer in active use; retain their presets as
  importable legacy data rather than prioritizing new functionality for them.
- Keep runtime use offline and portable: unpack a ZIP and launch the executable.
  The target machine should not need a separate Python installation.
- Repository code, comments, and documentation are written in English. Plan for
  German user-facing labels and help; confirm localization scope before building.

## Recommended technology

Use **Python, PySide6/Qt Widgets, and pySerial**, developed in VS Code.

- Python keeps the command catalog, response processing, and diagnostic workflows
  relatively easy to extend. Serial throughput does not justify C++ on its own.
- PySide6 provides Qt's official Python bindings and suitable desktop controls:
  a plain-text terminal, lists/trees, tables, split panes, and editing dialogs.
- pySerial provides byte-oriented serial access, timeouts, flow control, and
  modem control/status signals where the adapter and driver support them.
- Start with a PyInstaller folder bundle containing the executable and runtime
  dependencies, distributed as a ZIP. Consider a single-file executable only
  later; it extracts dependencies at startup and is harder to troubleshoot.
- Use a versioned JSON format for command catalogs and profiles. No database is
  necessary for the initial product scope.

Alternatives considered:

| Approach | Assessment |
| --- | --- |
| Python + Tkinter | Adequate for a smaller terminal; Qt is preferred for richer editors and diagnostic views. |
| C++ + Qt | Technically suitable, but adds build and maintenance work without a clear benefit here. |
| C++ + wxWidgets | Worth reconsidering if broad legacy Windows or x86 support becomes mandatory. |

### Windows compatibility and distribution

Qt's documentation checked during the discussion lists Windows 10 1809 or later
on x64 for Qt 6.11. It also states that Qt 6.12 will be the last version supporting
Windows 10. Choose and pin a mutually compatible Python/PySide6/PyInstaller set;
do not interpret this proposal as a recommendation to install every latest release.
Recheck support at implementation time. C++ with Qt has the same Qt platform limit.

Framework support is not proof that the finished application runs on 20H2. Test
the packaged application on a clean Windows 10 20H2 x64 machine or VM and test
real serial hardware separately. USB/RS232 driver availability remains a separate
requirement. Include required runtime libraries in the distribution.

Define portable settings and log locations explicitly. A writable application
folder can support portable mode; a read-only folder needs a clear alternative
such as a user-selected directory or a per-user data directory.

## Existing implementation findings

The inspected source project targets .NET Framework 4.0. This describes the
checked-in source, not independently verified provenance of every shipped EXE.

| Location | Observed behavior | Consequence for the rewrite |
| --- | --- | --- |
| `.Old_Version/MC-Sourcecode/ModemController/MainForm.vb`, `Antwort` | Reads a line, adds newlines before and after it, then appends another blank line. | Excess spacing is partly introduced by the application, not only the modem. |
| `MainForm.vb`, `SendeATBefehl` | Combines `WriteLine` with an explicit `vbNewLine`. | Define transmitted terminators once and inspect the actual bytes. |
| `MainForm.vb`, `TimeOutAbwarten` | Runs 260,000 iterations of `Application.DoEvents`. | Replace the machine-dependent delay with explicit deadlines and response handling. |
| `MainForm.vb`, `portsetzen` | Sets read and write timeouts to 50 ms. | Separate low-level read polling from complete command-response deadlines. |
| `MainForm.vb`, `LadeEinstellungen` | Joins VCE lines into one command-entry string. | Import sequences as reviewed steps instead of blindly concatenating them. |
| `XMLParser.vb` and `XMLSettings.xml` | Serialize tree labels as encoded XML names and store command text in `Description`. | Separate the data model from the GUI tree and use ordinary fields. |

The observed HTerm discrepancies have not been reproduced. Baud rate, framing,
flow control, line endings, timing, and control-line behavior are hypotheses to
compare against a known-working HTerm session, not confirmed root causes.

## User interface

Keep the terminal as the central, largest part of the window. Put searchable
command categories and favorites beside it. Integrate command entry into the
terminal surface so typing, sent commands, and received responses share one
workspace; a separate send panel must not be required for ordinary use. Provide
clear connection state and a stop/cancel action.

### YAT evaluation and agreed product direction (2026-09-16)

The user evaluated YAT 2.8.2 portable with a small MC/TC command-page template.
An ESP32 was connected because no modem was available. This was a UI evaluation,
not modem interoperability or AT-response validation.

Keep the useful interaction ideas: a dropdown selects a command category or
profile, and a small group of labeled buttons presents its commands. Preserve
exact-byte buttons and an optional hex view. Build our own lightweight,
focused application rather than reproducing YAT's full feature set or interface.
Reuse interaction ideas and our own reviewed command data, not YAT program code
or binaries. Python, PySide6 and pySerial remain the agreed technology direction.

The user's reported friction during this trial was too many options, paths not
being remembered, presets needing repeated loading, and a receive area that did
not also serve as the terminal input area. These are trial observations and
product requirements, not verified claims that YAT cannot support persistence.

Requirements for our application:

- Keep ordinary use focused on the port, Connect, a category/profile dropdown,
  a compact command-button group, and the shared terminal surface. Put advanced
  settings and diagnostic detail behind an explicit expansion.
- Allow typing commands directly in the terminal workspace, with command history
  and sent/received content visible together. Preserve the received transcript;
  typing must edit the current input only. Define local echo and Enter/terminator
  behavior explicitly, without sending bytes merely when focus changes.
- Remember imported presets, user edits, the selected profile/category, and the
  last connection settings across restarts. Import once; normal startup must not
  require browsing for and reloading a preset file.
- Remember the last directories used for import, export, logs, and captures.
  Store settings in the chosen portable/per-user location and use relative paths
  for bundled resources. Handle moved or missing directories with a clear fallback
  instead of silently discarding the saved configuration.
- Restoring settings must not automatically transmit commands, execute setup
  sequences, or connect to a device. Connection remains an explicit user action.
- Keep empty buttons and secondary panels out of the default view. Favor a small,
  coherent interface over exposing every possible terminal feature at startup.

The tracked [YAT command-page reference](../.Info/YAT/README.md) preserves the
trial template as design/input material. The downloaded application and local
experiments remain under ignored `.Temp/`; no YAT runtime is a project dependency.

### Simple connection mode

- Select a COM port and choose **Connect** or **Find settings**.
- Use the selected profile or last successful connection parameters internally.
- Display the effective settings unobtrusively, for example
  `COM4 | 115200 | 8N1 | no flow control`.
- Refresh available ports and handle missing, busy, or unplugged devices clearly.

### Advanced connection mode

Expose baud rate, data bits, parity, stop bits, flow control, DTR/RTS, line ending,
response deadlines, and optional delays between commands or individual bytes.
Show CTS/DSR/RI/CD states where supported. Keep these controls collapsible.
Users must also be able to try settings manually without running a search.

## Terminal and byte handling

Treat the transport as a byte stream. Store received and transmitted bytes
independently of text decoding, line normalization, and display formatting.

- Offer text, hexadecimal, and combined byte/text views of the same captured data.
- Keep a compact readable view that collapses surplus empty lines for display.
  Preserve the original bytes and meaningful spacing in raw capture/export.
- Allow explicit text encoding and visible control characters for diagnosis.
- Distinguish sent and received data and provide timestamps and byte counts.
- Support history, search, copy, clear display, and session export.
- Pause autoscroll while the user reads older output.
- Bound the visible history so long sessions do not freeze the GUI. Make capture
  retention and truncation behavior explicit rather than silently losing data.
- Buffer partial responses across reads and handle CR, LF, CRLF, and prompts
  without a newline. A serial read boundary is not a response boundary.

### Sending text and exact bytes

| Control | Bytes or behavior |
| --- | --- |
| CR button | `0D` |
| LF button | `0A` |
| CRLF button | `0D 0A` |
| ESC button | `1B` |
| Ctrl+Z button | `1A` |
| Hex entry | For example, `41 54 0D` sends `AT` followed by CR. |
| Custom byte buttons | Named, editable byte sequences stored with the catalog/profile. |

Text entry offers `None`, `CR`, `LF`, and `CRLF` terminators. Hex input and raw
control-character buttons send exactly their configured bytes with no implicit
terminator. Validate malformed hex before sending. Show what will be transmitted.

## Find settings workflow

Provide a built-in guided routine; users should not have to author a script.
It searches the selected COM port only and remains cancellable throughout.

1. Try the last successful settings and relevant profile defaults first.
2. Run a quick search over a bounded list of common baud rates using the normal
   framing and flow-control assumptions for the selected profile.
3. If needed, offer a broader search over user-selected framing and flow-control
   combinations. Show the search scope and progress rather than silently trying
   every possible combination.
4. For each candidate, configure the PC port, allow a bounded settling interval,
   separate previous input from the new attempt, and send only uppercase `AT`
   with the selected terminator, normally CR. Retain pre-attempt bytes in capture.
5. Wait for a complete standalone `OK` response within a command deadline. An
   echoed `AT`, an arbitrary substring, or an unrelated unsolicited message must
   not count as success. Account for delayed replies from an earlier attempt.
6. Confirm a candidate with repeated, separate AT exchanges before reporting it.
7. Stop at a confirmed candidate and offer **Use connection** and **Save profile**.
   Show the exact settings and response evidence, with optional further search.
8. On cancellation or failure, return to the prior PC-side settings where possible
   or a clearly disconnected state. Release port ownership predictably.

Describe the result as **working settings found**, not proof of the modem's saved
configuration. Autobaud can synchronize a modem to the rate used for `AT`, so more
than one rate may work. A short AT exchange also cannot fully validate flow control
for larger transfers or uniquely identify every framing parameter.

No response is inconclusive: a modem may be in data mode, asleep, configured for
suppressed or numeric result codes, or connected through unsuitable wiring.
Display this distinction rather than declaring the modem defective. Numeric-result
support, if added, needs deliberate matching rules and hardware validation.

The routine must not send reset, factory-default, baud-setting, persistence,
dialing, or escape-sequence commands. Changing PC settings and opening/closing a
port can still affect DTR/RTS and an active connection. Define control-line policy
per profile and avoid using the routine during an active data session. AT-only
search is not a guarantee of zero device-side effects under autobaud.

## Command catalog, profiles, and migration

Replace direct tree serialization with a versioned, GUI-independent JSON model.
Keep an ordinary editor with fields for name, category, command or byte sequence,
help text, parameters, supported model/profile, expected response, and timeout.

- Search categories and commands; add favorites, duplicate entries, reorder them,
  and import/export selected profiles.
- Use parameter fields for phone numbers, PINs, and other arguments. Do not ship
  personal phone numbers or secrets copied from old presets as defaults.
- Mark destructive or state-changing actions clearly. Keep read-only diagnostic
  actions separate from reset, persistence, SMS deletion, and configuration changes.
- Keep shipped defaults separate from user modifications so updates preserve edits.
- Model sequences as steps with response conditions, deadlines, cancellation, and
  optional delays. Prefer a declarative runner over arbitrary executable scripts.
- Preview legacy XML/VCE imports, decode their existing XML naming convention,
  preserve original files, and flag ambiguous entries or concatenated init strings.
- Preserve the user's catalog knowledge while reviewing command correctness and
  modem applicability against the relevant manufacturer documentation.

## Diagnostics and maintenance

Use shared basic commands plus device-specific profiles. MC93 supports LTE Cat-M
and NB-IoT, so a legacy GSM-only catalog is insufficient. Identify the exact modem
and firmware before enabling manufacturer-specific extensions.

The user mentioned TC55i; repository notes also contain MC55i-Q, MC55i-W, and
TC35i material. Confirm the exact hardware names rather than treating them as
interchangeable. Stollmann is a legacy import concern, not a current priority.

| Area | Intended assistance |
| --- | --- |
| Serial connection | Port configuration, handshaking, status signals, and comparison with a working HTerm session. |
| Device identity | Manufacturer, model, and firmware queries. |
| SIM | Readiness and PIN-state checks; guided parameter entry for explicit changes. |
| Network | Registration, operator, technology, and explained signal measurements. |
| Errors | Supported extended error information and understandable explanations. |
| SMS | Storage status, reading, and a guided send sequence; deletion as a separate action. |
| Diagnostic report | Export the query sequence, raw answers, timestamps, and connection settings. |

Add a **Run diagnostics** action that selects read-only queries appropriate to
the active profile. Unsupported queries must be reported and must not silently
trigger configuration changes. Treat asynchronous modem notifications separately
from the active command response.

SMS sending is a multi-step exchange: send the command, wait for `>`, send the
encoded message and the actual Ctrl+Z byte, then await completion. Literal text
such as `<Ctrl+Z>` is not a substitute. Profile-specific deadlines and cancellation
behavior must be defined for such interactions.

## Proposed internal structure

Keep five responsibilities separate:

1. **GUI:** terminal views, connection controls, catalog editor, and progress.
2. **Serial transport:** a single owner of the port, exact-byte reads/writes,
   connection lifecycle, control lines, and disconnection handling.
3. **Protocol/session processing:** partial data buffering, response boundaries,
   prompts, unsolicited notifications, and command deadlines.
4. **Catalog and profiles:** validated data, persistence, and legacy import.
5. **Workflow runner:** connection search and declarative diagnostic sequences.

Run serial work outside the GUI thread and deliver updates through a safe message
mechanism. Serialize commands so manual input, diagnostics, and setting searches
cannot interleave accidentally. Avoid busy waits and `Application.DoEvents`-style
reentrancy. A simulator/replay transport should make protocol tests independent
of physical hardware.

## Suggested implementation sequence

1. Confirm exact device models, collect successful HTerm settings and representative
   response captures, and choose a Windows-10-compatible dependency set.
2. Build the byte-oriented transport, basic/advanced connection UI, terminal,
   control-character buttons, raw logging, and text/hex views.
3. Package an early executable and test it on Windows 10 20H2 with real hardware.
4. Add the command/profile editor and previewable legacy imports.
5. Add the bounded, cancellable AT-only connection search.
6. Add model-specific diagnostics, SMS workflows, and report export.
7. Verify the complete portable package and document supported devices and limits.

Do not translate the old form line-for-line. Reuse its workflow and reviewed
catalog content while replacing timing, transport, and persistence boundaries.

## Acceptance and validation

- Packaged startup on clean Windows 10 20H2 x64 without a separately installed
  Python environment, plus a Windows 11 smoke check.
- Real-device checks with representative current modems and USB/RS232 adapters;
  capture the exact model, firmware, driver, and tested connection parameters.
- Byte-for-byte verification of AT terminators, raw hex, ESC, and Ctrl+Z.
- Receive tests for split CRLF, partial responses, empty lines, invalid text bytes,
  prompts without newlines, delayed responses, and interleaved notifications.
- Responsive GUI under continuous traffic, clear disconnect/busy-port handling,
  deterministic cancellation, and bounded visible history.
- Search rejects echoes and stale/unrelated OKs, confirms new responses, remains
  bounded, and never emits configuration/reset/save commands.
- Legacy import preserves originals and exposes unsupported/ambiguous entries.
- Restart restores presets, user edits, selected category/profile, connection
  settings and file-dialog directories without reimport or automatic device I/O.
  Verify portable-folder relocation and missing-path fallback separately.
- Ordinary AT entry works in the shared terminal workspace without a separate
  send window; sent and received content remains readable together.
- Explicit differentiation between simulator tests, packaging checks, and actual
  hardware evidence. None of these implementation checks has run yet.

## Agent tooling and repository hygiene

- Version only `.serena/project.yml`, `.serena/.gitignore`,
  `.projectatlas/config.toml`, and
  `.projectatlas/projectatlas-nonsource-files.toon` from the agent directories.
- Keep databases (including SQLite WAL/SHM files), caches, locks, generated maps,
  local memories, local overrides, and generated host MCP launch configurations
  out of Git. Root ignore rules allow only the named shared configuration files.
- Atlas host configurations currently contain machine-specific absolute paths;
  regenerate them locally with the installed ProjectAtlas setup workflow.
- ProjectAtlas was initialized for this repository. Its existing VB support is
  metadata/text-oriented, not a verified VB symbol graph. Refresh after changes.
- Serena's initial Erlang selection was unrelated to this project. Shared settings
  now select Python and Markdown for the planned application and documentation.
  This is configuration, not evidence that language servers or new code pass a
  health check. Verify activation when implementation begins.
- Preserve the legacy application and unrelated files. Continue the preparation
  branch or explicitly agree its successor; avoid duplicate implementation work.

## References

These sources informed the discussion; recheck versions and hardware applicability
when implementation starts.

- [Qt for Python / PySide6](https://doc.qt.io/qtforpython-6/)
- [Qt Windows support and Windows 10 support boundary](https://doc.qt.io/qt-6/windows.html)
- [pySerial API, timeouts, and control lines](https://pyserial.readthedocs.io/en/latest/pyserial_api.html)
- [PyInstaller distribution and packaging behavior](https://pyinstaller.org/en/stable/operating-mode.html)
- [MC93 manufacturer information](https://mc-technologies.com/en/produkt/163358-2/)
- [MC93 User Guide V2.7](https://mc-technologies.com/wp-content/uploads/2024/08/User-Guide-MC93-V2.7.pdf)
- [Quectel GSM UART Application Note: autobaud behavior for covered modules](https://quectel.com/content/uploads/2021/03/Quectel_GSM_UART_Application_Note_V1.2.pdf)

Local evidence: `.Old_Version/MC-Sourcecode/ModemController/`,
`.Old_Version/ModemController_V1.5.0.10/`, `docs/Infos/AT-Befehle.txt`,
`docs/Infos/Init-Strings.md`, the modem manuals under `docs/Infos/`, and the
screenshots under `docs/images/`. Some local
reference content is ignored by Git; verify availability in a fresh checkout.
