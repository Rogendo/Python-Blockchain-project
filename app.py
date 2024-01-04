from flask import Flask, render_template, request, jsonify, redirect  # Import the redirect function
import hashlib
import time
import json


app = Flask(__name__)

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.transactions}{self.timestamp}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []

    def create_genesis_block(self):
        return Block(0, [], time.time(), "0")

    def add_block(self, transactions):
        previous_block = self.get_latest_block()
        new_block = Block(len(self.chain), transactions, time.time(), previous_block.hash)
        self.chain.append(new_block)
        return new_block

    def get_latest_block(self):
        return self.chain[-1]

# Create a blockchain instance
blockchain = Blockchain()

@app.route('/')
def index():
    return render_template('index.html', chain=blockchain.chain)

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    sender = request.form['sender']
    recipient = request.form['recipient']
    amount = float(request.form['amount'])

    transaction = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount
    }

    blockchain.pending_transactions.append(transaction)
    return redirect('/')

@app.route('/mine_block')
def mine_block():
    previous_block = blockchain.get_latest_block()
    transactions = blockchain.pending_transactions.copy()
    blockchain.pending_transactions = []

    new_block = blockchain.add_block(transactions)

    return render_template('mined_block.html', block=new_block)

if __name__ == '__main__':
    app.run(debug=True)
