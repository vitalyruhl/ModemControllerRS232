# AT modem diagnosis reference

This is the primary offline text reference for common GSM/cellular AT commands,
profile notes, and historical initialization findings. It consolidates the former
command list, MC55i initialization notes, and TC35i incoming-call note. Commands
are reference data, not an executable setup script or a claim of device support.
The [documentation index](../README.md) lists supplementary manufacturer manuals.

## Start with evidence

1. Confirm the COM port, wiring, serial settings, and whether another program owns
   the port. Opening a port can affect DTR/RTS and an existing connection.
2. Send `AT` with the required terminator, normally CR. Preserve the actual sent
   and received bytes. An echo is not a successful response.
3. Identify the manufacturer, module and firmware before using vendor extensions.
4. Read SIM state, registration, signal and operator information separately.
5. For SMS problems, inspect current SMS configuration before changing it. Preserve
   error codes and their timing; do not infer a cause from one failed command.

Treat `ERROR`, timeout, unsupported commands, unknown values, and an unavailable
network as different outcomes. Resetting, changing settings, dialing, sending SMS,
or saving to flash is never an implicit diagnostic step.

## Common queries

Support and exact response forms depend on the module and firmware. Test/query
forms such as `=?` and `?` are not interchangeable; do not generate arbitrary
probes from command names.

| Command | Purpose | Interpretation or caution |
| --- | --- | --- |
| `AT` | Basic command/response check | A standalone `OK` is evidence of communication, not full modem health. |
| `ATI` | Identification summary | Exact content is vendor-dependent. |
| `AT+CGMI`, `AT+CGMM`, `AT+CGMR` | Manufacturer, model, firmware | Use together to establish command applicability. |
| `AT+GCAP` | Report capabilities, where supported | Not an exhaustive feature guarantee. |
| `AT+CGSN` | Equipment identity, commonly IMEI | Sensitive identifier; omit from shared reports by default. |
| `AT+CIMI` | SIM subscriber identity (IMSI) | Sensitive; may fail while the SIM is locked or unavailable. |
| `AT+CPIN?` | SIM authentication state | `READY`, `SIM PIN`, `SIM PUK` and other locks require different handling. |
| `AT+CREG?` | Circuit-switched registration | Read the status field, not the reporting-mode field. |
| `AT+CGREG?` | Packet-domain registration, where supported | Keep separate from circuit-switched status. |
| `AT+CEREG?` | EPS registration, where supported | Do not assume availability on older GSM devices. |
| `AT+COPS?` | Current operator/selection mode | Unlike `AT+COPS=?`, this is not a full operator scan. |
| `AT+CSQ` | Signal quality | `99` means unknown/unavailable; see below. |
| `AT+CEER` | Last extended connection error, where supported | Context and supported error types are vendor-dependent. |
| `AT+CMEE?` | Current extended-error presentation | Enabling it with `=1` or `=2` changes a setting. |
| `AT+IPR?` | Configured serial rate, where supported | Working/autobaud settings are not necessarily saved settings. |
| `AT+CMGF?` | SMS format | Query before selecting text/PDU mode. |
| `AT+CSCS?`, `AT+CSCS=?` | Selected/available character sets | Supported character sets vary; UART text encoding is a separate concern. |
| `AT+CPMS?` | SMS storage selection and usage | `AT+CPMS=...` changes storage selection. |
| `AT+CNMI?` | SMS notification configuration | Does not itself read pending messages. |
| `AT+CSCA?` | SMS service-centre configuration | Do not replace it with a number copied from another installation. |
| `AT+CBC`, `AT+CCLK?` | Battery/power information and clock, where supported | Optional; not prerequisites for ordinary diagnostics. |

### SIM and registration

- `READY`: SIM authentication is satisfied, not proof of network registration.
- `SIM PIN`: obtain the user's PIN explicitly; do not guess or automatically retry.
- `SIM PUK`: stop ordinary PIN entry. Follow the applicable manufacturer/operator
  recovery procedure; repeated incorrect input can permanently block the SIM.
- `+CREG: <n>,<stat>` contains reporting mode first and registration state second.
  Basic legacy states are `0` not registered/not searching, `1` home network,
  `2` searching, `3` denied, `4` unknown, and `5` roaming.
- Other registration commands and newer devices can have additional fields/states.
  Preserve unknown values rather than reusing an old interpretation blindly.

### Signal quality

For the documented legacy `+CSQ: <rssi>,<ber>` encoding:

| RSSI | Meaning |
| --- | --- |
| `0` | -113 dBm or less |
| `1` | -111 dBm |
| `2` through `30` | -109 through -53 dBm, in 2 dB steps |
| `31` | -51 dBm or greater |
| `99` | Unknown or not detectable |

BER values `0` through `7` describe RXQUAL; `99` is unknown/unavailable. A meaningful
BER measurement can require an active connection. `99,99` is not zero signal.
Do not use legacy RSSI conversion for LTE-specific metrics such as RSRP/RSRQ.

## Exact bytes and SMS exchanges

| Action | Exact bytes |
| --- | --- |
| CR | `0D` |
| LF | `0A` |
| CRLF | `0D 0A` |
| ESC | `1B` |
| Ctrl+Z | `1A` |
| AT followed by CR | `41 54 0D` |

Hex/control-byte actions add no terminator. Text commands use the selected
terminator exactly once. ESC and Ctrl+Z can cancel/submit a pending exchange;
they are not harmless display characters.

An explicitly requested text-mode SMS send uses `AT+CMGS="<recipient>"`, waits for
the `>` prompt, then sends the validated message and the actual `1A` byte. The
literal string `<Ctrl+Z>` is not a substitute. Verify mode, character set and
length; do not assume PDU, Unicode, multipart, or arbitrary binary support.

After submission, timeout does not establish that nothing was sent. Do not retry
automatically. Reading messages with `AT+CMGR=<index>` or listing them with
`AT+CMGL=...` can change read/unread state. `AT+CMGD=<index>` deletes messages and
requires separate confirmation. Message content and recipients are private data.

## State-changing commands: explicit use only

These are capability references, not universal presets. Confirm syntax, support,
parameters and effects for the selected device before sending.

| Command or family | Effect / caution |
| --- | --- |
| `AT+CPIN="<PIN>"` | Unlocks the SIM; never log the argument or retry automatically. |
| `AT+CPIN="<PUK>","<new PIN>"` | PUK recovery on supported devices; not an ordinary PIN-change recipe. |
| `AT+CLCK="SC",0,"<PIN>"` | Disables SIM PIN protection, not merely unlocks this session. |
| `AT+CMEE=1` / `AT+CMEE=2` | Changes extended-error presentation; not a read-only probe. |
| `AT+CREG=1`, `AT+CLIP=1`, `AT+CRC=1` | Changes registration notifications, caller-ID reporting or ring result format. |
| `AT+CMGF=1`, `AT+CSCS=...` | Changes SMS mode or selected character set. |
| `AT+CNMI=...`, `AT+CPMS=...`, `AT+CSCA=...` | Changes SMS routing/storage/service-centre settings. |
| `AT+COPS=2` / `AT+COPS=0` | Deregisters / selects automatic registration; can interrupt service. |
| `AT+COPS=?` | Potentially long operator scan; exclude from a quick default batch. |
| `AT+CFUN=1,1` | Restart on supported devices; invalidates prior session/SIM observations. |
| `ATZ`, `AT&F`, `AT&W` | Restore a profile, restore defaults, save settings; distinct operations. |
| `AT+CGATT=0`, `AT+CGDCONT=...` | Changes packet attachment/context configuration. |
| `ATD...`, `ATD...;`, `ATD*99...`, `ATD*98...` | Initiates a data/voice/packet session; may incur costs. Not a diagnostic default. |
| `AT+CHUP`, `ATH` | Ends calls/connections; not a passive test. |
| `AT+CBST=...`, `AT+CSNS=...` | Changes bearer/call interpretation; model and network dependent. |
| `AT+CPBS`, `AT+CPBR`, `AT+CPBW` | Phonebook selection/read/write family; outside the core diagnosis scope. |
| `AT+CMGW`, `AT+CSCB`, `AT+CMMS`, `AT+CVIB` | Message storage/broadcast/link or vibration features; optional, device-specific. |

Old operator mailbox service codes are not universal modem commands. Verify them
with the current operator; do not ship historical numbers or provider assumptions
as default actions.

## Profile notes and historical initialization

Profiles group supported buttons and immediately visible device limitations.
Record terminal name, actual module, firmware, source and verification state.
User observations and manufacturer-backed facts must remain distinguishable.
Unknown/unsupported functions must not become enabled profile buttons.

### MC55i-Q and MC55i-W

The 2023-02-03 notes mention `ATZ`, followed by registration/caller-ID/ring and
text-SMS setup, notification selection `AT+CNMI=1,1`, and storage `AT+CPMS="MT"`.
These change state; they are not commands to run automatically on connection.

- The Q-labelled example additionally contains
  `AT+QURCCFG="urcport","uart1"`. Verify the actual module's documentation before
  enabling this vendor-specific routing action.
- The Q example separates commands with `|`; the W example combines multiple
  suffixes with spaces. Neither notation is a portable sequential execution API.
  Review and model individual commands with responses/timeouts instead.
- Do not infer that Q/W terminal labels uniquely establish the embedded module or
  guarantee that both devices support all the same commands.

### TC35/TC35i incoming-call incident

The 2020-11-23 note replaced an older initialization string with one including
`AT+CSNS=0` and `AT#CMGF=1`. The latter spelling is unverified; preserve it as an
import warning, not a corrected command to send. Mixed separators also need review.

The TC35-family AT manual describes `AT+CSNS` for incoming calls without bearer
information: `0` voice, `2` fax and `4` data (page 113, version 04.00). This does not
prove that the historical change fixed the reported incident. Verify the exact
TC35i firmware and intended bearer before applying it.

### Other device families and limitations

- MC88/MC88i developer material is useful context; product flyers are not command
  specifications. Do not infer MC93 or TC55i support from it.
- `AT+QNWINFO` is a vendor extension, not a generic GSM query. `No Service` is an
  observation, not proof of a hardware failure or empty credit balance.
- A reported inability to originate a wake-up/ringing call belongs in the affected
  profile's notes. The affected model has not been established; do not guess it.
- Legacy ELSA/Hayes material can explain serial concepts but does not establish
  cellular registration, SIM or SMS behavior.

## Error interpretation and provenance

Preserve `+CME ERROR` / `+CMS ERROR` codes and contextual replies. Decode them only
against an applicable specification. A failed SMS, `No Service`, a locked SIM,
searching registration, and unknown signal can coexist without proving one cause.
Ask for the next discriminating observation instead of automatically resetting.

This reference paraphrases the historical text notes; it is not a wholesale PDF
transcription. Manufacturer references remain supplementary, especially for
device-specific limits. The TC35-family manual documents CMEE, CPIN, CREG, CSNS
and CSQ on pages 84, 96, 108, 113 and 114 respectively. Follow the source links in
the documentation index when more detail or a current variant specification is
needed. Do not treat unreviewed manuals or historical installers as executable
instructions.
