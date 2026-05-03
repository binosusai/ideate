# Deployment

## Recommended POC Deployment
- Frontend: Vercel
- Backend: AWS Lambda + API Gateway, ECS Fargate, or App Runner
- Database: Neon Postgres or Supabase Postgres
- Auth: Clerk for SaaS, Firebase Auth when the Firebase ecosystem is preferred
- Infra: Terraform once cloud resources are selected
- DevOps: GitHub Actions for checks and preview deploys

## Vercel
Deploy `frontend/` as the static site. Configure API routing once the backend target URL exists.

## AWS
Convert `backend/app.py` to Lambda/API Gateway or containerize it for App Runner/ECS.

## Terraform
Use `infra/terraform/main.tf` as the starting point. Do not commit Terraform state.

## Environment Variables
Configure secrets in Vercel, AWS, Clerk, Firebase, Neon, or Supabase dashboards. Do not commit `.env`.
