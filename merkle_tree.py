import hashlib
import math

class HashNode:
    def __init__(self, node_hash):
        self.node_hash = node_hash
        self.parent = []

    def set_parent(self, node):
        self.parent.append(node)


class MerkleTree:
    def __init__(self, transactions: list):
        self.transactions = list(map(lambda x: f'{x["t_id"]} {x["data"]}', transactions))
        self.merkle_root = None
        self.hashes = []
        self.nodes = []
        self.create_hashes()
        self.total_hashes, self.depth = self.calculate_total_hashes()
        self.create_tree()
        self.extract_hashes()
        self.set_parents()

    def create_hashes(self):
        for _ in self.transactions:
            self.hashes.append(hashlib.sha256((hashlib.sha256(_.encode()).hexdigest()).encode()).hexdigest())
            self.nodes.append(HashNode(hashlib.sha256((hashlib.sha256(_.encode()).hexdigest()).encode()).hexdigest()))

    def create_tree(self):
        counter = 0
        while len(self.hashes) > 1:
            last_layer = []
            for i in range(0, len(self.hashes), 2):
                if i != len(self.hashes) - 1:
                    result = self.combine_hashes(self.hashes[i], self.hashes[i + 1])
                    h = HashNode(result)
                    self.nodes.append(h)
                    last_layer.append(result)
                    counter += 1
                else:
                    result = self.combine_hashes(self.hashes[i - 1], self.hashes[i])
                    h = HashNode(result)
                    self.nodes.append(h)
                    last_layer.append(result)
                    counter += 1
            self.hashes.clear()
            self.hashes = last_layer
        self.merkle_root = self.nodes[-1]

    def calculate_total_hashes(self):
        depth = 0
        answer = len(self.hashes)
        current = answer
        while current != 1:
            current = math.ceil(current / 2)
            answer = answer + current
            depth += 1
        return answer, depth

    def extract_hashes(self):
        self.hashes.clear()
        for _ in self.nodes:
            self.hashes.append(_.node_hash)

    def get_merkle_root(self):
        return self.merkle_root

    def set_parents(self):
        hashes = []

        for _ in self.transactions:
            hashes.append(HashNode(hashlib.sha256(_.encode()).hexdigest()))

        while len(hashes) > 1:
            last_round = []
            for i in range(0, len(hashes), 2):
                if i != len(hashes) - 1 and len(hashes) > 1:
                    result = self.combine_hashes(hashes[i].node_hash, hashes[i + 1].node_hash)
                    last_round.append(HashNode(result))
                    for j in self.nodes:
                        if j.node_hash == result:
                            x = self.hashes.index(hashes[i].node_hash)
                            self.nodes[x].set_parent(j)
                            x = self.hashes.index(hashes[i + 1].node_hash)
                            self.nodes[x].set_parent(j)

                else:
                    result = self.combine_hashes(hashes[i - 1].node_hash, hashes[i].node_hash)
                    last_round.append(HashNode(result))
                    for j in self.nodes:
                        if j.node_hash == result:
                            x = self.hashes.index(hashes[i].node_hash)
                            self.nodes[x].set_parent(j)
                            x = self.hashes.index(hashes[i - 1].node_hash)
                            self.nodes[x].set_parent(j)
            hashes.clear()
            hashes = last_round

    @staticmethod
    def combine_hashes(h1, h2):
        h = h1 + h2
        return hashlib.sha256((hashlib.sha256(h.encode()).hexdigest()).encode()).hexdigest()
