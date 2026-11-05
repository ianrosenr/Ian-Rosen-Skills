---
type: regex
pattern: '#+ *Goal[\s\S]*#+ *Constraints[\s\S]*#+ *Interfaces[\s\S]*#+ *Files touched[\s\S]*#+ *Acceptance criteria[\s\S]*#+ *Out of scope'
target: { source: file, path: specs/out.md }
---
