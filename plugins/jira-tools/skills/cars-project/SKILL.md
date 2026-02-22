---
name: cars-project
version: 1.0.0
user-invocable: false
description: |
  CARS project-specific configuration for the carscommerce.atlassian.net org.
  Activated automatically by /jira-create when the user is working in the CARS project.
  Provides team field setup and UUID resolution instructions specific to carscommerce.
---

# CARS Project Configuration

This skill is activated by `/jira-create` when the authenticated user's Atlassian site is `carscommerce.atlassian.net` and the user selects the CARS project. It governs how team fields are set on newly created tickets in this org.

## Team Field

In the carscommerce org, the team custom field ID is `customfield_11100`.

### Resolving a Team UUID

To find the UUID for a given team, fetch an existing ticket that already belongs to that team:

```
atlassian___getJiraIssue(cloudId, issueIdOrKey: "CARS-<existing-ticket>")
```

Look at the `customfield_11100` field in the response. The value is the team UUID (a plain string, not wrapped in an object).

### Setting the Team

After creating the ticket, set the team via `atlassian___editJiraIssue`:

```
atlassian___editJiraIssue(
  cloudId,
  issueIdOrKey: "CARS-<new-ticket>",
  fields: {"customfield_11100": "<team-uuid>"}
)
```

Pass the UUID as a plain string. Do **not** wrap it in `{"id": "..."}` -- that returns a 400 error.

### Determining Which Team to Use

1. If the ticket has a parent, fetch the parent and read its `customfield_11100`.
   - If set, offer the user the option to inherit the parent's team or specify a different one via AskUser.
   - If not set, ask the user which team should own this ticket.
2. If there is no parent, ask the user which team should own this ticket.
