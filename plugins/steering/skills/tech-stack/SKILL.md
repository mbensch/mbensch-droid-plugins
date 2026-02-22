---
name: tech-stack-steering
description: Technology stack constraints and coding rules from STEERING.md. Auto-loaded when making technology choices, adding dependencies, proposing architectural changes, or writing code. Enforces what frameworks, libraries, and patterns are approved.
user-invocable: false
---

# Tech Stack Steering

You MUST read `STEERING.md` in the project root and consult its constraints before:
- Adding any new dependency or library
- Proposing a library swap or alternative approach
- Choosing a new implementation pattern
- Suggesting an architecture change
- Writing code that touches tooling, build, or CI configuration

## Non-Negotiable Rules

The constraints in STEERING.md are non-negotiable. They override any suggestion you might have based on general knowledge or best practices, unless the user explicitly decides to update STEERING.md first via `/update-steering`.

## Dependency Approval Process

Before suggesting ANY new dependency:
1. Check if the functionality already exists in the approved tech stack in STEERING.md
2. Check if native language features can handle it without a dependency
3. Only if a new dependency is truly necessary, state explicitly:
   - What it does
   - Why the existing approved stack cannot handle it
   - Its maintenance status and popularity
4. Wait for explicit user approval before adding it

## When STEERING.md Does Not Exist

If `STEERING.md` does not exist in the project root, suggest the user run `/init-steering` to generate it from the codebase automatically.
