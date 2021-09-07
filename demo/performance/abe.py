#!/usr/bin/env python

from charm.schemes.abenc.abenc_bsw07 import CPabe_BSW07
from charm.toolbox.pairinggroup import GT, PairingGroup

pg = PairingGroup('MNT224')
cpabe = CPabe_BSW07(pg)
(public_key, master_secret_key) = cpabe.setup()
attr_list = ['DEPT1', 'TEAM1']
secret_key = cpabe.keygen(public_key, master_secret_key, attr_list)
pol = '(DEPT1 and TEAM1)'
random_pg_elem = pg.random(GT)


def encrypt(plaintext, data=random_pg_elem, pairing_group=pg, pk=public_key, policy=pol, debug=0):
    """
    Encrypt data using ABE scheme with the given public key and policy
    :param data: the content to encrypt
    :param pairing_group: pairing group to use
    :param pk: public key to use for encryption
    :param policy: policy to apply during encryption
    :param debug: if 1, prints will be shown during execution; default 0, no prints are shown
    :return: encrypted data
    """
    #starting_time = time() * 1000.0

    # if debug:  # ONLY USE FOR DEBUG
    #    print('DATA = (%s) %s' % (type(data), data))
    #    print('PK = (%s) %s' % (type(pk), pk))
    #    print('POLICY = (%s) %s' % (type(policy), policy))

    #elapsed_time = (time() * 1000.0) - starting_time
    #print('[{}] before CPabe_BSW07'.format(elapsed_time))
    # Encrypt data with CP-ABE

    #elapsed_time = (time() * 1000.0) - starting_time
    #print('[{}] after Pabe_BSW07'.format(elapsed_time))

    # enc_data = cpabe.encrypt(pk, data, policy)
    return cpabe.encrypt(pk, data, policy)

    #elapsed_time = (time() * 1000.0) - starting_time
    #print('[{}] after cpabe.encrypt'.format(elapsed_time))

    # if debug:  # ONLY USE FOR DEBUG
    #    print('ENC DATA WITH POLICY = %s' % enc_data)

    # Remove policy from encrypted data
    # enc_data.pop('policy')

    # if debug:  # ONLY USE FOR DEBUG
    #    print('ENCRYPTED DATA = %s' % enc_data)

    #elapsed_time = (time() * 1000.0) - starting_time
    #print('[{}] end of abe.encrypt'.format(elapsed_time))

    # return enc_data


def decrypt(enc_data=None, pk=public_key, sk=secret_key, pairing_group=pg, debug=0):
    """
    Decrypt encrypted data with CP-ABE using the given public and secret key.
    :param enc_data: encrypted data to decrypt
    :param pk: CP-ABE public key
    :param sk: CP-ABE secret key
    :param pairing_group: pairing group to use
    :param debug: if 1, prints will be shown during execution; default 0, no prints are shown
    :return: decrypted data
    """

    # print('############################### ABE.DECRYPT')
    # import traceback
    # traceback.print_stack()
    return cpabe.decrypt(pk, sk, enc_data)
