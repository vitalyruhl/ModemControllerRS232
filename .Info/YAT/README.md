# YAT MC/TC command-page reference

`MC-TC-Commands.yacps` is our command-page template used to evaluate YAT 2.8.2
portable on 2026-09-16. It is preserved as reference data for the planned modem
controller. No YAT executable, library, installer, or other runtime is included.
The local downloaded application remains under ignored `.Temp/`.

## Included pages

| Page | Contents |
| --- | --- |
| MC-TC Status | Eight common AT queries: connection, identity, SIM, registration, signal, operator, baud rate, and SMS storage. |
| Control bytes | CR, LF, CRLF, ESC, Ctrl+Z, and `AT` followed by CR. |
| MC-TC Setup - changes settings | Six individual configuration commands for registration reporting, caller ID, extended ring, SMS mode, notifications, and storage. |

Setup commands come from the repository's MC55i-Q/MC55i-W initialization notes
and legacy TC35i material. This is not a verified MC93/TC55i device profile.
Vendor-specific routing, resets, factory defaults, save-to-flash commands, and
automatic initialization sequences are omitted.

## Loading the reference in YAT

Open the predefined-command editor with **Ctrl+Shift+D** and import the `.yacps`
file. Use **Add pages from file** to preserve existing pages. Select the desired
page in the dropdown. **Hide Undefined Commands** removes unused buttons, and
**View > Panels > Send File** can hide file transmission. Save the terminal with
**Ctrl+S** to preserve its layout and settings in a separate `.yat` file.

Select the actual serial settings and the appropriate send terminator before
connecting to a modem; ordinary AT commands normally use CR. The raw-byte buttons
use YAT's `\!(NoEOL)` keyword and append no implicit terminator. Setup buttons
change device settings when sent; Ctrl+Z can submit pending input, and ESC can
cancel it. Check device support and context before sending.

## Evidence and limits

All 20 command strings were accepted by YAT 2.8.2's parser during offline
validation. Raw payloads decoded to `0D`, `0A`, `0D 0A`, `1B`, `1A`, and
`41 54 0D`, respectively. The template was successfully imported into the UI.
No command button was used to transmit during setup. Only an ESP32 was available;
modem behavior and serial settings were not validated.

The user liked category selection through a dropdown and the command buttons,
but found the overall interface too busy and the separate receive/input areas
unsuitable. Preset and path persistence were also points of friction in the
trial. Our application will adopt selected interaction ideas while providing
integrated terminal input and persistent settings. See the
[upgrade proposal](../../docs/upgrade.md) for the agreed requirements.
