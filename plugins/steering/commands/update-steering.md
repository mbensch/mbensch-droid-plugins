---
description: Update STEERING.md with new rules, tech stack changes, coding conventions, or architecture constraints. Guides you through the type of change and edits the appropriate section.
---

Update the project's STEERING.md rules. Follow these steps exactly:

## Step 1: Check for STEERING.md

Check if `STEERING.md` exists in the project root using the Read tool.

If it does not exist, stop and tell the user:
> "STEERING.md does not exist yet. Run `/init-steering` first to generate it from your codebase."

If it exists, read its full contents before proceeding.

## Step 2: Ask what kind of update is needed

Use the AskUser tool to ask:

> "What would you like to update in STEERING.md?"

Options:
- Add a "do this" rule (approved pattern, required practice, or convention to follow)
- Add a "don't do this" rule (forbidden pattern, off-limits library, or hard boundary)
- Update the tech stack (add, remove, or change a technology or its version)
- Add or update a coding convention
- Add or update an architecture pattern or constraint
- Update build/test/CI commands
- Update contribution rules
- Something else (free text description)

## Step 3: Gather the specific details

Based on the user's answer, use the AskUser tool to ask for the specific details:

- **"Do" rule**: "What should always be done? Describe the rule concisely. Example: 'All API calls must go through the centralized client in src/lib/api.ts'"
- **"Don't" rule**: "What should never be done? Describe the rule concisely. Example: 'Never use Moment.js -- use date-fns instead'"
- **Tech stack change**: "Describe the change. Example: 'Replace Prisma with Drizzle ORM' or 'Add Redis for caching (ioredis v5)'"
- **Coding convention**: "Describe the convention. Example: 'All React components must use named exports, never default exports'"
- **Architecture pattern**: "Describe the constraint or pattern. Example: 'All business logic must live in service layer files under src/services/, never in route handlers'"
- **Build/test/CI commands**: "What command(s) should be added or updated?"
- **Contribution rules**: "What contribution rule should be added or updated?"
- **Something else**: "Describe what you want to change or add to STEERING.md"

## Step 4: Apply the update

Edit `STEERING.md` to incorporate the change in the most appropriate section:

- "Do" rules that are coding conventions → **Code Style & Linting** or **Architecture & Patterns** section
- "Don't" rules that are forbidden patterns → **Hard Boundaries** section
- "Don't" rules that are off-limits libraries → **Off-Limits Libraries** section
- Tech stack changes → **Tech Stack** table (update the row, add a row, or remove a row)
- Coding conventions → **Code Style & Linting** section
- Architecture patterns → **Architecture & Patterns** section
- Build/test commands → **Build, Test & CI** section
- Contribution rules → **Contribution Rules** section
- Ambiguous rules → use your best judgment about the right section, or add a new section if none fits

If the relevant section does not exist in the current STEERING.md, create it.

When wording rules:
- Be specific and actionable
- For "do" rules: start with an imperative verb ("Use...", "Always...", "Prefer...")
- For "don't" rules: start with "DO NOT" (matching the existing Hard Boundaries style)
- Keep it to one or two sentences

## Step 5: Confirm the change

After editing, report:
- What was changed (the exact text added or modified)
- Which section it was added to
- If any existing rule was replaced or superseded, mention it
