terraform {
  required_version = ">= 1.6.0"
}

# Placeholder infrastructure for: Local contractor quote comparison tool
# Recommended production shape:
# - Frontend: Vercel project
# - Backend: AWS Lambda + API Gateway, ECS Fargate, or App Runner
# - Database: Neon Postgres, Supabase Postgres, or SQLite only for local/dev
# - Auth: Clerk by default for SaaS, Firebase Auth when Firebase ecosystem is preferred

variable "project_name" {
  type    = string
  default = "local-contractor-quote-comparison-tool"
}
