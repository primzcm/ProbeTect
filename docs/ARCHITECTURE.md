# Architecture Overview

This document captures the current state of the ProbeTect architecture so new contributors can ramp up quickly.

## High-Level Flow
1. Anonymous visitors land on the marketing site (`blog` app) rendered from `templates/blog/home.html`.
2. Users register or log in through views in the `accounts` app, powered by the custom `User` model with role support.
3. Authenticated users access the dashboard and upload pages (served by `accounts` and `materials`).
4. PDF uploads are validated, stored in Supabase Storage, and tracked via the `Material` model for later quiz processing.

## Applications
- **accounts**
  - Extends `AbstractUser` with a `role` enum and helper methods.
  - Provides signup, login (with email aliases), logout, and a lightweight dashboard view.
  - Custom admin registration exposes role management in Django admin.
- **materials**
  - Model: `Material` stores metadata, status, and storage location for each upload.
  - Forms: `MaterialUploadForm` performs file validation and handles Tailwind widgets.
  - Views: `MaterialUploadView` coordinates form handling, Supabase integration, flash messaging, and recent uploads list.
  - Supabase helpers: `_get_config`, `upload_file`, and `delete_file` abstract REST calls using environment variables.
- **blog**
  - Single `landing` view for the marketing homepage.
  - Templates present product messaging and call-to-actions while sharing the global layout.

## Settings & Configuration
- `mysite/settings.py` loads environment variables via `dotenv`, configures `dj_database_url` for Postgres/Supabase, and declares the custom `AUTH_USER_MODEL`.
- Static assets: `STATICFILES_DIRS` points to `static/` for Tailwind CSS overrides. Use `collectstatic` during deployment.
- Media uploads: handled externally through Supabase; local `MEDIA_ROOT` exists for future use.

## Data Model Snapshot
- `accounts.User`
  - Inherits built-in username/email auth fields.
  - Adds `role` (`student` or `instructor`) to drive conditional UI and permissions.
- `materials.Material`
  - ForeignKey to `User` (owner).
  - Metadata fields: `title`, `subject`, `description`, `visibility`, `status`, file properties, timestamps.
  - `save()` auto-populates `storage_path` and title fallback from `original_filename`.

## Future Directions
- **Quiz generation pipeline:** consume Supabase URLs and persist generated questions linked to `Material` records.
- **Processing statuses:** background workers can update `status` (`uploaded` → `processing` → `ready`).
- **Instructor features:** dashboards that summarise class-level performance when quiz data becomes available.
- **Deletion lifecycle:** extend `delete_file` usage so removing a `Material` also purges Supabase storage.

Keep `DOCS_UPDATES.md` in sync as these areas evolve.
