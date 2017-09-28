from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import subprocess

from setuptools import find_packages, setup
from distutils.cmd import Command


def xrun(*args):
    subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                   check=True)


class GenerateProtobufCommand(Command):
    description = 'generate Protobuf schema'

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        xrun('make', 'all-proto')


class GenerateEd25519Sha3(Command):
    description = 'generate ed25519 sha3'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        xrun('cd','src/lib/ed25519')
        xrun('make','clean')
        xrun('make')



setup(
    name='iroha',
    version='0.95',
    description='Python library for Hyperledger Iroha',
    url='https://github.com/hyperledger/iroha-python',
    license='Apache',
    packages=find_packages(),
    # Keep the dependencies lexicographically sorted.
    install_requires=[
        'protobuf',
        'grpcio',
        'grpcio-tools',
        'pysha3',
        'pylint',
        'six'
    ],
    cmdclass={
        'genproto': GenerateProtobufCommand,
        'gened25519' : GenerateEd25519Sha3
    },
)
