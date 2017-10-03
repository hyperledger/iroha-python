from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import subprocess

from setuptools import find_packages, setup
from distutils.cmd import Command


def xrun(*args):
    subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                   check=True)


class GeneratePrev(Command):
    description = 'generate previous'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        xrun('make', 'all')


setup(
    name='iroha',
    version='0.95',
    description='Python library for Hyperledger Iroha',
    url='https://github.com/hyperledger/iroha-python',
    license='Apache',
    packages=find_packages(exclude=('tests')),
    data_files=[('iroha/lib/ed25519/lib', ['iroha/lib/ed25519/lib/libed25519.so'])],
    # Keep the dependencies lexicographically sorted.
    install_requires=[
        'protobuf',
        'grpcio',
        'grpcio-tools',
        'pysha3'
    ],
    cmdclass={
        'gen': GeneratePrev
    },
)
