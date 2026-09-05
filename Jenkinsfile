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
                // Clonar el repositorio con los nuevos cambios
                checkout scm
            }
        }

        stage('Terraform Infrastructure') {
            steps {
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
                withCredentials([file(credentialsId: "${GCP_CREDS_ID}", variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    sh "gcloud auth activate-service-account --key-file=\$GOOGLE_APPLICATION_CREDENTIALS"
                    sh "gcloud container clusters get-credentials ${CLUSTER_NAME} --zone ${ZONE} --project ${GCP_PROJECT_ID}"
                }
            }
        }

        stage('Ansible Setup') {
            steps {
                dir('ansible') {
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
                // 1. Crear/Actualizar el secreto de Kubernetes para la base de datos de forma segura
                sh '''
                    kubectl create secret generic db-secret \
                      --from-literal=password='password' \
                      --namespace=production \
                      --dry-run=client -o yaml | kubectl apply -f -
                '''

                // 2. Modificamos el archivo usando su ruta absoluta en el workspace
                sh "sed -i 's|IMAGE_PLACEHOLDER|us-central1-docker.pkg.dev/devops-interview-poc-123/app-repo/mi-app-devops:${BUILD_NUMBER}|g' app/k8s/deployment.yaml"

                // 3. Aplicamos de golpe toda la carpeta de Kubernetes
                sh "kubectl apply -f app/k8s/"
            }
        }

        stage('Post-Deployment Validation') {
            steps {
                script {
                    try {
                        echo "Esperando a que los Pods estén listos en el namespace production..."
                        sh 'kubectl rollout status deployment/mi-app-deployment -n production --timeout=120s'
                    } catch (Exception e) {
                        sh 'kubectl get pods -n production'
                        sh 'kubectl describe deployment mi-app-deployment -n production'
                        error "Fallo en la validación: El despliegue no se completó."
                    }
                }
            }
        }
    } // Fin de stages

    post {
        always {
            echo "Limpiando el espacio de trabajo..."
            deleteDir()
        }
        success {
            echo "✅ ¡Despliegue exitoso!"
        }
        failure {
            echo "❌ Fallo en el pipeline. Iniciando protocolos de revisión de logs."
        }
    }
}
