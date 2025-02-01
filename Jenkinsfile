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
        timeout(time: 2, unit: 'HOURS') {
          retry(5) {
            checkout scm
          }
        }
      }
    }
    
    stage("Dependencies") {
        steps {
          echo "Installing local genie python"
          bat """
                setlocal
                set WORKWIN=%WORKSPACE:/=\\%
                rd /s /q %WORKWIN%\\Python3
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
        logParser ([
            projectRulePath: 'parse_rules',
            parsingRulesPath: '',
            showGraphs: true, 
            unstableOnWarning: false,
            useProjectRule: true,
        ])
    } 
  }
  
  // The options directive is for configuration that applies to the whole job.
  options {
    buildDiscarder(logRotator(numToKeepStr:'20', daysToKeepStr: '28'))
    timeout(time: 180, unit: 'MINUTES')
    disableConcurrentBuilds()
    timestamps()
    skipDefaultCheckout(true)
  }
}
