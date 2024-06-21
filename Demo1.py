import hashlib
import json
import time


class PatientRecord:
    def __init__(self, patient_id, name, medical_history, treatments, diagnoses):
        self.patient_id = patient_id
        self.name = name
        self.medical_history = medical_history
        self.treatments = treatments
        self.diagnoses = diagnoses


class Block:
    def __init__(self, index, timestamp, patient_record, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.patient_record = patient_record
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({"index": self.index, "timestamp": self.timestamp,
                                   "patient_record": self.patient_record.__dict__, "previous_hash": self.previous_hash,
                                   "nonce": self.nonce}, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print("Block mined: ", self.hash)


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 2  # Adjust the difficulty to control mining speed

    def create_genesis_block(self):
        return Block(0, time.time(), PatientRecord("0", "Genesis Patient", "", "", ""), "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True


# Example usage
if __name__ == "__main__":
    blockchain = Blockchain()
    patient_record_1 = PatientRecord("12345", "Alice Smith", "Hypertension, Diabetes", "ACE inhibitors, Insulin",
                                     "Hypertensive crisis, Diabetic ketoacidosis")
    patient_record_2 = PatientRecord("67890", "Bob Johnson", "Asthma", "Bronchodilators", "Asthma exacerbation")

    blockchain.add_block(Block(1, time.time(), patient_record_1, blockchain.get_latest_block().hash))
    blockchain.add_block(Block(2, time.time(), patient_record_2, blockchain.get_latest_block().hash))

    print("Is blockchain valid? ", blockchain.is_chain_valid())
