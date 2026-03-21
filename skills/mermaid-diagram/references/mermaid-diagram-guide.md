# Mermaid Diagram Type Reference

## Diagram Type Selection

| Type | Keyword | Use For |
|------|---------|---------|
| `flowchart` | `flowchart TD/LR` | Processes, decision trees, workflows |
| `sequenceDiagram` | `sequenceDiagram` | API calls, service interactions, protocols |
| `classDiagram` | `classDiagram` | OOP design, data models, relationships |
| `erDiagram` | `erDiagram` | Database schemas, entity relationships |
| `stateDiagram-v2` | `stateDiagram-v2` | State machines, lifecycles |
| `C4Context` | `C4Context` | System context, container views |
| `gantt` | `gantt` | Project timelines, schedules |
| `journey` | `journey` | User journeys, experience maps |
| `mindmap` | `mindmap` | Brainstorming, concept hierarchies |
| `pie` | `pie` | Proportional data |

## Flowchart

```mermaid
flowchart TD
    A[Start] -->|"input"| B{Decision}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E[End]
    D --> E
```

**Direction**: `TD` (top-down), `LR` (left-right), `BT`, `RL`
**Shapes**: `[rect]`, `(round)`, `{diamond}`, `([stadium])`, `[[subroutine]]`, `[(cylinder)]`, `((circle))`
**Links**: `-->`, `---`, `-.->`, `==>`, `--text-->`, `-->|text|`

## Sequence Diagram

```mermaid
sequenceDiagram
    participant C as Client
    participant S as Server
    participant DB as Database
    C->>S: POST /api/login
    activate S
    S->>DB: SELECT user
    DB-->>S: user record
    S-->>C: 200 OK + JWT
    deactivate S
```

**Arrows**: `->>` (solid), `-->>` (dotted), `-x` (cross), `-)` (async)
**Blocks**: `loop`, `alt/else`, `opt`, `par/and`, `critical`, `break`

## Class Diagram

```mermaid
classDiagram
    class Animal {
        +String name
        +int age
        +makeSound() void
    }
    class Dog {
        +fetch() void
    }
    Animal <|-- Dog : inherits
```

**Relations**: `<|--` (inherit), `*--` (composition), `o--` (aggregation), `-->` (association), `..>` (dependency)

## ER Diagram

```mermaid
erDiagram
    USER ||--o{ ORDER : places
    ORDER ||--|{ LINE_ITEM : contains
    PRODUCT ||--o{ LINE_ITEM : "ordered in"
    USER {
        int id PK
        string name
        string email UK
    }
```

**Cardinality**: `||` (one), `o|` (zero or one), `}|` (one or more), `}o` (zero or more)

## State Diagram

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Processing : submit
    Processing --> Success : complete
    Processing --> Error : fail
    Error --> Idle : retry
    Success --> [*]
```

## C4 Context

```mermaid
C4Context
    title System Context
    Person(user, "User", "End user")
    System(app, "Application", "Main system")
    System_Ext(ext, "External API", "Third party")
    Rel(user, app, "Uses")
    Rel(app, ext, "Calls")
```

## Gantt Chart

```mermaid
gantt
    title Project Timeline
    dateFormat YYYY-MM-DD
    section Phase 1
    Design    :a1, 2026-01-01, 14d
    Implement :a2, after a1, 21d
    section Phase 2
    Test      :b1, after a2, 14d
    Deploy    :b2, after b1, 7d
```

## High-Contrast Styling (Required)

Always add these classDef styles for accessibility:

```
classDef default fill:#E8F4FD,stroke:#1B4F72,stroke-width:2px,color:#1B4F72
classDef highlight fill:#D4EFDF,stroke:#1E8449,stroke-width:2px,color:#1E8449
classDef warning fill:#FDEBD0,stroke:#B9770E,stroke-width:2px,color:#B9770E
classDef error fill:#FADBD8,stroke:#C0392B,stroke-width:2px,color:#C0392B
```
