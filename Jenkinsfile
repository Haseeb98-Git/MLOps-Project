// pipeline {
//     agent any

//     environment {
//         // Define any environment variables if needed
//         PYTHON_ENV = 'python3'
//     }

//     stages {
//         stage('Checkout') {
//             steps {
//                 // Checkout the code from the Git repository
//                 checkout scm
//             }
//         }

//         stage('Set up Python') {
//             steps {
//                 // Install Python and dependencies
//                 sh 'python --version'  // Check Python version
//                 sh 'pip install --upgrade pip'  // Upgrade pip
//                 sh 'pip install -r requirements.txt'  // Install dependencies
//             }
//         }

//         stage('Linting') {
//             steps {
//                 // Run the linting process with flake8
//                 sh 'flake8 .'
//             }
//         }

//         stage('Testing') {
//             steps {
//                 // Run the tests with pytest
//                 sh 'pytest'
//             }
//         }
//     }

//     post {
//         always {
//             // Archive test results and any other necessary cleanup
//             junit '**/test-*.xml'  // This assumes your tests output in JUnit format
//         }
//         success {
//             // Actions for success (e.g., notify success)
//             echo "Build succeeded!"
//         }
//         failure {
//             // Actions for failure (e.g., notify failure)
//             echo "Build failed."
//         }
//     }
// }
