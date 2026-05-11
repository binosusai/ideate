terraform {
  required_version = ">= 1.6"
  required_providers {
    neon = {
      source  = "kislerdm/neon"
      version = "~> 0.6"
    }
  }
  # State is stored locally in terraform.tfstate (gitignored).
  # Terraform only needs to run locally when changing infrastructure.
  # GitHub Actions (daily.yml) connects directly via DATABASE_URL — it never runs Terraform.
}

provider "neon" {
  api_key = var.neon_api_key
}

# -------------------------------------------------------------------
# Neon Postgres — uses the shared platform module
# -------------------------------------------------------------------
module "neon" {
  source = "../../../platform/terraform-modules/neon-postgres"

  project_name  = "ideate"
  branch_name   = "main"
  database_name = "ideate"
  role_name     = "ideate_app"
  # Find this at console.neon.tech → Organization Settings → Organization ID
  org_id        = var.neon_org_id
}

# -------------------------------------------------------------------
# Outputs — copy connection_uri to GitHub Actions secret DATABASE_URL
# -------------------------------------------------------------------
output "database_url" {
  value       = module.neon.connection_uri
  sensitive   = true
  description = "Postgres connection string — set this as the DATABASE_URL GitHub Actions secret."
}

variable "neon_org_id" {
  type        = string
  description = "Neon organization ID. Find it at console.neon.tech → Organization Settings."
}

variable "neon_api_key" {
  type        = string
  description = "Neon API key from console.neon.tech → Account Settings → API Keys."
  sensitive   = true
}
