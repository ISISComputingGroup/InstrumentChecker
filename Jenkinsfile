#!groovy

pipeline {

  // agent defines where the pipeline will run.
  agent {  
    label {
      label "ConfigCheck"
    }
  }
  
  triggers {
    cron('H 1 * * *')
  }
  
  stages {  
    stage("Checkout") {
      steps {
        checkout scm
      }
    }
    
    stage("Build") {
      steps {
        
        bat """
            call build/update_genie_python.bat
            if %errorlevel% neq 0 (
                    @echo ERROR: Cannot install clean genie_python
                    goto ERROR
            )

            call run_tests.bat || echo "running tests failed."
            """
      }
    }
    
    stage("Unit Test Results") {
      steps {
        junit "test-reports/**/*.xml"
      }
   }
  }
  
  post {
    failure {
      step([$class: 'Mailer', notifyEveryUnstableBuild: true, recipients: 'icp-buildserver@lists.isis.rl.ac.uk', sendToIndividuals: true])
    }    
  }
  
  // The options directive is for configuration that applies to the whole job.
  options {
    buildDiscarder(logRotator(numToKeepStr:'20', daysToKeepStr: '28'))
    timeout(time: 60, unit: 'MINUTES')
    disableConcurrentBuilds()
  }
}
