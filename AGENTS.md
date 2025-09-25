# AGENTS.md - Working Agreements for ProbeTect

This file sets the ground rules for agents and contributors operating in this repository. Unless a deeper `AGENTS.md` overrides them, these instructions apply to the entire project.

## Repository Layout

- `mysite/` – Django project settings, URLs, and ASGI/Wsgi configuration
- `accounts/` – Custom user model, auth flows, and dashboard view logic
- `materials/` – Material model, upload form/view, Supabase integration helpers
- `blog/` – Public landing page views
- `templates/` – Shared HTML templates (base layout, auth screens, upload, marketing)
- `static/` – Tailwind-driven CSS assets
- `docs/` – Architecture notes and other reference guides
- `README.md` / `DOCS_UPDATES.md` / `AGENTS.md` – Entry points for onboarding and process updates

## General Principles

- Keep changes focused; prefer incremental PRs over sweeping rewrites.
- Mirror existing Django patterns (CBVs, forms, models) before inventing new abstractions.
- Update documentation whenever behaviour, configuration, or dependencies change.
- Treat environment variables as secrets—never hardcode credentials or copy real keys into commits.
- Use descriptive names; avoid single-letter identifiers outside of simple comprehensions.

## Backend Conventions (Django)

- Python 3.11+, Django 4.2 LTS; respect typing already present (`from __future__ import annotations`).
- Models live beside their app logic; ensure migrations accompany schema changes.
- Views favour class-based implementations with `LoginRequiredMixin` where authentication is required.
- Forms handle validation; keep view logic thin and surface friendly error messages via Django messages.
- Supabase interactions go through `materials/supabase.py`; do not embed storage calls elsewhere.
- URLs: namespaced per app (`materials:upload`, etc.); keep reverse names stable.
- Templates extend `base.html` and use Tailwind utility classes already in place.

## Documentation Rules

- Record every meaningful change in `DOCS_UPDATES.md` (date, author, summary, impacted docs/code).
- Keep `README.md` accurate for setup (venv, migrations, runserver).
- Expand `docs/` (e.g., architecture, process) when introducing new subsystems like quiz generation or background workers.

## Code Style

- Follow existing formatting (black-compatible spacing, trailing commas where appropriate).
- Prefer dataclasses only if they integrate cleanly with Django; otherwise stick with models and plain classes.
- Add concise comments only when code is non-obvious (e.g., Supabase edge cases).
- Tests: add or extend `tests.py` within each app and run them via Django’s test runner.

## Dependency Management

- Manage Python packages via the project virtualenv. Document new runtime deps in `README.md` and pin them in the chosen dependency file (`requirements.txt` when introduced).
- Avoid bringing in heavy libraries without buy-in; prefer standard Django utilities first.
- For Supabase or third-party integrations, surface required env vars in `.env` guidance.

## PR / Change Checklist

- [ ] Logic follows the structure above (apps, forms, views, supabase helpers)
- [ ] Tests updated or added where behaviour changes
- [ ] Docs touched (`DOCS_UPDATES.md`, README, or `docs/` entries)
- [ ] Supabase usage stays within `materials/supabase.py` helpers
- [ ] Lint/test commands (`python manage.py check`, `python manage.py test`) considered when applicable

## IMPORTANT — Execution Rules (ProbeTect)

Avoid long-running servers unless explicitly required.
Do **NOT** run:

- `python manage.py runserver` (ask first if live testing is necessary)
- `celery -A` or any worker/beat commands
- File watchers such as `npm run dev` (no frontend dev server here, but avoid analogous tools)

Allowed commands (safe, complete quickly):

Backend checks/tests:

- `python manage.py check`
- `python manage.py test`
- `python manage.py makemigrations --check --dry-run`

Utility scripts:

- `python manage.py migrate` (only when schema changes are intentional)
- `python manage.py shell -c "..."` for short, non-interactive tasks if needed

If a background service is required, coordinate with the team and provide a reversible plan before starting it.

---

Higher-level directories may define additional rules in nested `AGENTS.md` files; those local instructions take precedence within their scope. Keep this document up to date as workflows evolve.
