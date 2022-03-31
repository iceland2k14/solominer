# -*- coding: utf-8 -*-
"""

@author: iceland
"""


from pprint import pprint
from threading import Thread
import requests
import binascii
import hashlib
import logging
import socket
import random
import json
import time


cHeight = 0 


# replace it with your bitcoin address
address = '1Q1Ten9ASaVMswFmvu64spJi96SojHCNWv'




def logg(msg):
    logging.basicConfig(level=logging.INFO, filename="miner.log", format='%(asctime)s %(message)s') # include timestamp
    logging.info(msg)




def get_current_block_height():
    # Returns the current network best height 
    r = requests.get('https://blockchain.info/latestblock')
    return int(r.json()['height'])



def newBlockListener():

    global cHeight

    while True:
        network_height = get_current_block_height()

        if network_height > cHeight: 
            logg('[*] Network has new height %d ' %network_height)
            logg('[*] Our local is %d' %cHeight)
            cHeight = network_height
            logg('[*] Our new local after update is %d' %cHeight)

        # respect Api
        time.sleep(40)





def BitcoinMiner(restart=False):

    if restart:
        time.sleep(2)
        logg('[*] Bitcoin Miner Restarted')
    else:
        logg('[*] Bitcoin Miner Started')
        print('[*] Bitcoin Miner Started')



    sock    = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('solo.ckpool.org', 3333))

    sock.sendall(b'{"id": 1, "method": "mining.subscribe", "params": []}\n')


    lines = sock.recv(1024).decode().split('\n')

    response = json.loads(lines[0])
    sub_details,extranonce1,extranonce2_size = response['result']

    sock.sendall(b'{"params": ["'+address.encode()+b'", "password"], "id": 2, "method": "mining.authorize"}\n')

    response = b''
    while response.count(b'\n') < 4 and not(b'mining.notify' in response): response += sock.recv(1024)

    responses = [json.loads(res) for res in response.decode().split('\n') if len(res.strip())>0 and 'mining.notify' in res]
    job_id,prevhash,coinb1,coinb2,merkle_branch,version,nbits,ntime,clean_jobs = responses[0]['params']
    target = (nbits[2:]+'00'*(int(nbits[:2],16) - 3)).zfill(64)
    extranonce2 = hex(random.randint(0,2**32-1))[2:].zfill(2*extranonce2_size)      # create random

    coinbase = coinb1 + extranonce1 + extranonce2 + coinb2
    coinbase_hash_bin = hashlib.sha256(hashlib.sha256(binascii.unhexlify(coinbase)).digest()).digest()

    merkle_root = coinbase_hash_bin
    for h in merkle_branch:
        merkle_root = hashlib.sha256(hashlib.sha256(merkle_root + binascii.unhexlify(h)).digest()).digest()

    merkle_root = binascii.hexlify(merkle_root).decode()

    #little endian
    merkle_root = ''.join([merkle_root[i]+merkle_root[i+1] for i in range(0,len(merkle_root),2)][::-1])

    

    work_on = get_current_block_height()






    while True:
        if cHeight > work_on:
            logg('[*] Restarting Miner')
            BitcoinMiner(restart=True)
            break 


        nonce   = hex(random.randint(0,2**32-1))[2:].zfill(8) # nnonve   #hex(int(nonce,16)+1)[2:]
        blockheader = version + prevhash + merkle_root + nbits + ntime + nonce +\
        '000000800000000000000000000000000000000000000000000000000000000000000000000000000000000080020000'
        hash = hashlib.sha256(hashlib.sha256(binascii.unhexlify(blockheader)).digest()).digest()
        hash = binascii.hexlify(hash).decode()



        if hash.startswith('000000000000000000000'): logg('hash: {}'.format(hash))
        if hash.startswith('000000000000000000'): logg('hash: {}'.format(hash))
        if hash.startswith('000000000000000'): logg('hash: {}'.format(hash))
        if hash.startswith('000000000000'): logg('hash: {}'.format(hash))
        if hash.startswith('0000000'): logg('hash: {}'.format(hash))



        if hash >= target :
            print('[*] New block mined')
            logg('[*] success!!')
            logg(blockheader)
            logg('hash: {}'.format(hash))
            payload = bytes('{"params": ["'+address+'", "'+job_id+'", "'+extranonce2 \
                +'", "'+ntime+'", "'+nonce+'"], "id": 1, "method": "mining.submit"}\n', 'utf-8')
            sock.sendall(payload)
            logg(payload)
            ret = sock.recv(1024)
            logg(ret)

            return True




if __name__ == '__main__':
    Thread(target = newBlockListener).start()
    time.sleep(2)
    Thread(target = BitcoinMiner).start()
