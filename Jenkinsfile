pipeline {
    agent any
    
    environment {
        // This is the ID of your Username/Password credential in Jenkins
        XRAY_CREDS_ID = 'xray-cloud-creds'
        
        // Your specific Jira Test Execution Key
        TEST_EXEC_KEY = 'LOGI-70'
        
        // The 'Configuration Alias' you set in Manage Jenkins > System
        JIRA_INSTANCE = 'JIRA_INSTANCE'
    }

    stages {
        stage('Install Environment') {
            steps {
                // Using 'bat' for Windows and 'python -m' to ensure the 3.14 path is used
                bat 'python -m pip install pytest'
            }
        }

        stage('Run Logic Tests') {
            steps {
                // '|| exit 0' ensures the pipeline continues to the upload stage even if a test fails
                bat 'python -m pytest test_logic.py --junitxml=results.xml || exit 0'
            }
        }

        stage('Update Xray Execution') {
            steps {
                // Sends results.xml to update LOGI-70
                step([$class: 'XrayImportResultsBuilder',
                    serverInstance: "${env.JIRA_INSTANCE}",
                    endpointName: '/junit',
                    importFilePath: 'results.xml',
                    importInfo: [
                        testExecutionKey: "${env.TEST_EXEC_KEY}"
                    ]
                ])
            }
        }
    }
}
