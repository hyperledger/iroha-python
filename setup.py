import setuptools

with open('README.md', 'r') as readme_file:
    long_description = readme_file.read()

setuptools.setup(
    name='iroha',
    version='0.0.2',
    description='Python library for Hyperledger Iroha',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='Apache-2.0',
    url='https://github.com/hyperledger/iroha-python',
    packages=setuptools.find_packages(
        exclude=['dist', 'build', '*.pyc', '.DS_Store',
                 '.vscode',  '.idea', '__pycache__', '*.bak']),
    install_requires=[
        'grpcio-tools',
        'pysha3;python_version<"3.6"'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent'
    ]
)
