#!/usr/bin/env groovy

def doPythonWheels() {
    version = sh(script: 'git describe --tags \$(git rev-list --tags --max-count=1) || true', returnStdout: true).trim()
    checkTag = sh(script: 'git describe --tags --exact-match ${GIT_COMMIT}', returnStatus: true)
    if (checkTag != 0) {
        version += ".dev" + env.BUILD_NUMBER
    }

    sh(script: "sed -i.bak 's/{{ PYPI_VERSION }}/${version}/g' setup.py;")

    iC = docker.image('quay.io/pypa/manylinux1_x86_64')
    iC.inside("-v ${WORKSPACE}:/io") {
        sh(script: '/opt/python/cp35-cp35m/bin/pip wheel --no-deps /io/ -w /io/wheelhouse/', returnStdout: true)
    }
}

def publishWheels() {
    repo = "release"
    checkTag = sh(script: 'git describe --tags --exact-match ${GIT_COMMIT}', returnStatus: true)    
    version = sh(script: 'git describe --tags \$(git rev-list --tags --max-count=1) || true', returnStdout: true).trim()
    if (checkTag != 0) {
        version += ".dev" + env.BUILD_NUMBER
        repo = "develop"
    }
    withCredentials([usernamePassword(credentialsId: 'ci_nexus', passwordVariable: 'CI_NEXUS_PASSWORD', usernameVariable: 'CI_NEXUS_USERNAME'), usernamePassword(credentialsId: 'ci_iroha_pypi', passwordVariable: 'CI_PYPI_PASSWORD', usernameVariable: 'CI_PYPI_USERNAME')]) {
        sh(script: "cd wheelhouse && find . -type f -name \"iroha*.whl\" -exec curl -u ${CI_NEXUS_USERNAME}:${CI_NEXUS_PASSWORD} --upload-file {} https://nexus.iroha.tech/repository/artifacts/iroha-python/${repo}/{} \\;")
        sh(script: "cd wheelhouse && find . -type f -name \"iroha*.whl\" -exec echo 'Wheel available at https://nexus.iroha.tech/service/rest/repository/browse/artifacts/iroha-python/${repo}/{}' \\;")

        if (checkTag == 0) {
            iC = docker.image('quay.io/pypa/manylinux1_x86_64')
            iC.inside("") {
                sh(script: '/opt/python/cp35-cp35m/bin/pip install twine', returnStdout: true)
                sh(script: "cd wheelhouse && find . -type f -name \"iroha*.whl\" -exec curl -u ${CI_NEXUS_USERNAME}:${CI_NEXUS_PASSWORD} --upload-file {} https://nexus.iroha.tech/repository/artifacts/iroha-python/latest.whl \\;")
                sh(script: "cd wheelhouse && find . -type f -name \"iroha*.whl\" -exec echo 'Latest release available at https://nexus.iroha.tech/service/rest/repository/browse/artifacts/iroha-python/latest.whl' \\;")
                sh "/opt/python/cp35-cp35m/bin/twine upload --skip-existing -u ${CI_PYPI_USERNAME} -p ${CI_PYPI_PASSWORD} wheelhouse/iroha*.whl"
            }
        }
    }
}

def testWheels() {
    def scmVars = checkout scm
    def tests = ['tx-example.py', 'batch-example.py', 'blocks-query.py']
    DOCKER_NETWORK = "${scmVars.CHANGE_ID}-${scmVars.GIT_COMMIT}-${BUILD_NUMBER}"
    writeFile file: ".env", text: "SUBNET=${DOCKER_NETWORK}\nIROHA_VERSION=${IROHA_VERSION}"
    sh(script: "wget https://raw.githubusercontent.com/hyperledger/iroha/develop/example/config.docker -O docker/iroha/config.docker")
    sh(returnStdout: true, script: "docker-compose -f docker/docker-compose.yaml pull")
    sh(returnStdout: true, script: "docker-compose -f docker/docker-compose.yaml up --build -d")
    for (String item : tests) {
        iC = docker.image('python:3.5-slim')
        iC.inside("--network='${DOCKER_NETWORK}'") {
            sh(script: "find wheelhouse -type f -name \"iroha*.whl\" -exec pip install {} \\;")
            sh(script: "while ! timeout 2 bash -c \"echo > /dev/tcp/iroha/50051\"; do sleep 2; done")
            sh(script: "IROHA_HOST_ADDR=iroha ./examples/${item}")
        }
        sh(returnStdout: true, script: "docker-compose -f docker/docker-compose.yaml restart")
    }
    sh(returnStdout: true, script: "docker-compose -f docker/docker-compose.yaml down")
}

return this
