import hashlib
import time

class Block:
    def __init__(self,data,previous_hash):
        self.timestamp = time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()   

    def calculate_hash(self):
        hash_string = f"{self.data}{self.previous_hash}{self.timestamp}".encode()
        return hashlib.sha256(hash_string).hexdigest()  # Use hashlib.sha256

class Blockchain:
    def __init__(self):
        self.chain=[]
        self.create_genesis_block()
    
    def create_genesis_block(self):
        genesis_block = Block("Genesis Block",0)
        self.chain.append(genesis_block)

    def add_block(self,data):
        previous_block = self.chain[-1]
        new_block = Block(data,previous_block.hash)
        self.chain.append(new_block)


# test the blockchain
        
blockchain = Blockchain()
blockchain.add_block("First Block")
blockchain.add_block("Second Block")


for block in blockchain.chain:
    print(block.data)