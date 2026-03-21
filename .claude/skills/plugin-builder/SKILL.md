---
name: plugin-builder
description: >
  Use when the user asks to build, create, or modify a Claude Code plugin. Trigger on:
  "build a plugin", "create a plugin", "add a command", "add a skill", "add an agent",
  "add a hook", "plugin structure", or when the user wants to extend any plugin with new
  components. Also trigger when troubleshooting plugin loading, skill discovery, or hook
  configuration within a plugin context.
version: 0.2.0
---

# Plugin Builder

Build well-structured Claude Code plugins that match proven patterns.

## Before You Start

If you're in a repo with an existing plugin (look for `.claude-plugin/plugin.json`),
read it first to match its conventions. In the cowork repo, `pete-pa/` is the reference
implementation.

## Plugin Skeleton

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json       # ONLY this file goes here
├── commands/             # User-invoked slash commands
├── skills/               # Auto-activating knowledge
│   └── skill-name/
│       └── SKILL.md
├── references/           # Shared guides (prefer this over per-skill refs/)
├── agents/               # Autonomous subagents
├── hooks/
│   └── hooks.json        # Event-driven automation
├── .mcp.json             # External tool connections
└── README.md
```

Nothing goes inside `.claude-plugin/` except `plugin.json`. This is the one rule
that causes the most confusion — commands, skills, agents all live at the plugin root.

## plugin.json

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "One sentence: what this plugin does",
  "author": { "name": "Pete" }
}
```

`name` becomes the namespace — skills appear as `/plugin-name:skill-name`.

## Deciding What to Build

| User wants... | Build a... |
|--------------|------------|
| A `/slash-command` they type | **Command** (`commands/name.md`) |
| Claude to automatically apply knowledge | **Skill** (`skills/name/SKILL.md`) |
| A task to run in isolated context | **Agent** (`agents/name.md`) |
| Something on file save, session start, etc. | **Hook** (`hooks/hooks.json`) |
| Connection to external API/service | **MCP server** (`.mcp.json`) |

Most plugins need only 1-2 of these.

## Building Commands

Single `.md` files in `commands/`. Write instructions TO Claude, not to the user:

```markdown
---
description: Short text shown in /help
allowed-tools: Read, Grep, Glob, Bash
model: sonnet
---

Do the thing the user asked for. Use $ARGUMENTS as the input.

1. First step
2. Second step
3. Present results
```

Commands typically load a skill, then execute its workflow. Reference resources
via `${CLAUDE_PLUGIN_ROOT}/skills/...` or `${CLAUDE_PLUGIN_ROOT}/references/...`.

## Building Skills

- `SKILL.md` must be exactly that filename (case-sensitive), in a kebab-case folder
- Description says WHAT it does AND WHEN to use it, with trigger phrases
- Keep under 500 lines — move detail into `references/`
- Use imperative form ("Check the code", not "You should check the code")
- For full skill writing guidance, use the `tdd-writing` or `skill-creator` skills

## Building Agents

Agents run in their own context with restricted tools:

```markdown
---
name: my-agent
description: Use this agent when [scenario]. Proactively use for [task type].
model: haiku
tools: Read, Grep, Glob
---

You are a [role]. When invoked:
1. Do this
2. Return findings to the main conversation
```

- **Read-only work** → haiku (fast, cheap)
- **Analysis and design** → sonnet
- Only grant tools the agent actually needs

### Agents Cannot Use MCP Tools

MCP connections only exist in the parent session. Agents **cannot** use browser
automation, external APIs, or any MCP-provided tools. Design accordingly: use agents
for code analysis and file processing, keep MCP-dependent work in skills/commands.

## Building Hooks

```json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/scripts/setup.sh",
        "timeout": 30
      }]
    }]
  }
}
```

Useful events: `SessionStart` (inject context), `PostToolUse` with `Write|Edit`
(auto-format), `PreToolUse` with `Bash` (block dangerous commands), `Stop` (verify work).

Hook types: `command` (shell), `prompt` (single LLM call), `agent` (multi-turn).
Exit codes: `0` = allow, `2` = block.

## Variables

| Variable | Where | Purpose |
|----------|-------|---------|
| `${CLAUDE_PLUGIN_ROOT}` | Everywhere | Absolute path to plugin root |
| `$ARGUMENTS` | Commands/Skills | User input after command name |

## Testing

```bash
claude --plugin-dir ./my-plugin    # Load without installing
claude --debug                      # See what's loading
```

## Common Mistakes

1. **Files inside `.claude-plugin/`** — only plugin.json goes there
2. **Instructions for the user instead of Claude** — commands are prompts Claude executes
3. **Everything in SKILL.md** — use `references/` for detail
4. **Vague descriptions** — "Helps with projects" will never trigger
5. **Agents with all tools** — restrict to what they need
6. **Hardcoded paths** — use `${CLAUDE_PLUGIN_ROOT}`
7. **MCP work in agents** — agents can't access MCP tools
