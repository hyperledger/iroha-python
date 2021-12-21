import setuptools

with open('README.md', 'r') as readme_file:
    long_description = readme_file.read()

setuptools.setup(
    name='iroha',
    version='{{ PYPI_VERSION }}',
    description='Python library for Hyperledger Iroha',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Soramitsu Co Ltd',
    author_email='admin@soramitsu.co.jp',
    license='Apache-2.0',
    url='https://github.com/hyperledger/iroha-python',
    packages=setuptools.find_packages(
        exclude=['dist', 'build', '*.pyc', '.DS_Store',
                 '.vscode',  '.idea', '__pycache__', '*.bak']),
    install_requires=[
        'protobuf>=3.8.0',
        'grpcio-tools>=1.12.1',
        'pysha3;python_version<"3.6"',
        'pynacl>=1.4.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent'
    ],
    project_urls={
        "Jenkins": "https://jenkins.soramitsu.co.jp/",
        "Nexus": "https://nexus.iroha.tech/",
        "Documentation": "https://iroha.readthedocs.io/en/latest/",
        "Doxygen": "https://docs.iroha.tech/",
        "Source Code": "https://github.com/hyperledger/iroha-python",
    }
)
