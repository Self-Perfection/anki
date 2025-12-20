# Copyright: Self-Perfection
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
"""
External Resources addon for Anki.
Adds buttons to quickly look up words in external dictionaries and resources.
"""

import os
import urllib.parse
from typing import Optional

from aqt import gui_hooks
from aqt.editor import Editor
from aqt.qt import QDesktopServices, QUrl
from aqt.utils import showWarning


def get_field_value(editor: Editor, field_name: Optional[str] = None) -> str:
    """
    Get value from a specific field or current field.

    Args:
        editor: The editor instance
        field_name: Name of field to get value from. If None, uses current field.

    Returns:
        Field value with HTML tags stripped
    """
    if not editor.note:
        return ""

    if field_name:
        # Get value from specific field by name
        if field_name in editor.note:
            value = editor.note[field_name]
        else:
            return ""
    else:
        # Get value from current active field
        if editor.currentField is None:
            return ""

        # Get field name from field index
        fields = editor.note.note_type()['flds']
        if editor.currentField >= len(fields):
            return ""

        field_name = fields[editor.currentField]['name']
        value = editor.note[field_name]

    # Strip HTML tags
    import re
    value = re.sub(r'<[^>]+>', '', value)

    # Strip whitespace
    value = value.strip()

    return value


def open_infopedia_pt(editor: Editor):
    """
    Opens Infopedia PT-EN dictionary for the word in current field.
    """
    # Get word from current field
    word = get_field_value(editor, field_name='Word')

    if not word:
        showWarning("Could not get content of Word field")
        return

    # URL encode the word
    encoded_word = urllib.parse.quote(word)

    # Build URL
    url = f"https://www.infopedia.pt/dicionarios/portugues-ingles/{encoded_word}"

    # Open in browser
    QDesktopServices.openUrl(QUrl(url))


def add_infopedia_button(buttons, editor):
    """Adds Infopedia PT button to the editor toolbar"""
    addon_path = os.path.dirname(__file__)
    icon_path = os.path.join(addon_path, "infopedia_pt.png")

    # Use icon if it exists, otherwise use label
    icon = icon_path if os.path.exists(icon_path) else None

    btn = editor.addButton(
        icon=icon,
        cmd="infopedia_pt",
        func=lambda e: open_infopedia_pt(e),
        tip="Look up word in Infopedia PT-EN dictionary",
        label="PT" if not icon else "",
    )
    buttons.append(btn)
    return buttons


# Register hook
gui_hooks.editor_did_init_buttons.append(add_infopedia_button)
