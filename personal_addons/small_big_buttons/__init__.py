# Copyright: Self-Perfection
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
"""
Addon to add <small> and <big> buttons to the Anki editor.
Preserves existing HTML formatting when wrapping text.
"""

from aqt import gui_hooks
from aqt.editor import Editor


def wrap_text(editor: Editor, tag: str):
    """
    Wraps selected text in an HTML tag, preserving existing formatting.
    Gets selected HTML via callback, wraps it, and inserts back.
    """
    # JavaScript to get the selected HTML content
    js_get_selection = """
    (function() {
        const sel = window.getSelection();
        if (!sel || sel.rangeCount === 0) return '';

        const range = sel.getRangeAt(0);
        if (range.collapsed) return '';

        // Create a temporary container to get HTML of selection
        const container = document.createElement('div');
        container.appendChild(range.cloneContents());
        return container.innerHTML;
    })();
    """

    def on_selection_received(html: str):
        if not html:
            return

        # Wrap the HTML in the specified tag
        wrapped_html = f"<{tag}>{html}</{tag}>"

        # Insert the wrapped HTML using Anki's pasteHTML function
        # This preserves formatting better than execCommand
        import json
        editor.web.eval(f"pasteHTML({json.dumps(wrapped_html)}, true, false);")

    # Get selection HTML and process it
    editor.web.evalWithCallback(js_get_selection, on_selection_received)


def add_small_button(buttons, editor):
    """Adds <small> button to the editor toolbar"""
    btn = editor.addButton(
        icon=None,
        cmd="small_text",
        func=lambda e: wrap_text(e, "small"),
        tip="Wrap in <small> tag (Ctrl+Shift+,)",
        label="small",
        keys="Ctrl+Shift+,",
    )
    buttons.append(btn)
    return buttons


def add_big_button(buttons, editor):
    """Adds <big> button to the editor toolbar"""
    btn = editor.addButton(
        icon=None,
        cmd="big_text",
        func=lambda e: wrap_text(e, "big"),
        tip="Wrap in <big> tag (Ctrl+Shift+.)",
        label="big",
        keys="Ctrl+Shift+.",
    )
    buttons.append(btn)
    return buttons


# Register hooks
gui_hooks.editor_did_init_buttons.append(add_small_button)
gui_hooks.editor_did_init_buttons.append(add_big_button)
