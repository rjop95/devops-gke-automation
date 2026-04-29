resource "google_compute_network" "main_vpc" {
  name                    = var.network_name
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "main_subnet" {
  name          = "${var.network_name}-subnet"
  region        = var.region
  network       = google_compute_network.main_vpc.name
  ip_cidr_range = "10.0.1.0/24"
}

# Regla de firewall para permitir SSH (útil para Ansible después)
resource "google_compute_firewall" "allow_ssh" {
  name    = "allow-ssh"
  network = google_compute_network.main_vpc.name

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = ["0.0.0.0/0"]
}
