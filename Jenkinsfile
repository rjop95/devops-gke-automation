pipeline {
    agent any

    environment {
        // Credenciales y Configuración de GCP
        GCP_PROJECT_ID = 'devops-interview-poc-123'
        GCP_CREDS_ID   = 'gcp-creds' // El ID que pusiste en Jenkins Credentials
        CLUSTER_NAME   = 'devops-cluster'
        ZONE           = 'us-central1-a'
        
        // Configuración de Docker/Artifact Registry
        IMAGE_NAME     = 'mi-app-devops'
        REGION         = 'us-central1'
        REPOSITORY     = 'app-repo'
        IMAGE_TAG      = "${env.BUILD_ID}" // Etiqueta única por cada build
    }

    stages {
        stage('Checkout SCM') {
            steps {
                // Clonar el repositorio con los nuevos cambios (docs, tests, etc.)
                checkout scm
            }
        }

        stage('Terraform Infrastructure') {
            steps {
                // Usamos withCredentials para que Terraform tenga acceso a la Service Account
                withCredentials([file(credentialsId: "${GCP_CREDS_ID}", variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    dir('infra') {
                        sh 'terraform init'
                        sh "terraform apply -auto-approve -var='project_id=${GCP_PROJECT_ID}'"
                    }
                }
            }
        }

        stage('Configuración de Acceso (L2 Fix)') {
            steps {
                // Este es el paso que arregla el ConnectTimeoutError
                // Refresca el archivo kubeconfig de Jenkins con la info del clúster recién creado
                withCredentials([file(credentialsId: "${GCP_CREDS_ID}", variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    sh "gcloud auth activate-service-account --key-file=\$GOOGLE_APPLICATION_CREDENTIALS"
                    sh "gcloud container clusters get-credentials ${CLUSTER_NAME} --zone ${ZONE} --project ${GCP_PROJECT_ID}"
                }
            }
        }

        stage('Ansible Setup') {
            steps {
                dir('ansible') {
                    // Ejecutamos el setup de K8s (Namespaces, RBAC, etc.)
                    // Ahora que el contexto de kubectl está fresco, no dará timeout
                    sh 'ansible-playbook k8s_setup.yml'
                }
            }
        }

        stage('Build & Push Docker Image') {
            steps {
                withCredentials([file(credentialsId: "${GCP_CREDS_ID}", variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    sh "cat \$GOOGLE_APPLICATION_CREDENTIALS | docker login -u _json_key --password-stdin https://${REGION}-docker.pkg.dev"
                    
                    dir('app') {
                        sh "docker build -t ${REGION}-docker.pkg.dev/${GCP_PROJECT_ID}/${REPOSITORY}/${IMAGE_NAME}:${IMAGE_TAG} ."
                        sh "docker push ${REGION}-docker.pkg.dev/${GCP_PROJECT_ID}/${REPOSITORY}/${IMAGE_NAME}:${IMAGE_TAG}"
                    }
                }
            }
        }

        stage('Deploy to GKE') {
            steps {
                dir('app/k8s') {
                    // Actualizamos la imagen en el manifiesto y desplegamos
                    sh "sed -i 's|IMAGE_PLACEHOLDER|${REGION}-docker.pkg.dev/${GCP_PROJECT_ID}/${REPOSITORY}/${IMAGE_NAME}:${IMAGE_TAG}|g' deployment.yaml"
                    sh "kubectl apply -f deployment.yaml"
                    // sh "kubectl apply -f service.yml"
                }
            }
        }

stage('Post-Deployment Validation') {
    steps {
        script {
            echo "Esperando a que los Pods estén listos en el namespace production..."
            // Cambiamos 'mi-app-devops' por 'mi-app-deployment'
            sh 'kubectl rollout status deployment/mi-app-deployment -n production --timeout=90s'
        }
    }
}
    }

    post {
        always {
            echo "Limpiando el espacio de trabajo..."
           // cleanWs()
        }
        success {
            echo "✅ Pipeline completado exitosamente. Sistema listo para validación Postman."
        }
        failure {
            echo "❌ Fallo en el pipeline. Iniciando protocolos de revisión de logs (L2 Support Mode)."
        }
    }
}
