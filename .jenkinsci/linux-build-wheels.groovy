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
    checkTag = sh(script: 'git describe --tags --exact-match ${GIT_COMMIT}', returnStatus: true)
    // if (env.GIT_LOCAL_BRANCH == "master" &&  checkTag)
    withCredentials([usernamePassword(credentialsId: 'ci_nexus', passwordVariable: 'CI_NEXUS_PASSWORD', usernameVariable: 'CI_NEXUS_USERNAME')]) {
        sh "twine upload --skip-existing -u ${CI_NEXUS_USERNAME} -p ${CI_NEXUS_PASSWORD} --repository-url https://nexus.soramitsu.co.jp/repository/pypi-upload-${repo}/ wheelhouse/iroha*.whl"
    }
}

return this
