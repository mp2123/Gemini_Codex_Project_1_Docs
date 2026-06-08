# AGENTS.md - Fake Public Example

This is a sanitized example of project-level agent instructions.

## Mission

Maintain a small analytics dashboard that uses public or synthetic data only.

## Safety Rules

- Do not commit `.env` files.
- Do not print credentials, tokens, or private account data.
- Do not use private employer data.
- Use feature branches for app changes.
- Run verification before committing.

## Verification

Before closeout, run:

```bash
git status --short --branch
git diff --check
npm run lint
npm run build
```

## Closeout

Update:

- `CHANGELOG.md`
- `NEXT_ACTIONS.md`
- any decision docs affected by the work
