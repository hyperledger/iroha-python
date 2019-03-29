#!/usr/bin/env groovy

def doPythonWheels() {
    version = sh(script: 'git describe --tags \$(git rev-list --tags --max-count=1) || true', returnStdout: true).trim()
    repo = "master"
    if (env.GIT_LOCAL_BRANCH != "master") {
        version += ".dev" + env.BUILD_NUMBER
        repo = "develop"
    }

    sh(script: "sed -i.bak 's/{{ PYPI_VERSION }}/${version}/g' setup.py;")

    iC = docker.image('quay.io/pypa/manylinux1_x86_64')
    iC.inside("-v ${WORKSPACE}:/io") {
        sh(script: '/opt/python/cp35-cp35m/bin/pip wheel --no-deps /io/ -w /io/wheelhouse/', returnStdout: true)
    }
}

def publishWheels() {
    checkTag = sh(script: 'git describe --tags --exact-match ${GIT_COMMIT}', returnStatus: true)
    withCredentials([usernamePassword(credentialsId: 'ci_nexus', passwordVariable: 'CI_NEXUS_PASSWORD', usernameVariable: 'CI_NEXUS_USERNAME')]) {
        sh(script: "find wheelhouse -type f -name \"iroha*.whl\" -exec curl -u ${CI_NEXUS_USERNAME}:${CI_NEXUS_PASSWORD} --upload-file {} https://nexus.iroha.tech/repository/artifacts/iroha-python/${repo}/{} \\;")
        sh(script: "find wheelhouse -type f -name \"iroha*.whl\" -exec echo 'https://nexus.iroha.tech/service/rest/repository/browse/artifacts/iroha-python/${repo}/{} \\;")
    }
    if (env.GIT_LOCAL_BRANCH == '' && checkTag) {
        iC = docker.image('quay.io/pypa/manylinux1_x86_64')
        iC.inside("") {
            sh(script: '/opt/python/cp35-cp35m/bin/pip install twine', returnStdout: true)
            sh "/opt/python/cp35-cp35m/bin/twine upload --skip-existing -u ${ci_pypi_username} -p ${ci_pypi_password} --repository-url https://test.pypi.org/legacy/ wheelhouse/iroha*.whl"
        }
    }
}

def testWheels() {
    def scmVars = checkout scm
    def tests = ['tx-example.py', 'batch-example.py', 'blocks-query.py']
    for (String item : tests) {
        DOCKER_NETWORK = "${scmVars.CHANGE_ID}-${scmVars.GIT_COMMIT}-${BUILD_NUMBER}"
        writeFile file: ".env", text: "SUBNET=${DOCKER_NETWORK}\nIROHA_VERSION=${IROHA_VERSION}"
        sh(script: "wget https://raw.githubusercontent.com/hyperledger/iroha/develop/example/config.docker -O docker/iroha/config.docker")
        sh(returnStdout: true, script: "docker-compose -f docker/docker-compose.yaml pull")
        sh(returnStdout: true, script: "docker-compose -f docker/docker-compose.yaml up --build -d")
        iC = docker.image('python:3.5-slim')
        iC.inside("--network='${DOCKER_NETWORK}'") {
            sh(script: "find wheelhouse -type f -name \"iroha*.whl\" -exec pip install {} \\;")
            sh(script: "while ! timeout 2 bash -c \"echo > /dev/tcp/iroha/50051\"; do sleep 2; done")
            sh(script: "IROHA_HOST_ADDR=iroha ./examples/${item}")
        }
        sh(returnStdout: true, script: "docker-compose -f docker/docker-compose.yaml down")
    }
}

return this
