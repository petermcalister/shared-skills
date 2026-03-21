# Mermaid Syntax Troubleshooting Guide

Common syntax errors and fixes. Check here when mmdc validation fails.

## Quick Fixes

- ✅ Wrap reserved words in double quotes
- ✅ Check for missing `end` keywords in blocks
- ✅ Ensure colons before message text in sequence diagrams
- ✅ Verify arrow syntax (`-->` not `->`)
- ✅ Escape special characters with quotes or HTML entities

---

## Cross-Cutting Issues (All Diagrams)

### 🔴 Error 1: Reserved Words as Identifiers

Reserved: `default`, `style`, `class`, `end`, `subgraph`, `click`, `classDef`, `linkStyle`, `graph`

**Bad:** `start --> end`
**Good:** `start --> "end"`

### 🔴 Error 2: Unescaped Special Characters

Characters needing quotes: `"`, `(`, `)`, `[`, `]`, `{`, `}`, `\`, `:`, `;`, `#`, `%`

**Bad:** `A[Say "hello"]`
**Good:** `A["Say #34;hello#34;"]`

**Rule:** When in doubt, wrap the entire label in double quotes.

### 🟡 Error 3: Invalid classDef Syntax

**Bad:** `classDef myClass { fill: #ff0000; stroke: #333; }`
**Good:** `classDef myClass fill:#ff0000,stroke:#333,color:#fff`

No curly braces. Comma-separated. No semicolons.

### 🟢 Error 4: Empty Comments

**Bad:** `%%` (alone on a line)
**Good:** `%% This is a comment`

---

## Flowchart Errors

### 🔴 Error 5: "end" as Node Name

**Bad:** `start --> end`
**Good:** `start --> endNode["end"]`

### 🔴 Error 6: Wrong Arrow Syntax

**Bad:** `A -> B` or `A => B`
**Good:** `A --> B` or `A ==> B`

### 🟠 Error 7: Subgraph Without end

Every `subgraph` needs a closing `end`:
```
subgraph Group
    A --> B
end
```

### 🟠 Error 8: Node ID Starting with Number

**Bad:** `1node[Label]`
**Good:** `node1[Label]`

### 🟡 Error 9: Semicolons in Labels

**Bad:** `A[Step 1; Step 2]`
**Good:** `A["Step 1; Step 2"]`

### 🟡 Error 10: Parentheses in Labels

**Bad:** `A[Function(x)]`
**Good:** `A["Function(x)"]`

---

## Sequence Diagram Errors

### 🔴 Error 11: Missing Colon Before Message

**Bad:** `A->>B Login request`
**Good:** `A->>B: Login request`

### 🔴 Error 12: Wrong Arrow Types

**Bad:** `A-->B: message` (this is a dotted arrow without response semantics)
**Good:** `A->>B: message` (solid with arrowhead) or `A-->>B: response` (dotted response)

### 🟠 Error 13: Unquoted Participant Names with Spaces

**Bad:** `participant User Service`
**Good:** `participant US as User Service`

### 🟠 Error 14: Semicolons in Messages

**Bad:** `A->>B: Step 1; Step 2`
**Good:** `A->>B: Step 1 and Step 2`

### 🟡 Error 15: Missing activate/deactivate Balance

Every `activate X` needs a matching `deactivate X`.

---

## Class Diagram Errors

### 🟠 Error 16: Wrong Relationship Syntax

**Bad:** `A -> B` or `A -- B`
**Good:** `A --> B` (association), `A <|-- B` (inheritance), `A *-- B` (composition)

### 🟡 Error 17: Missing Return Type

**Bad:** `+methodName()`
**Good:** `+methodName() void` or `+methodName() String`

---

## State Diagram Errors

### 🔴 Error 18: Using `graph` Instead of `stateDiagram-v2`

**Bad:** `stateDiagram`
**Good:** `stateDiagram-v2`

### 🟠 Error 19: Missing [*] for Start/End

Start: `[*] --> FirstState`
End: `LastState --> [*]`

---

## ER Diagram Errors

### 🔴 Error 20: Wrong Cardinality Symbols

**Bad:** `A 1--* B`
**Good:** `A ||--o{ B : "has many"`

Cardinality: `||` (exactly one), `o|` (zero or one), `}|` (one or more), `}o` (zero or more)

### 🟠 Error 21: Missing Relationship Label

**Bad:** `USER ||--o{ ORDER`
**Good:** `USER ||--o{ ORDER : places`

---

## Gantt Chart Errors

### 🟠 Error 22: Wrong Date Format

**Bad:** `01/15/2026`
**Good:** `2026-01-15` (use `dateFormat YYYY-MM-DD`)

### 🟡 Error 23: Missing Section

Tasks must be inside a `section`:
```
section Phase 1
Task 1 :a1, 2026-01-01, 7d
```

### 🟡 Error 24: Task Duration Syntax

**Bad:** `Task :2026-01-01, 7 days`
**Good:** `Task :2026-01-01, 7d`

---

## Pie Chart Errors

### 🟡 Error 25: Missing Title

```
pie title Distribution
    "Category A" : 40
    "Category B" : 60
```

### 🟡 Error 26: Unquoted Labels

**Bad:** `Category A : 40`
**Good:** `"Category A" : 40`

---

## General Errors

### 🟠 Error 27: Mixing Diagram Types

Each code block must contain exactly one diagram type. Don't mix `flowchart` and `sequenceDiagram` in the same block.

### 🟡 Error 28: Trailing Whitespace in Labels

Some parsers choke on trailing spaces. Trim all labels.
