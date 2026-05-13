terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 7.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

resource "google_artifact_registry_repository" "my_repo" {
  project    = var.project_id
  location      = "us-central1"
  repository_id = "app-repo"
  format        = "DOCKER"
}
