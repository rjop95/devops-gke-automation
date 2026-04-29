resource "google_container_cluster" "primary" {
  project    = var.project_id
  name     = "devops-cluster"
  location = "us-central1-a"
  initial_node_count = 1
  remove_default_node_pool = true
  deletion_protection = false
  node_config {
    machine_type = "e2-small"
  }
}

resource "google_container_node_pool" "primary_nodes" {
  project    = var.project_id
  name       = "my-node-pool"
  location   = "us-central1-a"
  cluster    = google_container_cluster.primary.name
  node_count = 1

  node_config {
    preemptible  = true
    machine_type = "e2-small"
  }
}

resource "google_artifact_registry_repository" "app_repo" {
  project    = var.project_id
  location      = "us-central1"
  repository_id = "app-repo"
  format        = "DOCKER"
}
