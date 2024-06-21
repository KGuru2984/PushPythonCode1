import hashlib
import time


class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(
            str(self.index).encode('utf-8') +
            str(self.timestamp).encode('utf-8') +
            str(self.data).encode('utf-8') +
            str(self.previous_hash).encode('utf-8')
        )
        return sha.hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.votes = {}

    def create_genesis_block(self):
        return Block(0, time.time(), "Genesis Block", "0")

    def add_block(self, data):
        previous_block = self.get_latest_block()
        new_block = Block(previous_block.index + 1, time.time(), data, previous_block.hash)
        self.chain.append(new_block)

    def vote(self, candidate):
        self.votes[candidate] = self.votes.get(candidate, 0) + 1

    def get_votes(self):
        return self.votes

    def get_latest_block(self):
        return self.chain[-1]

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True


# Main function to test the voting system
def main():
    blockchain = Blockchain()

    # Add blocks to the blockchain
    blockchain.add_block("Candidate A")
    blockchain.add_block("Candidate B")
    blockchain.add_block("Candidate A")

    # Vote for candidates
    blockchain.vote("Candidate A")
    blockchain.vote("Candidate B")
    blockchain.vote("Candidate A")
    blockchain.vote("Candidate A")

    # Get vote results
    print("Vote Results:")
    for candidate, votes in blockchain.get_votes().items():
        print(f"{candidate}: {votes}")

    # Check if the blockchain is valid
    print("Is blockchain valid?", blockchain.is_chain_valid())


if __name__ == "__main__":
    main()
