# Architecture

## POC Goal
Demonstrate `Local contractor quote comparison tool` with a simple browser workflow and a local backend API.

## Components
- `frontend/`: static HTML/CSS/JavaScript
- `backend/`: Python stdlib HTTP API
- `poc.sqlite3`: local runtime database, ignored by git
- `infra/`: Terraform placeholders for production resources
- `.github/workflows/`: CI checks

## Production Upgrade Path
Replace SQLite with Neon or Supabase Postgres, add Clerk or Firebase Auth, deploy frontend to Vercel, and deploy backend to AWS.
