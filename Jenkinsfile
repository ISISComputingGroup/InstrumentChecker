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
    
    stage("Dependencies") {
        steps {
          echo "Installing local genie python"
          bat """
                setlocal
                rd /s /q ${env.WORKSPACE}\\Python3
                call build\\update_genie_python.bat ${env.WORKSPACE}\\Python3
                if %errorlevel% neq 0 exit /b %errorlevel%
          """
        }
    }    

    stage("Run Tests") {
      steps {
        echo "Running tests"
        bat """
            setlocal
            call run_tests.bat
            if %errorlevel% neq 0 exit /b %errorlevel%
            """
      }
    }
    
  }
  
  post {
    always {
        junit "test-reports/**/*.xml"
    } 
  }
  
  // The options directive is for configuration that applies to the whole job.
  options {
    buildDiscarder(logRotator(numToKeepStr:'20', daysToKeepStr: '28'))
    timeout(time: 90, unit: 'MINUTES')
    disableConcurrentBuilds()
    timestamps()
  }
}
