# Driver File
import random
import network
import blockchain
import hashlib
import math

# initializing transactions
t_1 = [{'t_id': '0', 'data': '100BTC Credit'}, {'t_id': '1', 'data': '100BTC Credit'},
       {'t_id': '2', 'data': '100BTC Credit'}]
t_2 = [{'t_id': '0', 'data': '250BTC Credit'}, {'t_id': '1', 'data': '50BTC Credit'},
       {'t_id': '2', 'data': '100BTC Credit'}]
t_3 = [{'t_id': '0', 'data': '150BTC Credit'}, {'t_id': '1', 'data': '100BTC Credit'},
       {'t_id': '2', 'data': '500BTC Credit'}]

# initializing peers
peers_1 = ['192.168.1.100', '192.168.1.101', '192.168.1.102', '192.168.1.103']

# initializing blockchain
blockchain_1 = blockchain.Blockchain('Rods XL')

# creation of network for given blockchain
network_1 = network.Network(blockchain_1, peers_1)

# Setting a target for block 1
targ = 'fffff0f' + hashlib.sha256(
    hashlib.sha256(str(math.ceil(random.random() * 100)).encode()).hexdigest().encode()).hexdigest()[6:-1]

# peer 1 mining a block
block_1, timestamp, nonce = network_1.peers[0].mine_block(t_1, targ)
block_1.set_miner(network_1.peers[0].ip_address)

# other peers checking the validity of block 1
for i in network_1.peers:
    if i != block_1.miner:
        i.validate_block(block_1, nonce, targ)

# peer 1 appending block to blockchain after validation
if network_1.approvals == len(network_1.peers):
    network_1.peers[0].local_blockchain.append_block(block_1)
    print(f'Block has been added to the local blockchain of {network_1.peers[0].ip_address}')

# checking chain validity
network_1.peers[0].local_blockchain.check_chain_validity()

# addition of a peer to the network
network_1.add_peer(network.Peer('192.168.1.104'))

# propogation of changes in blockchain
for i in network_1.peers:
    if i.ip_address != block_1.miner:
        i.local_blockchain.append_block(block_1)
        print(f'Block has been added to the local blockchain of {i.ip_address}')

# updating the global copy of blockchain
network_1.blockchain = network_1.peers[0].local_blockchain.create_copy()

# deallocation of redundant variables as these variable are already present on some or the other node
del i, block_1, targ, nonce, t_1, t_2, t_3, peers_1
