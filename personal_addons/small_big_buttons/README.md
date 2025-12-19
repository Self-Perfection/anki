# Small and Big Text Buttons

⚠️ **STATUS: NOT WORKING** - This addon is currently non-functional due to architectural limitations.

Anki addon attempting to add `<small>` and `<big>` buttons to the editor toolbar.

## ❌ Current Problem

The addon **does not work** when clicking the buttons. The buttons appear in the toolbar but do nothing when activated.

## 🔍 Why Standard Editor Buttons Work (and ours don't)

### Standard Built-in Buttons Architecture

Anki's built-in formatting buttons (Bold, Italic, Underline, etc.) use a sophisticated TypeScript/Svelte architecture:

#### 1. **Direct DOM Access**
```typescript
// BoldButton.svelte
import { surrounder } from "../rich-text-input";

function applyAttribute(): void {
    surrounder.surround('bold', exclusiveNames);
}
```

The `surrounder` object has **direct access** to the editor's contenteditable field through Svelte component context.

#### 2. **Surrounder System** (ts/editor/surround.ts)
```typescript
export class Surrounder<T> {
    #api?: SurroundedAPI;  // Direct reference to editor API

    async surround(formatName: string): Promise<void> {
        const base = await this.#getBaseElement();  // Direct access!
        const selection = getSelection(base)!;      // Works in shadow DOM
        const range = getRange(selection);

        // Complex logic that preserves existing formatting
        const clearedRange = removeFormats(range, base, exclusives);
        const matches = isSurroundedInner(clearedRange, base, matcher);
        surroundAndSelect(matches, clearedRange, base, format, selection);
    }
}
```

#### 3. **Low-level DOM Manipulation** (ts/lib/domlib/surround/)
```typescript
export function surround<T>(range: Range, base: Element, format: SurroundFormat<T>): Range {
    const splitRange = splitPartiallySelected(range);
    const build = new BuildFormat(format, base, range, splitRange);
    const apply = new ApplyFormat(format);
    return surroundOnCorrectNode(range, base, build, apply, boolMatcher(format));
}
```

This system:
- Splits partially selected text nodes
- Builds a tree representation of formatting
- Applies changes while **preserving existing tags**
- Handles complex cases (nested formatting, partial selections, etc.)

### Why Python Addons Can't Use This System

#### ❌ No Direct DOM Access
```python
# Python addon code
def wrap_text(editor: Editor, tag: str):
    # We can only execute JavaScript strings via bridge
    editor.web.eval("some_javascript_code")
    # We have NO direct access to the Surrounder instance
    # We have NO access to the editor's shadow DOM context
```

#### ❌ No Svelte Component Context
```python
# We can't do this from Python:
from ts.editor.rich_text_input import surrounder  # ❌ Not possible!
surrounder.surround('small', [])  # ❌ No access!
```

#### ❌ Shadow DOM Isolation
```python
# When we execute JavaScript via editor.web.eval():
js_code = """
    const sel = window.getSelection();  // ⚠️ May not work in shadow DOM
    const range = sel.getRangeAt(0);    // ⚠️ Wrong context
"""
editor.web.eval(js_code)
```

The editor field is inside a shadow DOM or iframe context that `window.getSelection()` can't access from our injected JavaScript.

## 🔧 Attempted Solutions

### Attempt 1: Direct Range API Manipulation
```python
js_code = f"""
    const field = document.activeElement;
    const selection = field.ownerDocument.getSelection();
    const range = selection.getRangeAt(0);
    const wrapper = document.createElement('{tag}');
    const fragment = range.extractContents();
    wrapper.appendChild(fragment);
    range.insertNode(wrapper);
"""
editor.web.eval(js_code)
```
**Result**: ❌ Does nothing. Likely wrong DOM context.

### Attempt 2: Get HTML via Callback + pasteHTML
```python
js_get_selection = """
    const sel = window.getSelection();
    const range = sel.getRangeAt(0);
    const container = document.createElement('div');
    container.appendChild(range.cloneContents());
    return container.innerHTML;
"""

def on_selection_received(html: str):
    wrapped_html = f"<{tag}>{html}</{tag}>"
    editor.web.eval(f"pasteHTML({json.dumps(wrapped_html)}, true, false);")

editor.web.evalWithCallback(js_get_selection, on_selection_received)
```
**Result**: ❌ Does nothing. `window.getSelection()` returns empty/wrong selection.

## 📊 Architecture Comparison

| Feature | Built-in Buttons | Python Addon |
|---------|-----------------|--------------|
| **Language** | TypeScript/Svelte | Python |
| **DOM Access** | ✅ Direct via component context | ❌ Only via JavaScript eval |
| **Surrounder System** | ✅ Full access | ❌ Not accessible |
| **Selection API** | ✅ Correct shadow DOM context | ❌ Wrong context via eval |
| **Format Preservation** | ✅ Complex tree-based algorithm | ⚠️ Simple HTML wrapping |
| **Integration** | ✅ Native Svelte components | ⚠️ Legacy addButton() hook |

## 🎯 What We Need (But Can't Access)

To make this work properly, we would need:

1. **Access to the Surrounder instance** from Python
   ```python
   # This doesn't exist:
   editor.surrounder.registerFormat('small', {'surroundElement': 'small', ...})
   editor.surrounder.surround('small', [])
   ```

2. **Proper JavaScript bridge function** exposed by Anki
   ```javascript
   // This doesn't exist in Anki:
   function wrapSelectionInTag(tagName) {
       globalThis.surrounder.surround(tagName, []);
   }
   ```

3. **Access to editor field context** from eval
   ```python
   # Current eval runs in wrong context
   editor.web.eval("...")  # Can't access editor's shadow DOM properly
   ```

## 💡 Possible Solutions (Not Implemented)

### Option 1: Patch Anki Core
Add a new method to Editor class:
```python
# In qt/aqt/editor.py
def wrapInTag(self, tag: str) -> None:
    self.web.eval(f"globalThis.wrapInTag({json.dumps(tag)});")
```

And expose it in TypeScript:
```typescript
// In ts/editor/
globalThis.wrapInTag = (tag: string) => {
    surrounder.surround(tag, []);
};
```

### Option 2: Create Svelte Component
Convert this addon to a Svelte component integrated directly into the editor toolbar (requires modifying Anki source).

### Option 3: Use execCommand (Lossy)
```python
# Works but DESTROYS existing formatting ❌
editor.web.eval(f"document.execCommand('insertHTML', false, '<small>text</small>');")
```

## 📝 Conclusion

This addon demonstrates the **architectural limitations of Python-based editor addons** in modern Anki. While the `editor_did_init_buttons` hook allows adding buttons to the toolbar, accessing the editor's formatting system requires TypeScript/Svelte integration that Python addons cannot utilize.

The modern Anki editor uses a sophisticated formatting system that is only accessible from TypeScript components with proper component context. Python addons are limited to:
- Adding buttons (visual only)
- Executing arbitrary JavaScript (but in wrong context)
- Cannot access the Surrounder system
- Cannot properly interact with shadow DOM

**This addon remains non-functional until Anki provides better Python API access to the editor formatting system.**
