from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import subprocess

from setuptools import find_packages, setup
from distutils.cmd import Command


def xrun(*args):
    subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                   check=True)


class GenerateFlatbuffersCommand(Command):
    description = 'generate FlatBuffers schema'

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        xrun('flatc', '--python', '-o', '_generated', 'api.fbs')
        xrun('touch', '_generated/__init__.py')


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
    cmdclass={
        'genfbs': GenerateFlatbuffersCommand,
    },
)
