terraform {
     backend "gcs" {
       bucket = "devops-interview-poc-123-tfstate"
       prefix = "terraform/state"
     }
   }
