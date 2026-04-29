resource "google_container_cluster" "primary" {
  name     = "devops-cluster"
  location = var.zone

  network    = google_compute_network.main_vpc.name
  subnetwork = google_compute_subnetwork.main_subnet.name

  remove_default_node_pool = true
  initial_node_count       = 1
  deletion_protection      = false
}

resource "google_container_node_pool" "primary_nodes" {
  name       = "main-node-pool"
  location   = var.zone
  cluster    = google_container_cluster.primary.name
  node_count = 1

  node_config {
    preemptible  = true # Ahorra costos en prácticas
    machine_type = "e2-medium"

    labels = {
      env = "dev"
    }

    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}
