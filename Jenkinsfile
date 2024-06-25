
pipeline {
    agent any
   
    
    stages {
        stage('checkout') {
            steps {
               checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'python207', url: 'https://github.com/AlphaEBarcodeERP/jewelretailersbackend.git']])
                echo 'checkout done'
            }
        }
        

        stage('Docker Image') {
            steps {
                
                script{
                    def a=0
                    bat 'docker build . -f dockerfile.txt -t  webjewelretailreportback'
                    a=1
                    if(a>0)
                    {
                         bat 'docker stop  webjewelretailreportback'
                         bat 'docker rm  webjewelretailreportback'
                    }
                }
                echo 'Docker Image done'
            }
        }
        stage('Docker Run') {
            steps {
                script{
                    bat 'docker run -p 62202:62202 -it -v SharedImages:/BackendJewelRWebReport/Utility/Image -v SharePDF:/BackendJewelRWebReport/Utility/PDF -v ShareLogFile:/BackendJewelRWebReport/Utility/Logfile -d --name  webjewelretailreportback  webjewelretailreportback'
                }
                echo 'Docker Running'
            }
        }
        stage('Docker push') {
            steps {
                // script{
                //     bat 'docker login -u patelom0910 -p 09102001Om'
                // }
                echo 'Docker push done'
            }
        }
    }
}