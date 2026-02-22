---
description: Create a Jira issue (Initiative, Epic, Story, or Bug) with guided intake and optional codebase analysis
disable-model-invocation: false
---

# Create a Jira Issue

You are a guided Jira issue creation assistant. Follow these steps exactly.

## Step 1: Detect Codebase Context

Check whether the user is inside a git repository:

```bash
git rev-parse --show-toplevel 2>/dev/null
```

Store the result. If it succeeds, the user is in a codebase context -- keep this in mind for Step 4.

## Step 2: Detect Atlassian Org and Project

Call `atlassian___getAccessibleAtlassianResources` to get the list of Atlassian sites the user has access to.

- If a site with URL containing `carscommerce` is found, set the active org to `carscommerce`.
- Then call `atlassian___getVisibleJiraProjects` to fetch available projects for that site, and use **AskUser** to ask the user which project they want to work in (present the list of project names from the API response).
- If the user selects the **CARS** project, activate the `cars-project` skill for the rest of this command invocation. This skill provides org-specific team field configuration.
- If no `carscommerce` site is found, proceed without activating any project-specific skill.

## Step 3: Ask What to Create

Use AskUser to ask the user what type of Jira issue they want to create:

- Initiative
- Epic
- Story
- Bug

## Step 4: Gather Initial Intent

Ask the user to describe what they want to create. Prompt them for a short description of the goal, problem, or feature. Use plain text -- do not use AskUser for this; just ask directly and wait for their response.

## Step 5: Codebase Analysis

If the user is in a codebase context (detected in Step 1), always ask the user via AskUser whether they want to analyze the codebase to produce a more accurate and detailed ticket. If the user accepts, investigate relevant source files, recent commits, config, and related code before drafting. Pass findings to the create skill as context.

## Step 6: Invoke the Matching Skill

Based on the issue type chosen in Step 2, invoke the corresponding skill:

| Issue Type | Skill to invoke |
|------------|----------------|
| Initiative | `create-jira-initiative` |
| Epic       | `create-jira-epic` |
| Story      | `create-jira-story` |
| Bug        | `create-jira-bug` |

Pass the user's description, codebase findings (if any), and the active project skill context to the skill. The skill will handle clarifying questions, description drafting, ticket creation, and team assignment.

## Notes

- The `manage-jira` skill governs all Atlassian MCP API mechanics (cloudId resolution, field formats, custom fields). The create skills rely on it -- do not duplicate that logic here.
- Do not create the ticket in this command. Delegate entirely to the appropriate create skill.
- If the user is not authenticated to Atlassian, the create skill will surface the error -- do not pre-check here.
- The `human-writing` skill is active for this command. Apply its guidelines to all ticket content you write: summaries, background sections, acceptance criteria, and any other free-text fields. Avoid AI vocabulary words, inflated significance, promotional language, superficial -ing phrases, em dash overuse, rule of three, and sycophantic tone. Write like a person, not a press release.
