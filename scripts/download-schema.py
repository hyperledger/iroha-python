#!/usr/bin/env python3


from six.moves import urllib
import os.path
from os import chdir

directory = os.path.dirname(os.path.abspath(__file__))
chdir(directory)
print('Working directory set to {}'.format(directory))

BASE_URL = 'https://raw.githubusercontent.com/hyperledger/iroha/master/shared_model/schema/'

FILES = [
    'block.proto',
    'commands.proto',
    'endpoint.proto',
    'primitive.proto',
    'proposal.proto',
    'qry_responses.proto',
    'queries.proto',
    'transaction.proto'
]

for file in FILES:
    print(file)
    data = urllib.request.urlopen(BASE_URL + file)
    print('\tdownloading')
    with open(os.path.join('..', 'schema', file), 'wb') as out:
        out.write(data.read())
        out.flush()
    print('\tsaved')

print('Done.')
