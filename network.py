import datetime
import blockchain
import hashlib


class Peer:
    def __init__(self, ip_address, name=None, type_of_node='Light Node'):
        self.ip_address = ip_address
        self.name = name
        self.type = type_of_node
        self.connected_to = []
        self.connection_time = datetime.datetime.now().ctime()
        self.local_blockchain = None
        self.network = None

    def set_network(self, network):
        self.network = network

    @staticmethod
    def mine_block(tx, targ):
        block = blockchain.Block(tx, targ)
        timestamp = block.get_timestamp()
        nonce = block.get_nonce()
        return block, timestamp, nonce

    def validate_block(self, block, nonce, targ):
        to_be_hashed = str(block.tx) + str(block.previous_hash) + str(block.merkle_root) + str(block.timestamp) + str(
            nonce)
        hashed_value = hashlib.sha256((hashlib.sha256(to_be_hashed.encode()).hexdigest()).encode()).hexdigest()
        if hashed_value > targ:
            print(f'Block has been validated by {self.ip_address}!')
            self.network.approvals += 1
        else:
            print('Block is invalid!')


class Network:
    def __init__(self, blockchain: blockchain.Blockchain, peers=None):
        self.network_type = "P2P"
        self.network_for = blockchain.name
        self.blockchain = blockchain
        if peers is None:
            self.peers = []
        else:
            self.peers = []
            for _ in range(len(peers)):
                self.peers.append(Peer(peers[_], f'Machine {_}'))
        self.connected_ips = list(map(lambda x: x.ip_address, self.peers))
        for i in self.peers:
            i.connected_to = self.find_connections(i.ip_address)
            i.local_blockchain = blockchain.create_copy()
            i.set_network(self)
        self.approvals = 0
        print(f'Network created for {self.network_for}!')

    def reset_approvals(self):
        self.approvals = 0

    def add_peer(self, peer, ip_address=None):
        if str(type(peer)) == "<class '__main__.Peer'>" or str(type(peer)) == "<class 'network.Peer'>":
            self.peers.append(peer)
            self.connected_ips.append(self.peers[-1].ip_address)
            self.peers[-1].connected_to = (self.find_connections(self.peers[-1].ip_address))
            for i in range(len(self.peers) - 2):
                self.peers[i].connected_to.append(self.peers[-1].ip_address)
            self.peers[-1].local_blockchain = self.blockchain.create_copy()

        else:
            peer = Peer(ip_address, peer)
            self.peers.append(peer)
            self.connected_ips.append(self.peers[-1].ip_address)
            self.peers[-1].connected_to = (self.find_connections(ip_address))
            for i in range(len(self.peers) - 2):
                self.peers[i].connected_to.append(ip_address)
            self.peers[-1].local_blockchain = self.blockchain.create_copy()

    def find_connections(self, ip):
        idx = self.connected_ips.index(ip)
        connections = self.peers.copy()
        connections.remove(connections[idx])
        return connections

    def propogate_change(self):
        pass
