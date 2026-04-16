pipeline {
    agent any
    
    environment {
        // Use the ID from your "Manage Credentials" screen
        XRAY_CREDS_ID = 'xray-cloud-creds'
        // Replace with your actual Jira Test Execution Key
        TEST_EXEC_KEY = 'LOGI-70'
        // The name you gave to the Jira instance in Jenkins System config
        JIRA_INSTANCE = 'JIRA_INSTANCE'
    }

    stages {
        stage('Install Environment') {
            steps {
                // Installs pytest so the agent can run the scripts
                sh 'pip install pytest'
            }
        }

        stage('Run Logic Tests') {
            steps {
                // Runs tests. '|| true' allows the pipeline to continue even if tests fail
                sh 'python -m pytest test_logic.py --junitxml=results.xml || true'
            }
        }

        stage('Update Xray Execution') {
            steps {
                // Sends results.xml to your specific Test Execution
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