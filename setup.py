"""Setup script."""


from setuptools import find_packages, setup


setup(
    name='iroha',
    version='0.1.0',
    description='Python library for Hyperledger Iroha',
    url='https://github.com/hyperledger/iroha-python',
    license='Apache',
    packages=find_packages(),
    # Keep the dependencies lexicographically sorted.
    install_requires=[
        'ed25519',
        'flatbuffers',
        'future',
        'pysha3',
        'six',
    ],
)
