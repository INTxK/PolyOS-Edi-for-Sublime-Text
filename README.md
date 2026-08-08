# PolyOS Editor for Sublime Text

> **v.3.3.4** — Updated 2026-08-08

A single package that bundles the PolyOS editor suite for Sublime Text 4,
including keybindings, shared preferences, and an auto-sync plugin for your
per-device `Packages/User` profile:

| Sub-package | What it ships |
| ----------- | ------------- |
| **PolyMark** | Custom syntax + color scheme for `.md`, `.txt` and `.pm`. Highlights dates, to-dos, tags, statuses, filenames and more. |
| **PolyOS Editor Dark** | UI theme (`PolyOS Editor Dark.sublime-theme` + `assets/`). Reads the active color scheme's `accent`/kind hooks so PolyMark and ProseMode re-tint the UI chrome automatically. |
| **ProseMode** | Focused monochrome color scheme for distraction-free writing. |

## Automatic updates

Every change is delivered through Package Control: when a new version is tagged
in this repository, the installed package upgrades itself (checked at startup
and every 4 hours by default). No terminal or sync scripts required.

The bundled **auto-sync plugin** (`polyos_auto_sync.py`) keeps the parts
Package Control can't manage — your `Packages/User` preferences and the
`Package Control.sublime-settings` baseline — in sync across devices. It
applies the package's `profile/` folder to `Packages/User` at startup, every 4
hours, or on demand via `PolyOS: Sync Profile Now`.

The PolyOS look is **use-ready on install**: the profile merges the shared
preferences (theme, color scheme, default syntax, fonts, caret) into your
`Packages/User/Preferences.sublime-settings`, so it wins over any stock
preferences — while preserving unrelated settings you already had.
`Package Control.sublime-settings` is merged (never clobbered), so packages you
installed yourself are preserved.

## Install via Package Control

> **Note:** the package installs under the name **PolyOS-Edi-for-Sublime-Text**
> (its repository name), and appears as such in `Preferences > Package Control >
> List Packages`. The syntax/color-scheme/theme labels inside stay distinct
> ("PolyMark", "ProseMode", "PolyOS Editor Dark").

1. Open `Command Palette` (`Ctrl+Shift+P` / `Cmd+Shift+P`).
2. Run `Package Control: Add Repository` and paste:
   `https://github.com/INTxK/PolyOS-Edi-for-Sublime-Text`
3. Run `Package Control: Install Package` and select
   `PolyOS-Edi-for-Sublime-Text`.

Once installed, Sublime Text reads the package from `Packages/PolyOS-Edi-for-
Sublime-Text/` (`Preferences > Browse Packages...`). The prebuilt
`dist/PolyOS-Edi-for-Sublime-Text.sublime-package` archive holds the same files
for users who prefer installing a single `.sublime-package`.

## Manual install

Drop the folder into your Sublime Text packages directory so the resources sit
at `Packages/PolyOS-Edi-for-Sublime-Text/`:

- Windows: `%APPDATA%\Sublime Text\Packages\`
- macOS: `~/Library/Application Support/Sublime Text/Packages/`

## Quick start

1. Open a `.md`, `.txt` or `.pm` file — PolyMark selects itself as the syntax.
2. `Cmd+Shift+P` → `UI: Select Color Scheme > PolyMark` (or `ProseMode`).
3. Enable the theme via `Preferences > Theme > PolyOS Editor Dark`.

> **Note:** because PolyMark auto-selects for `.txt`, it becomes the default
> syntax for every plain-text file. If you don't want that, delete the `txt`
> entry from `file_extensions:` at the top of `polymark.sublime-syntax`.

## What you can write

| Rule | Feature | Type this |
| ---- | ------- | --------- |
| A2a  | Arrow ligature | `->` |
| A7   | List markers | `- item`, `+ item` |
| A8   | Date header | `2026-08-05` |
| A9   | Duration range | `16-18-07 -> 16-18-12` |
| E1   | Area/project hierarchy | `@Inbox/@Work` |
| E2   | Headings | `# H1` … `###### H6` |
| E3   | To-do item (open) | `- [ ] task` |
| E4   | To-do item (done) | `- [x] task` |
| E5   | Metadata definition | `[Thoughts]: value` |
| E6   | Horizontal rule | `---` |
| E7   | Blockquote | `> text` |
| E8   | Quoted string | `"text"` |
| E9   | Comment | `/// text` |
| E10  | Bold | `**text**` |
| E11  | Italic | `*text*` |
| E12  | Custom tag | `<note>…</note>` |
| E13  | Date-time-stamp | `2025-12-18-16-08-32` |
| E14  | Email address | `name@provider.com` |
| E15  | Inline status markers | `[?]`, `[!]` |
| E16  | Single-line code marker | `$ command` |
| E17  | Task statuses | `- [/] text`, `- [-] text` |
| E18  | Filename with extension | `draft_2.docx` |
| A6a  | Keywords (extension point) | off by default |

Every rule is rendered live in `Examples.md` — open it in Sublime Text with
PolyMark active to see the full reference.

## Documentation

| Document | What it's for |
| -------- | ------------- |
| [`Examples.md`](Examples.md) | Interactive feature reference / cheat-sheet |
| [`Instructions.md`](Instructions.md) | Setup, activation, customization, troubleshooting |

## Customization

Colors and syntax knobs — file extensions, tag charset, timestamp/date/duration
formats, email and filename constraints, marker characters, and the keyword
extension point — are documented in the **PARAMETERS** sections at the top of
`polymark.sublime-syntax` and `polymark.sublime-color-scheme`. See
`Instructions.md` for a guided walkthrough.

## Files

```
├── polymark.sublime-syntax              Syntax rules (scopes every feature)
├── polymark.sublime-color-scheme        Color scheme (paints those scopes)
├── ProseMode.sublime-color-scheme       Focused writing color scheme
├── PolyOS Editor Dark.sublime-theme     UI theme
├── assets/                              Theme assets (2x PNGs)
├── Default (OSX|Windows).sublime-keymap F5/F6/F7 + tab bindings
├── Preferences.sublime-settings         Shared cross-platform preferences
├── *.sublime-settings                   Per-syntax settings (JSON, Plain Text, ...)
├── prose_toggles.py                     F5/F6/F7 command implementations
├── polyos_auto_sync.py                  User-profile auto-sync plugin
├── profile/                             Applied into Packages/User by the plugin
├── Examples.md                          Interactive feature reference
├── Instructions.md                      Setup & customization guide
└── LICENSE                              MIT License
```

## License

MIT License. See `LICENSE` for the full text.
