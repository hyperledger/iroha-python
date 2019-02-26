pipeline {
  environment {
    DOCKER_NETWORK = ''
    PROTOC_ZIP = 'protoc-3.5.1-linux-x86_64.zip'
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
        //   if (scmVars.GIT_LOCAL_BRANCH != "develop" && scmVars.CHANGE_BRANCH_LOCAL != "develop") {
        //     def builds = load ".jenkinsci/cancel-builds-same-job.groovy"
        //     builds.cancelSameJobBuilds()
        //   }
        }
      }
    }
    stage('Build') {
        parallel {
            stage('Build Linux') {
                agent { label 'd3-build-agent||docker-build-agent' }
                steps {
                    script {
                        iC = docker.image('hyperledger/iroha:develop-build')
                        iC.inside("") {
                            scmVars = checkout scm
                            // sh(script: "apt update && apt install -yqq curl git zip") // python3-dev python3-pip
                            // sh(script: "python3 -m pip install grpcio_tools protobuf")
                            // sh(script: "curl -OL https://github.com/google/protobuf/releases/download/v3.5.1/${PROTOC_ZIP}")
                            // sh(script: "unzip -o ${PROTOC_ZIP} -d /usr/local bin/protoc")
                            // sh(script: "rm -f ${PROTOC_ZIP}")
                            sh(script: "./scripts/download-schema.py")
                            sh(script: "./scripts/compile-proto.py")
                        }
                        iC = docker.image('quay.io/pypa/manylinux1_x86_64')
                        iC.inside("-v ${WORKSPACE}:/io") {
                          sh(script: """
                          for PYBIN in /opt/python/*/bin; do
                              "\${PYBIN}/pip" install -r /io/dev-requirements.txt
                              "\${PYBIN}/pip" wheel /io/ -w wheelhouse/
                          done

                          for whl in wheelhouse/*.whl; do
                              auditwheel repair "\${whl}" -w /io/wheelhouse/
                          done
                          """, returnStdout: true)
                        }
                    }
                    // script {
                    //     def scmVars = checkout scm
                    //     DOCKER_NETWORK = "${scmVars.CHANGE_ID}-${scmVars.GIT_COMMIT}-${BUILD_NUMBER}"
                    //     writeFile file: ".env", text: "SUBNET=${DOCKER_NETWORK}"
                    //     sh(returnStdout: true, script: "docker-compose -f docker/docker-compose.yaml pull")
                    //     sh(returnStdout: true, script: "docker-compose -f docker/docker-compose.yaml up --build -d")
                    //     sh(returnStdout: true, script: "docker exec d3-back-office-${DOCKER_NETWORK} /app/docker/back-office/wait-for-up.sh")
                    //     iC = docker.image('cypress/base:10')
                    //     iC.inside("--network='d3-${DOCKER_NETWORK}' --shm-size 4096m --ipc=host") {
                    //     sh(script: "yarn global add cypress")
                    //     var = sh(returnStatus:true, script: "yarn test:unit")
                    //     if (var != 0) {
                    //         echo '[FAILURE] Unit tests failed'
                    //         currentBuild.result = 'FAILURE';
                    //         return var
                    //     }
                    //     var = sh(returnStatus:true, script: "CYPRESS_baseUrl=http://d3-back-office:8080 CYPRESS_IROHA=http://grpcwebproxy:8080 cypress run")
                    //     if (var != 0) {
                    //         echo '[FAILURE] E2E tests failed'
                    //         currentBuild.result = 'FAILURE';
                    //         return var
                    //     }
                    //     }
                    // }
                }
            }
            stage('Build MacOS') {
                agent { label 'mac-mcst-3' }
                steps {
                    script {
                        sh(script: "echo 1")
                    }
                }
            }
        }
    }
    // stage('Tests (unit, e2e)') {
    //   agent { label 'd3-build-agent' }
    //   steps {
    //     script {
    //         def scmVars = checkout scm
    //         DOCKER_NETWORK = "${scmVars.CHANGE_ID}-${scmVars.GIT_COMMIT}-${BUILD_NUMBER}"
    //         writeFile file: ".env", text: "SUBNET=${DOCKER_NETWORK}"
    //         sh(returnStdout: true, script: "docker-compose -f docker/docker-compose.yaml pull")
    //         sh(returnStdout: true, script: "docker-compose -f docker/docker-compose.yaml up --build -d")
    //         sh(returnStdout: true, script: "docker exec d3-back-office-${DOCKER_NETWORK} /app/docker/back-office/wait-for-up.sh")
    //         iC = docker.image('cypress/base:10')
    //         iC.inside("--network='d3-${DOCKER_NETWORK}' --shm-size 4096m --ipc=host") {
    //           sh(script: "yarn global add cypress")
    //           var = sh(returnStatus:true, script: "yarn test:unit")
    //           if (var != 0) {
    //             echo '[FAILURE] Unit tests failed'
    //             currentBuild.result = 'FAILURE';
    //             return var
    //           }
    //           var = sh(returnStatus:true, script: "CYPRESS_baseUrl=http://d3-back-office:8080 CYPRESS_IROHA=http://grpcwebproxy:8080 cypress run")
    //           if (var != 0) {
    //             echo '[FAILURE] E2E tests failed'
    //             currentBuild.result = 'FAILURE';
    //             return var
    //           }
    //         }
    //     }
    //   }
    //   post {
    //     success {
    //       script {
    //         if (env.GIT_LOCAL_BRANCH in ["develop"] || env.CHANGE_BRANCH_LOCAL == 'develop') {
    //           def branch = env.CHANGE_BRANCH_LOCAL == 'develop' ? env.CHANGE_BRANCH_LOCAL : env.GIT_LOCAL_BRANCH
    //           sshagent(['jenkins-back-office']) {
    //             sh "ssh-agent"
    //             sh """
    //               rsync \
    //               -e 'ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no' \
    //               -rzcv --delete \
    //               dist/* \
    //               root@95.179.153.222:/var/www/dev/
    //             """
    //           }
    //         }
    //       }
    //     }
    //     always {
    //       script {
    //         withCredentials([usernamePassword(credentialsId: 'jenkins_nexus_creds', passwordVariable: 'NEXUS_PASS', usernameVariable: 'NEXUS_USER')]) {
    //           sh(script: "find \$(pwd)/tests/e2e/videos/*.mp4 -type f -exec curl -u ${NEXUS_USER}:${NEXUS_PASS} --upload-file {} https://nexus.iroha.tech/repository/back-office/crashes/${DOCKER_NETWORK}/ \\;", returnStdout: true)
    //           echo "You can find all videos here: https://nexus.iroha.tech/service/rest/repository/browse/back-office/crashes/${DOCKER_NETWORK}/"
    //         }
    //       }
    //     }
    //     cleanup {
    //       sh "mkdir build-logs"
    //       sh """
    //         while read -r LINE; do \
    //           docker logs \$(echo \$LINE | cut -d ' ' -f1) | gzip -6 > build-logs/\$(echo \$LINE | cut -d ' ' -f2).log.gz; \
    //         done < <(docker ps --filter "network=d3-${DOCKER_NETWORK}" --format "{{.ID}} {{.Names}}")
    //       """
    //       archiveArtifacts artifacts: 'build-logs/*.log.gz'
    //       sh "docker-compose -f docker/docker-compose.yaml down"
    //       cleanWs()
    //     }
    //   }
    // }
  }
}