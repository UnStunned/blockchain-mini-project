import datetime
import merkle_tree
import hashlib


class Block:
    def __init__(self, transactions, target):
        self.create_hashes(transactions)
        self.tx = list(map(lambda x: hashlib.sha256((hashlib.sha256(x.encode()).hexdigest()).encode()).hexdigest(),
                           self.create_hashes(transactions)))
        self.merkle_root = merkle_tree.MerkleTree(transactions).get_merkle_root().node_hash
        self.timestamp = round(float(datetime.datetime.now().timestamp()), 0)
        self.previous_hash = None
        self.miner = None
        self.block_height = None
        self.target = target
        self.nonce = 0
        self.block_hash = self.calculate_block_hash()

    def set_previous_hash(self, val):
        self.previous_hash = val

    def get_block_hash(self):
        return self.block_hash

    def get_timestamp(self):
        return self.timestamp

    def get_nonce(self):
        return self.nonce

    def calculate_block_hash(self):
        to_be_hashed = str(self.tx) + str(self.previous_hash) + str(self.merkle_root) + str(self.timestamp) + str(
            self.nonce)
        hashed_value = hashlib.sha256((hashlib.sha256(to_be_hashed.encode()).hexdigest()).encode()).hexdigest()
        iteration = 1
        while hashed_value < self.target:
            self.nonce += 1
            to_be_hashed = str(self.tx) + str(self.previous_hash) + str(self.merkle_root) + str(self.timestamp) + str(
                self.nonce)
            hashed_value = hashlib.sha256((hashlib.sha256(to_be_hashed.encode()).hexdigest()).encode()).hexdigest()
            iteration += 1
        print(f'Target found with nonce {self.nonce}')
        return hashlib.sha256((hashlib.sha256(to_be_hashed.encode()).hexdigest()).encode()).hexdigest()

    def set_block_height(self, val):
        self.block_height = val

    def set_miner(self, miner):
        self.miner = miner

    @staticmethod
    def create_hashes(transactions):
        t = list(map(lambda x: f'{x["t_id"]} {x["data"]}', transactions))
        return t


class Blockchain:
    def __init__(self, name):
        self.name = name
        self.blocks = []
        self.block_height = 0
        self.valid = True

    def get_block_height(self):
        return self.block_height

    def append_block(self, data):
        if str(type(data)) == "<class '__main__.Block'>" or str(type(data)) == "<class 'blockchain.Block'>":
            self.blocks.append(data)
            self.block_height = len(self.blocks)
            self.blocks[len(self.blocks) - 1].set_block_height(self.block_height - 1)
            if len(self.blocks) >= 2:
                self.blocks[-1].set_previous_hash(self.blocks[-2].block_hash)
            else:
                self.blocks[-1].set_previous_hash(
                    '0000000000000000000000000000000000000000000000000000000000000000')
        else:
            return print("Block could not be added to the blockchain!")

    def check_chain_validity(self):
        if len(self.blocks) >= 2:
            idx_1 = self.blocks.index(self.blocks[-1])
            idx_2 = self.blocks.index(self.blocks[-2])
            flag = 0
            for _ in range(len(self.blocks) - 1):
                if self.blocks[idx_1].previous_hash == self.blocks[idx_2].block_hash:
                    idx_1 -= 1
                    idx_2 -= 1
                    continue
                else:
                    flag = 1
                    break
            if self.blocks[idx_1].previous_hash != '0000000000000000000000000000000000000000000000000000000000000000':
                flag = 1
            else:
                pass
            if flag == 1:
                print("Invalid blockchain! Discarding.")
                return False
            else:
                print("Blockchain is valid!")
                return True
        elif 0 <= len(self.blocks) <= 1:
            print("Blockchain is valid!")
            return True

    def create_copy(self):
        blockchain_copy = Blockchain(self.name)
        blockchain_copy.blocks = self.blocks.copy()
        blockchain_copy.block_height = self.block_height
        blockchain_copy.valid = self.valid
        return blockchain_copy
