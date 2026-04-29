output "kubernetes_cluster_name" {
  value = google_container_cluster.primary.name
}

output "network_id" {
  value = google_compute_network.main_vpc.id
}
