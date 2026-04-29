variable "project_id" {
  description = "ID del proyecto en Google Cloud"
  type        = string
}

variable "region" {
  description = "Región de despliegue"
  type        = string
  default     = "us-central1"
}

variable "zone" {
  description = "Zona específica para el clúster"
  type        = string
  default     = "us-central1-a"
}

variable "network_name" {
  description = "Nombre de la VPC"
  type        = string
  default     = "devops-vpc"
}
