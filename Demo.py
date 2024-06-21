import uuid
import hashlib


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.id = uuid.uuid4().hex


class Blockchain:
    def __init__(self):
        self.users = {}
        self.create_genesis_user()

    def create_genesis_user(self):
        self.create_user("admin", "admin123")

    def create_user(self, username, password):
        if username not in self.users:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            self.users[username] = User(username, hashed_password)
            print("User '{}' created successfully.".format(username))
        else:
            print("User '{}' already exists.".format(username))

    def authenticate_user(self, username, password):
        if username in self.users:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if self.users[username].password == hashed_password:
                print("User '{}' authenticated successfully.".format(username))
                return True
        print("Authentication failed for user '{}'.".format(username))
        return False


# Example usage
blockchain = Blockchain()
blockchain.create_user("alice", "password123")
blockchain.authenticate_user("alice", "password123")
blockchain.authenticate_user("alice", "wrongpassword")
