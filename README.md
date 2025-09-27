# ProbeTect

ProbeTect is a Django web application that lets students and instructors upload lecture PDFs and turn them into quiz-ready study material. 

## Highlights
- **Account roles:** Custom `User` model distinguishes student and instructor experiences.
- **Secure storage:** PDF uploads are pushed to Supabase Storage and tracked with metadata for later processing.
- **Upload workflow:** Form validation guards file type and size, while the interface surfaces recent uploads and status updates.
- **Extensible UI:** Tailwind-based templates provide a landing page, auth flows, and a dashboard placeholder for future quiz analytics.

## Project Layout
```
ProbeTect/
├── accounts/        # Custom user model, auth flows, dashboard
├── materials/       # Material model, upload form/view, Supabase helpers
├── blog/            # Marketing landing page and homepage plumbing
├── mysite/          # Django project settings and URL routing
├── templates/       # Site-wide templates (base, auth, upload, landing, dashboard)
├── static/          # Shared static assets (Tailwind extensions)
├── docs/            # Extended documentation (architecture notes, etc.)
├── AGENTS.md        # Automation and agent guidelines
├── manage.py        # Django management entrypoint
└── DOCS_UPDATES.md  # Living documentation changelog (see below)
```
Additional notes live in [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) and [`AGENTS.md`](AGENTS.md).

## Prerequisites
- Python 3.11 (project virtualenv lives at `.venv/`)
- pip or another Python package manager
- Supabase project with Storage bucket access (service-role key)

### Core dependencies
The app relies on a small set of packages:
- Django 4.2.x
- `python-dotenv` for loading environment variables from `.env`
- `dj-database-url` for parsing `DATABASE_URL`

Install them into your virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
pip install "Django>=4.2,<5.0" python-dotenv dj-database-url
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
Visit `http://127.0.0.1:8000/` for the marketing landing page. After signing up, the dashboard lives at `/accounts/dashboard/`, and the upload workflow sits at `/materials/upload/` (requires authentication).

## Upload & Processing Flow
1. Authenticated users submit PDFs through `/materials/upload/`.
2. `MaterialUploadForm` validates size (<25 MB) and MIME type.
3. `SupabaseStorage.upload_file` stores the file in Supabase and returns a public URL.
4. A `Material` record persists metadata (owner, title, subject, visibility, etc.).
5. The dashboard and upload page list recent materials and their processing status (`uploaded`, `processing`, `ready`).

Downstream quiz generation will consume the stored metadata and Supabase URLs to build question banks (planned in upcoming iterations).

## Tests
The repository currently contains placeholder test modules (`accounts/tests.py`, `materials/tests.py`, etc.). As features solidify, add targeted unit or integration tests and run them with:

```bash
python manage.py test
```

## Deployment Notes
- Supabase storage credentials must use a service-role key to allow server-side uploads/deletes.
- Ensure `DEBUG=0` and configure `ALLOWED_HOSTS` before deploying.
- Static assets are served from `static/`; collect them with `python manage.py collectstatic` when preparing for production.

## Contributing
1. Create a feature branch off `main`.
2. Update or add documentation (including `DOCS_UPDATES.md`).
3. Write tests for new behaviour.
4. Submit a PR with screenshots or screencasts for front-end changes when possible.

## Documentation tracker
See [`DOCS_UPDATES.md`](DOCS_UPDATES.md) for a running log of documentation changes, release prep notes, and sprint recaps.



## AI Quiz Generation

Install the PDF and Gemini helpers and set the environment variables:

```bash
pip install pypdf
```

```env
GEMINI_API_KEY=your-google-ai-key
GEMINI_MODEL=gemini-2.0-flash
```

After migrating (`python manage.py migrate`), upload a PDF and use the *Generate quiz* button on the materials page.