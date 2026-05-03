# Draft POC: Local contractor quote comparison tool

This is a complete proof-of-concept package for `Local contractor quote comparison tool`.

## What Is Included
- Static frontend in `frontend/`
- Python stdlib backend API in `backend/`
- SQLite local persistence generated at runtime
- Terraform placeholders in `infra/terraform/`
- GitHub Actions checks in `.github/workflows/poc-ci.yml`
- Local setup and deployment docs in `docs/`

## Run Locally

```bash
python3 backend/app.py
```

Then open `http://localhost:8000`.
