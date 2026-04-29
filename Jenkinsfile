pipeline {
    agent any

    environment {
        PROJECT_ID = 'devops-interview-poc-123'
        REGION     = 'us-central1'
        REPO_NAME  = 'app-repo'
        IMAGE_NAME = 'my-app'
        CLUSTER    = 'devops-cluster'
        ZONE       = 'us-central1-a'
    }

    stages {
        stage('Audit & Prep') {
            steps {
                echo "🔍 Verificando herramientas..."
                sh 'terraform --version'
                sh 'ansible --version'
                sh 'gcloud --version'
            }
        }

        // --- NUEVA ETAPA: INFRAESTRUCTURA ---
stage('Infrastructure (IaC)') {
    steps {
        echo '🏗️ Sincronizando e implementando infraestructura...'
        dir('infra') {
            sh 'terraform init'
            
            sh '''
                # Importar Red y Subred
                terraform import -var="project_id=devops-interview-poc-123" google_compute_network.main_vpc projects/devops-interview-poc-123/global/networks/devops-vpc || true
                terraform import -var="project_id=devops-interview-poc-123" google_compute_subnetwork.main_subnet projects/devops-interview-poc-123/regions/us-central1/subnetworks/devops-vpc-subnet || true
                
                # Importar Firewall
                terraform import -var="project_id=devops-interview-poc-123" google_compute_firewall.allow_ssh projects/devops-interview-poc-123/global/firewalls/allow-ssh || true
                
                # Importar el Clúster de GKE (Esto es clave)
                terraform import -var="project_id=devops-interview-poc-123" google_container_cluster.primary projects/devops-interview-poc-123/zones/us-central1-a/clusters/devops-cluster || true
            '''
            
            sh 'terraform apply -auto-approve -var="project_id=devops-interview-poc-123"'
        }
    }
}
        // --- NUEVA ETAPA: CONFIGURACIÓN ---
        stage('Configuration (Ansible)') {
            steps {
                echo "⚙️ Configurando dependencias del clúster..."
                dir('ansible') {
                    // Usamos el playbook que creamos hoy para K8s
                    sh 'ansible-playbook k8s_setup.yml'
                }
            }
        }

        stage('Docker Build') {
            steps {
                echo "📦 Construyendo Imagen: v${env.BUILD_ID}"
                // Asegúrate de que la carpeta ./app exista en tu repo
                sh "docker build -t ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${IMAGE_NAME}:v${env.BUILD_ID} ./app"
            }
        }

        stage('Push to Artifact Registry') {
            steps {
                sh "gcloud auth configure-docker ${REGION}-docker.pkg.dev --quiet"
                sh "docker push ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${IMAGE_NAME}:v${env.BUILD_ID}"
            }
        }

        stage('Deploy to K8s') {
            steps {
                echo "☸️ Desplegando en GKE..."
                sh "gcloud container clusters get-credentials ${CLUSTER} --zone ${ZONE} --project ${PROJECT_ID}"
                
                // Actualizamos la imagen en el deployment
                sh "kubectl set image deployment/mi-app-deployment mi-app-container=${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${IMAGE_NAME}:v${env.BUILD_ID} -n production"
                
                sh "kubectl rollout status deployment/mi-app-deployment -n production"
            }
        }
    }

    post {
        success { echo "✅ ¡Pipeline Exitoso! Infraestructura y App actualizadas." }
        failure { echo "❌ Fallo en el pipeline. Revisa los logs." }
        always { cleanWs() }
    }
}
