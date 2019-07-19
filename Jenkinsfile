pipeline {
  environment {
    DOCKER_NETWORK = ''
    IROHA_VERSION = 'latest'
  }
  options {
    skipDefaultCheckout()
    buildDiscarder(logRotator(numToKeepStr: '20'))
    timestamps()
  }
  agent any
  stages {
    stage ('Stop same job builds') {
      agent { label 'master' }
      steps {
        script {
          def scmVars = checkout scm
          // need this for develop->master PR cases
          // CHANGE_BRANCH is not defined if this is a branch build
          try {
            scmVars.CHANGE_BRANCH_LOCAL = scmVars.CHANGE_BRANCH
          }
          catch(MissingPropertyException e) { }
          if (scmVars.GIT_LOCAL_BRANCH != "develop" && scmVars.CHANGE_BRANCH_LOCAL != "develop") {
            def builds = load ".jenkinsci/cancel-builds-same-job.groovy"
            builds.cancelSameJobBuilds()
          }
        }
      }
    }
    stage('Linux') {
      agent { label 'd3-build-agent||docker-build-agent' }
      stages {
        stage('Prepare') {
          steps {
            script {
              iC = docker.image('hyperledger/iroha:develop-build')
              iC.inside("") {
                  scmVars = checkout scm
                  sh(script: "./scripts/download-schema.py")
                  sh(script: "./scripts/compile-proto.py")
              }
            }
          }
        }
        stage('Build wheels') {
          steps {
            script {
              def wheels = load ".jenkinsci/linux-build-wheels.groovy"
              wheels.doPythonWheels()
            }
          }
        }
        stage('Tests') {
          steps {
            script {
              def wheels = load ".jenkinsci/linux-build-wheels.groovy"
              wheels.testWheels()
            }
          }
        }
        stage('Publish wheels') {
          steps {
            script {
              def wheels = load ".jenkinsci/linux-build-wheels.groovy"
              archiveArtifacts artifacts: 'wheelhouse/iroha*.whl', allowEmptyArchive: true
              if (currentBuild.currentResult == "SUCCESS") {
                wheels.publishWheels()
              }
            }
          }
        }
      }
    }
  }
  post {
    cleanup {
      cleanWs()
    }
  }
}
