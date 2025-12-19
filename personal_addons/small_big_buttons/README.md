# Small and Big Text Buttons

Anki addon that adds `<small>` and `<big>` buttons to the editor toolbar.

## Features

- Adds two new buttons to the editor: **small** and **big**
- Wraps selected text in `<small>` or `<big>` HTML tags
- **Preserves existing HTML formatting** (bold, italic, etc.)
- Keyboard shortcuts:
  - `Ctrl+Shift+,` for `<small>`
  - `Ctrl+Shift+.` for `<big>`

## How it works

Unlike the original version that used `document.execCommand('insertHTML')`, this addon uses the **Range API** to properly wrap selected content. This approach:

1. Extracts the selected content (including all nested HTML tags)
2. Creates a wrapper element (`<small>` or `<big>`)
3. Places the extracted content inside the wrapper
4. Inserts the wrapper back into the document

This preserves all existing formatting like bold, italic, underline, etc.

## Example

If you have text like this:
```html
This is <b>bold</b> and <i>italic</i> text
```

And you select "**bold** and **italic**" and click the `small` button, you get:
```html
This is <small><b>bold</b> and <i>italic</i></small> text
```

Instead of losing the formatting (which would happen with `insertHTML`).

## Installation

Copy the `small_big_buttons` folder to your Anki addons directory.

## Technical Details

The addon uses:
- **Python hooks**: `editor_did_init_buttons` to add buttons
- **JavaScript Range API**: To wrap selected content without destroying existing tags
- **Event dispatching**: Triggers `input` event so Anki knows the content changed
