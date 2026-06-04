# Project Skills

This directory contains project-specific agent skills for the Three Body
Simulation project.

Each skill is a subdirectory containing a `SKILL.md` file with YAML
frontmatter. Skills are automatically discovered and loaded by agents
configured with this directory in their `skills_paths`.

## Creating a New Skill

After completing a reusable multi-step workflow, ask the agent:
"Turn our last workflow into a skill" or use the workflow-skill-creator.

## Skill Structure

```
skills/
└── my-skill-name/
    ├── SKILL.md          # Required: Instructions with YAML frontmatter
    ├── scripts/          # Optional: Helper scripts
    └── references/       # Optional: Reference documentation
```
