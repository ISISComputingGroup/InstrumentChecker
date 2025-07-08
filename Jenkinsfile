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
    // as we "checkout scm" as a stage, we do not need to do it here too
    buildDiscarder(logRotator(numToKeepStr:'20', daysToKeepStr: '28'))
    timeout(time: 180, unit: 'MINUTES')
    disableConcurrentBuilds()
    timestamps()
    skipDefaultCheckout(true)
  }
}
