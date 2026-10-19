import re

path = r"C:\Users\Administrator\Documents\Codex\2026-10-19\new-chat-3\ios-shortcuts-collection\generate_shortcuts.py"
with open(path, encoding='utf-8') as f:
    content = f.read()

old = '"WFWorkflowActionIDs": [a["id"] for a in actions],'
new = '"WFWorkflowActionIDs": [a.get("WFActionIdentifier", "") for a in actions],'
content = content.replace(old, new)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed!")
