#!/usr/bin/env python3

# result codes are translated for text from documentation:
# https://iroha.readthedocs.io/en/develop/develop/api/commands.html


def resultOf_TransferAsset_ToHumanReadable(x):
    return {
        1: 'Could not transfer asset (Internal error happened)',
        2: 'No such permissions',
        3: 'No such source account',
        4: 'No such destination account',
        5: 'No such asset found',
        6: 'Not enough balance',
        7: 'Too much asset to transfer',
        0: 'OK'
    }.get(x, 0)


def resultOf_CreateDomain_ToHumanReadable(x):
    return {
        1: 'Could not create role (Internal error happened)',
        2: 'No such permissions',
        3: 'Domain already exists',
        4: 'No default role found',
        0: 'OK'
    }.get(x, 0)


def resultOf_CreateAccount_ToHumanReadable(x):
    return {
        1: 'Could not create account',
        2: 'No such permissions',
        3: 'No such domain',
        4: 'Account already exists',
        0: 'OK'
    }.get(x, 0)


def resultOf_CreateAsset_ToHumanReadable(x):
    return {
        1: 'Could not create asset',
        2: 'No such permissions',
        3: 'No such domain',
        4: 'Asset already exists',
        0: 'OK'
    }.get(x, 0)


def resultOf_AddAssetQuantity_and_TransferAsset_ToHumanReadable(x):
    return {
        1: 'Could not add asset quantity/transfer asset',
        2: 'No such permissions',
        3: 'No such asset/No such source account',
        4: 'Summation overflow (Resulting asset quantity is greater than the system can support)/No such destination account',
        5: 'No such asset found',
        6: 'Not enough balance',
        7: 'Too much asset to transfer',
        0: 'OK'
    }.get(x, 0)


def resultOf_AddAssetQuantity_ToHumanReadable(x):
    return {
        1: 'Could not add asset quantity/transfer asset',
        2: 'No such permissions',
        3: 'No such asset/No such source account',
        4: 'Summation overflow (Resulting asset quantity is greater than the system can support)/No such destination account',
        5: 'No such asset found',
        6: 'Not enough balance',
        7: 'Too much asset to transfer',
        0: 'OK'
    }.get(x, 0)


def resultOf_GetAccountAssetTransactions_ToHumanReadable(x):
    return {
        1: 'Could not get account transactions (Internal error happened)',
        2: 'No such permissions',
        3: 'Invalid signatures',
        4: 'Invalid pagination hash',
        5: 'Invalid account id',
        0: 'OK'
    }.get(x, 0)


def resultOf_SetAccountDetail_ToHumanReadable(x):
    return {
        1: 'Could not set account detail (Internal error happened)',
        2: 'No such permissions',
        3: 'No such account',
        0: 'OK'
    }.get(x, 0)


def resultOf_CompareAndSetAccountDetail_ToHumanReadable(x):
    return {
        1: 'Could not compare and set account detail (Internal error happened)',
        2: 'No such permissions',
        3: 'No such account',
        4: 'No match values',
        0: 'OK'
    }.get(x, 0)


def resultOf_GrantPermission_ToHumanReadable(x):
    return {
        1: 'Could not grant permission (Internal error happened)',
        2: 'No such permissions',
        3: 'No such account',
        0: 'OK'
    }.get(x, 0)


def resultOf_CreateRole_ToHumanReadable(x):
    return {
        1: 'Could not create role (Internal error happened)',
        2: 'No such permissions',
        3: 'Role already exists',
        0: 'OK'
    }.get(x, 0)


def resultOf_AppendRole_ToHumanReadable(x):
    return {
        1: 'Could not append role (Internal error happened)',
        2: 'No such permissions',
        3: 'No such account',
        4: 'No such role',
        0: 'OK'
    }.get(x, 0)


def resultOf_AddPeer_ToHumanReadable(x):
    return {
        1: 'Could not add peer (Internal error happened)',
        2: 'No such permissions',
        0: 'OK'
    }.get(x, 0)


def resultOf_RemovePeer_ToHumanReadable(x):
    return {
        1: 'Could not remove peer (Internal error happened)',
        2: 'No such permissions',
        3: 'No such peer',
        4: 'Network size does not allow to remove peer (After removing the peer the network would be empty)',
        0: 'OK'
    }.get(x, 0)


def resultOf_AddSignatory_ToHumanReadable(x):
    return {
        1: 'Could not add signatory (Internal error happened)',
        2: 'No such permissions',
        3: 'No such account',
        4: 'Signatory already exists',
        0: 'OK'
    }.get(x, 0)


def resultOf_RemoveSignatory_ToHumanReadable(x):
    return {
        1: 'Could not remove signatory (Internal error happened)',
        2: 'No such permissions',
        3: 'No such account',
        4: 'No such signatory',
        5: 'Quorum does not allow to remove signatory (After removing the signatory account will be left with less signatories, than its quorum allows)',
        0: 'OK'
    }.get(x, 0)


def resultOf_SetAccountQuorum_ToHumanReadable(x):
    return {
        1: 'Could not set quorum (Internal error happened)',
        2: 'No such permissions',
        3: 'No such account',
        4: 'No signatories on account (Add some signatories before setting quorum)',
        5: 'New quorum is incorrect (New quorum size is less than account’s signatories amount)',
        0: 'OK'
    }.get(x, 0)


error_codes_per_command = {
    'create_domain': resultOf_CreateDomain_ToHumanReadable,
    'create_asset': resultOf_CreateAsset_ToHumanReadable,
    'add_asset_quantity': resultOf_AddAssetQuantity_and_TransferAsset_ToHumanReadable,
    'create_account': resultOf_CreateAccount_ToHumanReadable,
    'transfer_asset': resultOf_TransferAsset_ToHumanReadable,
    'grant_permission': resultOf_GrantPermission_ToHumanReadable,
    'set_account_detail': resultOf_SetAccountDetail_ToHumanReadable,
    'set_account_quorum': resultOf_SetAccountQuorum_ToHumanReadable,
    'compare_and_set_account_detail': resultOf_CompareAndSetAccountDetail_ToHumanReadable,
    'create_role': resultOf_CreateRole_ToHumanReadable,
    'cppend_role': resultOf_AppendRole_ToHumanReadable,
    'add_peer': resultOf_AddPeer_ToHumanReadable,
    'remove_peer': resultOf_RemovePeer_ToHumanReadable,
    'add_signatory': resultOf_AddSignatory_ToHumanReadable,
    'remove_signatory': resultOf_RemoveSignatory_ToHumanReadable,
}


def get_proper_functions_for_commands(commands):
    if len(commands) == 1:
        return error_codes_per_command[commands[0]]

    def get_function(x: int):
        text = ''
        for command in commands:
            text += error_codes_per_command[command](x) + "|"
        return text[:-1]

    return get_function
