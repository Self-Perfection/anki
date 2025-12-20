# External Resources

✅ **STATUS: WORKING** - This addon successfully adds external resource lookup buttons.

Anki addon that adds buttons to the editor toolbar for quickly looking up words in external dictionaries and resources.

## Features

### 🇵🇹 Infopedia PT-EN Dictionary

- Adds a button to look up words in [Infopedia Portuguese-English dictionary](https://www.infopedia.pt/dicionarios/portugues-ingles/)
- Uses the word from the **current active field**
- Opens the dictionary page in your default browser
- Works with any text field

## Usage

1. **Edit a card** in Anki
2. **Click or focus** on the field containing the word you want to look up
3. **Click the Infopedia button** in the editor toolbar (shows "PT" or custom icon)
4. Your browser opens with the dictionary entry for that word

## How It Works

```python
# When you click the button:
1. Get value from current active field
2. Strip HTML tags and whitespace
3. URL-encode the word
4. Open: https://www.infopedia.pt/dicionarios/portugues-ingles/WORD
```

## Customization

### Adding Your Own Icon

Replace `infopedia_pt.png.placeholder` with an actual PNG icon:

```bash
cd personal_addons/external_resources
# Download or create your icon (recommended size: 16x16 or 24x24 px)
# Save as infopedia_pt.png
```

If no icon is found, the button will display "PT" as text label.

### Adding More Resources

You can easily extend this addon to add more external resources:

```python
def open_another_dictionary(editor: Editor):
    word = get_field_value(editor)
    if not word:
        showWarning("No word selected")
        return

    url = f"https://example.com/dictionary/{urllib.parse.quote(word)}"
    QDesktopServices.openUrl(QUrl(url))

def add_another_button(buttons, editor):
    btn = editor.addButton(
        icon=None,
        cmd="another_dict",
        func=lambda e: open_another_dictionary(e),
        tip="Look up in Another Dictionary",
        label="AD",
    )
    buttons.append(btn)
    return buttons

gui_hooks.editor_did_init_buttons.append(add_another_button)
```

## Architecture Comparison

Unlike the `small_big_buttons` addon that attempted to manipulate DOM formatting, this addon successfully works because:

| Feature | External Resources | Small/Big Buttons |
|---------|-------------------|-------------------|
| **Task** | Open external URL | Wrap text in tags |
| **DOM Access Needed** | ❌ No | ✅ Yes (failed) |
| **Python API Sufficient** | ✅ Yes | ❌ No |
| **Works** | ✅ Yes | ❌ No |

### Why This Works

```python
# We only need:
1. Get field value → editor.note[field_name]  ✅ Available
2. Open URL → QDesktopServices.openUrl()     ✅ Available
```

We don't need:
- ❌ Direct DOM manipulation
- ❌ Surrounder system access
- ❌ Shadow DOM context
- ❌ JavaScript execution in editor context

## Technical Details

**Language:** Python
**Qt Integration:** Uses `QDesktopServices.openUrl()` for cross-platform browser opening
**Hooks:** `editor_did_init_buttons` for adding toolbar buttons
**Field Access:** Uses `editor.note[field_name]` and `editor.currentField`

## Installation

Copy the `external_resources` folder to your Anki addons directory.

## Future Enhancements

Possible additions:
- More dictionary/resource buttons (Linguee, WordReference, etc.)
- Configuration dialog to customize URLs
- Keyboard shortcuts
- Support for multi-word selections
- Context menu integration
- Configurable field selection (instead of always using current field)

## License

GNU AGPL, version 3 or later
