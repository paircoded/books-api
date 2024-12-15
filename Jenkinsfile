def config = [
    terraform_dir: './terraform',
]

def app;

pipeline {
    environment {
        BUILD_NUMBER=/${env.BUILD_NUMBER}/
        TERRAFORM_DIR=/${config.terraform_dir}/
    }

    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Terraform Init') {
            steps {
                script {
                   withCredentials([file(credentialsId: 'k8sKubeConfig', variable: 'secretFile')]) {
                        sh '''
                            # god help me if I ever do anything concurrently
                            rm -rf ~/.kube && mkdir ~/.kube && chmod 700 ~/.kube && rm -f ~/.kube/config && ln -s ${secretFile} ~/.kube/config
                            cd ${TERRAFORM_DIR}
                            terraform init -migrate-state
                        '''
                    }
                }
            }
        }

        stage('Helm init') {
            steps {
                script {
                   withCredentials([file(credentialsId: 'k8sKubeConfig', variable: 'secretFile')]) {
                        sh '''
                            # god help me if I ever do anything concurrently
                            rm -rf ~/.kube && mkdir ~/.kube && chmod 700 ~/.kube && rm -f ~/.kube/config && ln -s ${secretFile} ~/.kube/config
                            helm repo add bitnami https://charts.bitnami.com/bitnami
                        '''
                    }
                }
            }
        }

        stage('Terraform Plan') {
            steps {
               withCredentials([file(credentialsId: 'k8sKubeConfig', variable: 'secretFile')]) {
                    sh '''
                        # god help me if I ever do anything concurrently
                        rm -rf ~/.kube && mkdir ~/.kube && chmod 700 ~/.kube && rm -f ~/.kube/config && ln -s ${secretFile} ~/.kube/config
                        cd ${TERRAFORM_DIR}
                        terraform plan -var image_tag="build-${BUILD_NUMBER}"
                       '''
               }
            }
        }

        stage('Build image') {
            steps {
                script {
                    app = docker.build("paircoded-books-api")
                }
            }
        }

        stage('Push image') {
            steps {
                script {
                    docker.withRegistry('https://docker-registry.poorlythoughtout.com', 'docker-registry') {
                        app.push("build-${env.BUILD_NUMBER}")
                        app.push("latest")
                    }
                }
            }
        }

        stage('Helm install') {
            steps {
               withCredentials([file(credentialsId: 'k8sKubeConfig', variable: 'secretFile')]) {
                    sh '''
                        # god help me if I ever do anything concurrently
                        rm -rf ~/.kube && mkdir ~/.kube && chmod 700 ~/.kube && rm -f ~/.kube/config && ln -s ${secretFile} ~/.kube/config
                        helm upgrade -f postgresql.values.yaml books-postgresql bitnami/postgresql --namespace paircoded
                       '''
               }
            }
        }

        stage('Terraform Apply') {
            steps {
               withCredentials([file(credentialsId: 'k8sKubeConfig', variable: 'secretFile')]) {
                    sh '''
                        # god help me if I ever do anything concurrently
                        rm -rf ~/.kube && mkdir ~/.kube && chmod 700 ~/.kube && rm -f ~/.kube/config && ln -s ${secretFile} ~/.kube/config
                        cd ${TERRAFORM_DIR}
                        terraform apply -auto-approve -var image_tag="build-${BUILD_NUMBER}"
                       '''
               }
            }
        }
    }
}

