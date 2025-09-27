# ProbeTect

ProbeTect is a Django web application that lets students and instructors upload lecture PDFs, generate AI-powered quizzes, and review results across personalised dashboards.

## Highlights
- **Account roles:** Custom `User` model distinguishes student and instructor experiences.
- **Secure storage:** PDF uploads are pushed to Supabase Storage and tracked with metadata for later processing.
- **Quiz generation:** Gemini reads stored PDFs, produces multiple-choice questions, and the app stores them for immediate practice.
- **Extensible UI:** Tailwind-based templates provide landing, auth, upload, and quiz-taking experiences ready for future analytics.

## Project Layout
```
ProbeTect/
+-- accounts/         # Custom user model, auth flows, dashboard
+-- materials/        # Material model, upload form/view, Supabase helpers
+-- quizzes/          # Quiz models, generation services, list/detail views
+-- blog/             # Marketing landing page
+-- mysite/           # Django project settings and URL routing
+-- templates/        # Site-wide templates (base, auth, upload, quizzes)
+-- static/           # Shared static assets (Tailwind extensions)
+-- docs/             # Extended documentation (architecture notes, etc.)
+-- AGENTS.md         # Automation and agent guidelines
+-- DOCS_UPDATES.md   # Documentation & change log
+-- manage.py         # Django management entrypoint
```
Additional notes live in [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) and [`AGENTS.md`](AGENTS.md).

## Architecture Snapshot
- **Frontend templates:** `templates/base.html` sets the site shell; materials and quiz templates render upload queues, quiz lists, and interactive quiz detail pages.
- **Upload pipeline:** `MaterialUploadView` validates PDFs, routes storage through Supabase (`materials/supabase.py`), and records metadata on `Material`.
- **Quiz pipeline:** `GenerateQuizView` extracts text from Supabase, calls Gemini 2.5 Flash via `quizzes/services.py`, saves `Quiz` and `QuizQuestion` records, and redirects users to take the quiz.
- **Quiz UX:** `QuizListView` shows generated quizzes (filterable per material) while `QuizDetailView` renders questions, collects answers, and computes scores server-side.
- **Configuration:** Environment variables define `DATABASE_URL`, Supabase credentials, and the Gemini model (`gemini-2.5-flash`). See `.env` for local overrides.

## Prerequisites
- Python 3.11 (project virtualenv lives at `.venv/`)
- pip or another Python package manager
- Supabase project with Storage bucket access (service-role key)

### Core dependencies
Install the required packages into your virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
pip install "Django>=4.2,<5.0" python-dotenv dj-database-url pypdf
```

## Environment
Copy `.env.example` (if present) or create `.env` with:

```env
DEBUG=1
DATABASE_URL=postgresql://...
SECRET_KEY=your-secret
ALLOWED_HOSTS=127.0.0.1,localhost
SUPABASE_URL=https://<your-project>.supabase.co
SUPABASE_SERVICE_ROLE_KEY=...
SUPABASE_STORAGE_BUCKET=pdf_uploads
GEMINI_API_KEY=your-google-ai-key
GEMINI_MODEL=gemini-2.5-flash
```

## Database setup
Run migrations after activating the virtualenv:

```bash
python manage.py migrate
```

Seed a superuser for admin access if needed:

```bash
python manage.py createsuperuser
```

## Running the app locally
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` for the marketing landing page. After signing up, the dashboard lives at `/accounts/dashboard/`, the upload workflow at `/materials/upload/`, and generated quizzes under `/quizzes/`.

## Upload & Quiz Flow
1. Authenticated users submit PDFs through `/materials/upload/`.
2. `MaterialUploadForm` validates size (<25 MB) and MIME type.
3. `upload_file()` pushes content to Supabase Storage and returns a path plus public URL.
4. A `Material` record persists metadata, owner, and storage references.
5. Users trigger **Generate quiz** from the queue; `GenerateQuizView` calls Gemini, stores a `Quiz` plus `QuizQuestion` entries, and redirects to the quiz detail page.
6. `QuizDetailView` renders questions, accepts responses, and shows score/feedback once submitted.

## Tests
The repository currently contains placeholder test modules (`accounts/tests.py`, `materials/tests.py`, etc.). Add targeted unit or integration tests as features solidify and run them with:

```bash
python manage.py test
```

## Deployment Notes
- Supabase storage credentials must use a service-role key to allow server-side uploads/deletes.
- Ensure `DEBUG=0` and configure `ALLOWED_HOSTS` before deploying.
- Static assets live in `static/`; collect them with `python manage.py collectstatic` for production.

## Contributing
1. Create a feature branch off `main`.
2. Update or add documentation (including `DOCS_UPDATES.md`).
3. Write tests for new behaviour.
4. Submit a PR with screenshots for front-end changes when possible.

## Documentation tracker
See [`DOCS_UPDATES.md`](DOCS_UPDATES.md) for a running log of documentation changes, release prep notes, and sprint recaps.
