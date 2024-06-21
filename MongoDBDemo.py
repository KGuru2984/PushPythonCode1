from hashlib import sha256
import json
import time
from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
import uuid

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.blockchain

# Generate a globally unique address for this node
node_identifier = str(uuid.uuid4()).replace('-', '')


class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash='1', proof=100)

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        # Store block data in MongoDB
        db.blocks.insert_one(block)
        return block

    def new_transaction(self, sender, recipient, identity, value):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'identity': identity,
            'value': value,
        })
        # Store transaction data in MongoDB
        db.transactions.insert_one({
            'sender': sender,
            'recipient': recipient,
            'identity': identity,
            'value': value,
            'timestamp': time.time()
        })
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        return sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]


# Custom JSON encoder to handle ObjectId serialization
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)


blockchain = Blockchain()
app.json_encoder = CustomJSONEncoder


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['sender', 'recipient', 'identity', 'value']
    if not all(k in values for k in required):
        return 'Missing values', 400

    index = blockchain.new_transaction(values['sender'], values['recipient'], values['identity'], values['value'])
    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
