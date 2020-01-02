pipeline {
  agent any
  triggers{
    pollSCM '* * * * *'
    cron(BRANCH_NAME == "master" ? "H H(2-5) * * *": "")
  }
  options { disableConcurrentBuilds() }
  parameters {
    booleanParam(name:"pytest_inmanta_dev" ,defaultValue: false, description: 'Changes the index used to install pytest-inmanta to the inmanta dev index')
  }
  stages {
    stage("setup"){
      steps{
        script{
          sh'''
          python3 -m venv ${WORKSPACE}/env
          ${WORKSPACE}/env/bin/pip install -U pip
          ${WORKSPACE}/env/bin/pip install -r requirements.dev.txt
          # make sure pytest inmanta is the required version
          '''
          if (params.pytest_inmanta_dev) {
            sh"""${WORKSPACE}/env/bin/pip install --pre -U pytest-inmanta -i https://artifacts.internal.inmanta.com/inmanta/dev"""
          }
        }
      }
    }
    stage("code linting"){
      steps{
        script{
          sh'''
          ${WORKSPACE}/env/bin/flake8 plugins tests
          '''
        }
      }
    }
    stage("tests"){
      steps{
        script{
          sh'''
          ${WORKSPACE}/env/bin/pytest tests -v --junitxml=junit.xml
          '''
          junit 'junit.xml'
        }
      }
    }
  }
  post{
    always{
      script{
        sh'''
        ${WORKSPACE}/env/bin/pip uninstall -y pytest-inmanta
        '''
      }
    }
  }
}
