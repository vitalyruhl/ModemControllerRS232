# Documentation index

- [AT modem diagnosis reference](reference/at-commands.md): primary offline text
  reference for queries, result interpretation, control bytes, SMS, profile notes
  and historical initialization caveats.
- [YAT evaluation template](../.Info/YAT/README.md): our MC/TC command pages and
  evaluation limits; the YAT application itself is not included.
- [Screenshots](images/): captures of the previous application.
- [Project overview](../README.md): current scaffold state, architecture areas,
  legacy application and distribution background.

Use the text reference first: it can be opened without a PDF viewer. PDFs below
are supplementary device references, not duplicate quick-start documents. Their
different model/version scope matters; filenames do not establish compatibility.

## Manufacturer references

| Source | Scope and limitations |
| --- | --- |
| [TC35/TC37 AT manual, version 04.00](reference/modems/tc35/tc3x_atc_01_v0400.pdf) | Legacy command reference, not proof of modern LTE/modem support. |
| [TC35i hardware description](reference/modems/tc35/tc35i_t_hd_v0301n.pdf) | Terminal hardware, serial interface and control signals. |
| [Supplementary TC35 document](reference/modems/tc35/1114471.pdf) | Text extraction was unreliable; visually review before relying on it. |
| [TC35i incoming-call incident attachment](reference/modems/tc35i-incoming-calls/gsm-caller-id.pdf) | Image-based supplementary evidence; the text reference records the known caveats. |
| [MC88 developer guide](reference/modems/MC88/m2mdev_M2M_Developer_Guide_4551.pdf) | Device context and example investigations; some examples change settings. |
| [Cellular terminal flyer](reference/modems/MC88/flyer_cellulare.pdf) | Product/module context, not an AT command specification. |
| [MC88 terminal flyer](reference/modems/MC88/MC88_Term_fl.pdf) | Prior local extraction reported no pages; not verified as usable evidence. |
| [ELSA MicroLink Office AT manual](reference/modems/elsa-microlink-at-commands.pdf) | Analog/Hayes reference, not a cellular command catalog. |

Historical [MC88 USB modem INF](reference/modems/MC88/usbmodem.inf) and
[USB/RS232 driver artifacts](reference/modems/usb-rs232-drivers/) are retained as
references only. They are not runtime dependencies, Windows 10 compatibility
evidence, or instructions to install drivers automatically.

## Source consolidation

The former AT command list, MC55i-Q/W initialization notes (2023-02-03), and
TC35i incoming-call note (2020-11-23) are consolidated into the text reference.
Examples containing personal values are omitted; ambiguous spellings and device
assumptions are flagged instead of silently converted into working commands.
Original documents remain available in repository history. Distinct manufacturer
manuals remain alongside the concise text, without duplicating entire manuals.

The Python source and test directories remain placeholders; this documentation
does not establish passing software, packaging, Windows or real-device tests.

