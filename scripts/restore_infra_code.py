import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Contenido de los archivos
main_content = """
resource "google_container_cluster" "primary" {
  name     = "devops-cluster"
  location = "us-central1-a"
  initial_node_count = 1
  remove_default_node_pool = true

  node_config {
    machine_type = "e2-small"
  }
}

resource "google_container_node_pool" "primary_nodes" {
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
  location      = "us-central1"
  repository_id = "app-repo"
  format        = "DOCKER"
}
"""

variables_content = """
variable "project_id" {
  description = "ID del proyecto de GCP"
  default     = "devops-interview-poc-123"
}

variable "region" {
  description = "Región de GCP"
  default     = "us-central1"
}
"""

def restore_all():
    infra_dir = os.path.join(BASE_DIR, 'infra')
    os.makedirs(infra_dir, exist_ok=True)
    
    # Lista de archivos a crear
    files_to_create = {
        'main.tf': main_content,
        'variables.tf': variables_content
    }
    
    for filename, content in files_to_create.items():
        file_path = os.path.join(infra_dir, filename)
        with open(file_path, 'w') as f:
            f.write(content.strip())
        print(f"✅ {filename} restaurado en: {file_path}")

if __name__ == "__main__":
    restore_all()
