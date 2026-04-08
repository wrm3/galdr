# g-constraint-add

Add a new architectural constraint to `.galdr/CONSTRAINTS.md`.

## When to use

Run this command when you want to formalize a new non-negotiable architectural rule for the project. New constraints should be rare — they are permanent guardrails, not preferences.

## Steps

1. Read `g-skl-constraints` skill
2. Run the **ADD** operation

## Process

The skill will:
1. Assign the next sequential C-ID
2. Prompt for name, rationale, applies-to, in-practice rules, violation examples, enforcement
3. Update `## Constraint Index` table
4. Add full `## Constraint Definitions` block
5. Append entry to `## Change Log`

## Usage

```
@g-constraint-add
```

Or with context:
```
@g-constraint-add — All SQL queries must use parameterized statements, never string formatting
```
