pipeline {
    agent any

    environment {
        // --- CONFIGURACIÓN DE GOOGLE CLOUD ---
        PROJECT_ID = 'devops-interview-poc-123'
        REGION     = 'us-central1'
        REPO_NAME  = 'app-repo'
        IMAGE_NAME = 'my-app'
        CLUSTER    = 'devops-cluster'
        ZONE       = 'us-central1-a'
    }

    stages {
        stage('Audit Environment') {
            steps {
                echo "🔍 Verificando herramientas en el Host..."
                sh 'python3 --version'
                sh 'docker --version'
                sh 'gcloud --version'
            }
        }

        stage('Docker Build') {
            steps {
                echo "🏗️ Construyendo Imagen: v${env.BUILD_ID}"
                sh "docker build -t ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${IMAGE_NAME}:v${env.BUILD_ID} ./app"
            }
        }

        stage('Push to Artifact Registry') {
            steps {
                echo "🚀 Subiendo imagen a Google Cloud..."
                sh "gcloud auth configure-docker ${REGION}-docker.pkg.dev --quiet"
                sh "docker push ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${IMAGE_NAME}:v${env.BUILD_ID}"
            }
        }

        stage('Deploy to K8s') {
            steps {
                echo "☸️ Actualizando GKE..."
                sh "gcloud container clusters get-credentials ${CLUSTER} --zone ${ZONE} --project ${PROJECT_ID}"
                
                // --- NOMBRE DEL CONTENEDOR CORRECTO: mi-app-container ---
                sh "kubectl set image deployment/mi-app-deployment mi-app-container=${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${IMAGE_NAME}:v${env.BUILD_ID}"
                
                sh "kubectl rollout status deployment/mi-app-deployment"
            }
        }
    }

    post {
        success {
            echo "✅ ¡Pipeline Exitoso! Aplicación desplegada en GKE."
        }
        failure {
            echo "❌ El pipeline falló. Revisa los logs para más detalle."
        }
        always {
            echo "🧹 Limpiando espacio de trabajo..."
            cleanWs()
        }
    }
}
