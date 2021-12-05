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
            setlocal
            call build\\update_genie_python.bat
            if %errorlevel% neq 0 (
                    @echo ERROR: Cannot install clean genie_python
                    exit /b %errorlevel% 
            )

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
    timeout(time: 60, unit: 'MINUTES')
    disableConcurrentBuilds()
    timestamps()
  }
}
