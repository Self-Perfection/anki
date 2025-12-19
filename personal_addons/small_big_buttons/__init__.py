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
    Uses Range API to properly wrap content without destroying existing tags.
    """
    # JavaScript function that properly wraps selection without destroying existing tags
    js_code = f"""
    (function() {{
        const field = document.activeElement;
        if (!field) return;

        const selection = field.ownerDocument.getSelection();
        if (!selection || selection.rangeCount === 0) return;

        const range = selection.getRangeAt(0);
        if (range.collapsed) return; // Nothing selected

        // Create the wrapper element
        const wrapper = document.createElement('{tag}');

        // Extract the selected content
        const fragment = range.extractContents();

        // Put the content inside the wrapper
        wrapper.appendChild(fragment);

        // Insert the wrapper at the selection point
        range.insertNode(wrapper);

        // Update the selection to include the wrapped content
        range.selectNode(wrapper);
        selection.removeAllRanges();
        selection.addRange(range);

        // Move cursor to the end
        selection.collapseToEnd();

        // Trigger input event so Anki knows content changed
        field.dispatchEvent(new Event('input', {{ bubbles: true }}));
    }})();
    """

    editor.web.eval(js_code)


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
