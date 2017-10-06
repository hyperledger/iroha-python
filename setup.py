from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import subprocess

from setuptools import find_packages, setup
from distutils.cmd import Command
from distutils.core import setup, Extension, Command
from distutils.util import get_platform
import os


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

sources = ["iroha/ed25519_sha3/ed25519_sha3module.c"]
sources.extend(["iroha/ed25519_sha3/lib/" + s for s in os.listdir("iroha/ed25519_sha3/lib/") if s.endswith(".c")])
module_ed25519_sha3 = Extension("ed25519_sha3",include_dirs=["iroha/ed25519_sha3/lib/"], sources=sources)

setup(
    name='iroha',
    version='0.95',
    description='Python library for Hyperledger Iroha',
    url='https://github.com/hyperledger/iroha-python',
    license='Apache',
    packages=find_packages(),
    ext_modules=[module_ed25519_sha3],
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
