# Architecture Overview

This document captures the current state of the ProbeTect architecture so new contributors can ramp up quickly.

## High-Level Flow
1. Anonymous visitors land on the marketing site (`blog` app) rendered from `templates/blog/home.html`.
2. Users register or log in through views in the `accounts` app, powered by the custom `User` model with role support.
3. Authenticated users access the dashboard and PDF upload experience (served by `accounts` and `materials`).
4. Uploaded PDFs are validated, stored in Supabase Storage, and tracked via the `Material` model.
5. Students trigger quiz generation from a material card; the system extracts text from Supabase, calls Gemini, and persists questions in the `quizzes` app.
6. Generated quizzes can be taken immediately, scored server-side, and results are rendered back to the user.

## Applications
- **accounts**
  - Extends `AbstractUser` with a `role` enum and helper methods.
  - Provides signup, login (with email aliases), logout, and a lightweight dashboard view.
  - Custom admin registration exposes role management in Django admin.
- **materials**
  - Model: `Material` stores metadata, status, and storage location for each upload.
  - Forms: `MaterialUploadForm` performs file validation with Tailwind-friendly widgets.
  - Views: `MaterialUploadView` coordinates form handling, Supabase integration, flash messaging, and recent uploads list.
  - Supabase helpers: `_get_config`, `upload_file`, `download_file`, and `delete_file` abstract REST calls using environment variables.
- **quizzes**
  - Models: `Quiz` captures quiz metadata, status, Gemini model used, and a link back to `Material`; `QuizQuestion` stores prompts, choices, answers, and explanations.
  - Views: `GenerateQuizView` orchestrates quiz creation, `QuizListView` lists a user's quizzes (optionally filtered per material), and `QuizDetailView` renders the take-and-score flow.
  - Services: `services.py` handles text extraction from PDFs, prompt construction, Gemini API interaction, and JSON parsing with robust error handling.
- **blog**
  - Single `landing` view for the marketing homepage.
  - Templates present product messaging and call-to-actions while sharing the global layout.

## Settings & Configuration
- `mysite/settings.py` loads environment variables via `dotenv`, configures `dj_database_url` for Postgres/Supabase, and declares the custom `AUTH_USER_MODEL`.
- Gemini configuration is sourced from `GEMINI_API_KEY` and `GEMINI_MODEL` (defaulting to `gemini-2.5-flash`).
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
- `quizzes.Quiz`
  - ForeignKey to `User` (owner) and `Material` (source document).
  - Tracks status (`pending`, `processing`, `ready`, `error`), question count, Gemini model, and any error message.
- `quizzes.QuizQuestion`
  - ForeignKey to `Quiz`.
  - Stores the prompt, optional multiple-choice array, canonical answer, explanation, and ordering index.

## AI & External Services
- **Supabase Storage** stores original PDFs; paths and public URLs live on each `Material` record.
- **Gemini 2.5 Flash** powers quiz generation via the `call_gemini` service function. Requests include extracted PDF text, and responses are normalized to strict JSON before persistence.

## Future Directions
- Background workers for long-running quiz generation and progress updates (transitioning quiz status off the request thread).
- Lesson planning features that aggregate quiz results to suggest study sessions.
- Instructor dashboards summarizing class-level quiz performance once sharing controls land.
- Storage lifecycle policies to purge Supabase files when materials or quizzes are deleted.

Keep `DOCS_UPDATES.md` in sync as these areas evolve.
