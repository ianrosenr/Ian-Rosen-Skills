---
name: explain
description: Explain a topic, concept, code, file, or question, tuned to the reader's role, skill level, and output budget. Use when the user asks to explain, clarify, or walk through something.
argument-hint: "[-r engineer|pm|business-manager|designer|qa|executive] [-l novice|competent|proficient|expert] [-b bare|lean|normal|verbose] <topic>"
metadata:
  version: "0.1.1"
---

# explain

1. Read `config-rules.md` in this skill's directory. Follow it exactly.
2. Read the config files it lists, parse args, resolve role/level/budget/audience.
3. First line of reply = echo line per rules.
4. Explain the task input per role + level + budget tier rules.
   - Gather only what's needed: targeted reads/searches of referenced code, not whole-repo scans.
   - Depth follows level; length/format follows budget; framing + code inclusion follow role.
   - Audience is irrelevant here (no artifact); still shown in echo line.
5. No task input -> echo line + ask what to explain.
