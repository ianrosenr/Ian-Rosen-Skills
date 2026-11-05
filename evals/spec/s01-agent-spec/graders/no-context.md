---
type: regex
pattern: '#+ *Context'
match: not_contains
target: { source: file, path: specs/out.md }
---
