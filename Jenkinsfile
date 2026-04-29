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
    # Importar Red, Subred y Firewall (Estos ya funcionaron, pero los dejamos por seguridad)
    terraform import -var="project_id=devops-interview-poc-123" google_compute_network.main_vpc projects/devops-interview-poc-123/global/networks/devops-vpc || true
    terraform import -var="project_id=devops-interview-poc-123" google_compute_subnetwork.main_subnet projects/devops-interview-poc-123/regions/us-central1/subnetworks/devops-vpc-subnet || true
    terraform import -var="project_id=devops-interview-poc-123" google_compute_firewall.allow_ssh projects/devops-interview-poc-123/global/firewalls/allow-ssh || true
    
    # CORRECCIÓN AQUÍ: Importar el Clúster de GKE con la ruta completa y limpia
    terraform import -var="project_id=devops-interview-poc-123" google_container_cluster.primary devops-interview-poc-123/us-central1-a/devops-cluster || true
    # 🎯 ÚLTIMA ADICIÓN: Importar el Node Pool
    terraform import -var="project_id=devops-interview-poc-123" google_container_node_pool.primary_nodes devops-interview-poc-123/us-central1-a/devops-cluster/main-node-pool || true		
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

        stage('Build & Push (Cloud Build)') {
            steps {
                echo '📦 Construyendo y subiendo imagen con Google Cloud Build...'
                // Usamos la variable de entorno para la versión si la tienes, o dejamos v7
                sh '''
                    gcloud builds submit ./app \
                        --tag us-central1-docker.pkg.dev/devops-interview-poc-123/app-repo/my-app:v7 \
                        --project=devops-interview-poc-123
                '''
            }
        }

        stage('Deploy to K8s') {
    steps {
        echo '☸️ Desplegando en GKE...'
        sh '''
            # Conexión al clúster
            gcloud container clusters get-credentials devops-cluster --zone us-central1-a --project devops-interview-poc-123
            
            # La ruta real según tu terminal es ./app/k8s/
            kubectl apply -f ./app/k8s/deployment.yaml -n production
            
            # Actualizamos la imagen
            kubectl set image deployment/mi-app-deployment mi-app-container=us-central1-docker.pkg.dev/devops-interview-poc-123/app-repo/my-app:v7 -n production
            
            # Verificamos que los pods suban bien
            kubectl rollout status deployment/mi-app-deployment -n production
        '''
    }
 }
}

    post {
        success { echo "✅ ¡Pipeline Exitoso! Infraestructura y App actualizadas." }
        failure { echo "❌ Fallo en el pipeline. Revisa los logs." }
        always { cleanWs() }
    }
}
