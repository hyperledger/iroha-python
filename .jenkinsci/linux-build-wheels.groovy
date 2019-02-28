#!/usr/bin/env groovy

def doPythonWheels() {
    version = sh(script: 'git describe --tags \$(git rev-list --tags --max-count=1) || true', returnStdout: true).trim()
    repo = 'release'
    if (env.GIT_LOCAL_BRANCH != "master") {
        repo = 'develop'
        version += ".dev" + env.BUILD_NUMBER
    }

    sh(script: "sed -i.bak 's/{{ PYPI_VERSION }}/${version}/g' setup.py;")

    iC = docker.image('quay.io/pypa/manylinux1_x86_64')
    iC.inside("-v ${WORKSPACE}:/io") {
        sh(script: '/opt/python/cp35-cp35m/bin/pip wheel --no-deps /io/ -w /io/wheelhouse/', returnStdout: true)
    }
}

def publishWheels() {
    checkTag = sh(script: 'git describe --tags --exact-match ${GIT_COMMIT}', returnStatus: true)
    // if (env.GIT_LOCAL_BRANCH == "master" &&  checkTag)
    withCredentials([usernamePassword(credentialsId: 'ci_nexus', passwordVariable: 'CI_NEXUS_PASSWORD', usernameVariable: 'CI_NEXUS_USERNAME')]) {
        sh(script: "find wheelhouse -type f -name \"iroha*.whl\" -exec curl -u ${CI_NEXUS_USERNAME}:${CI_NEXUS_PASSWORD} --upload-file wheelhouse/{} https://nexus.iroha.tech/repository/artifacts/iroha-python/wheels/{} \\;")
        // sh "/opt/python/cp35-cp35m/bin/twine upload --skip-existing -u ${CI_NEXUS_USERNAME} -p ${CI_NEXUS_PASSWORD} --repository-url https://nexus.soramitsu.co.jp/repository/pypi-upload-release/ wheelhouse/iroha*.whl"
    }
    // iC = docker.image('quay.io/pypa/manylinux1_x86_64')
    // iC.inside("") {
    //     // sh(script: '/opt/python/cp35-cp35m/bin/pip install twine', returnStdout: true)

    // }
}

def testWheels() {
    def scmVars = checkout scm
    DOCKER_NETWORK = "iroha-${scmVars.CHANGE_ID}-${scmVars.GIT_COMMIT}-${BUILD_NUMBER}"
    writeFile file: ".env", text: "SUBNET=${DOCKER_NETWORK}"
    sh(returnStdout: true, script: "docker-compose -f docker/docker-compose.yaml pull")
    sh(returnStdout: true, script: "docker-compose -f docker/docker-compose.yaml up --build -d")
    iC = docker.image('python:3.5-alpine')
    iC.inside("--network='iroha-${DOCKER_NETWORK}'") {
        sh(script: "find wheelhouse -type f -name \"iroha*.whl\" -exec pip install {} --no-index -f wheelhouse \\;")
    }
}

return this
