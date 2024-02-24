import pymongo
import os

# --- Configuration ---
# Configuration
client = None  # Placeholder, will be initialized on demand
db = None
collection = None


def connect_db():
    global client, db, collection
    client = pymongo.MongoClient(os.getenv('DATABASE_URL'))
    db = client["mydb"]
    collection = db["zywa"]


def disconnect_db():
    global client
    if client:
        client.close()
        client = None



# --- Card Model ---
class Card:
    def __init__(self, CARD_ID, USER_CONTACT, STATUS_HISTORY, _id=None):
        self.CARD_ID = CARD_ID
        self.USER_CONTACT = USER_CONTACT
        self.STATUS_HISTORY = STATUS_HISTORY

    @staticmethod
    def dropcollection():
        connect_db()
        db['zywa'].drop()
        disconnect_db()

    def save(self):
        """Inserts a new Card document into the MongoDB collection."""
        document = {
            "CARD_ID": self.CARD_ID,
            "USER_CONTACT": self.USER_CONTACT,
            "STATUS_HISTORY": self.STATUS_HISTORY
        }
        connect_db()
        result = collection.insert_one(document)
        disconnect_db()
        return result.inserted_id  # Optionally return the inserted ID

    @classmethod
    def find_by_card_id(cls, CARD_ID):
        """Finds a Card document by its CARD_ID."""
        connect_db()
        document = collection.find_one({"CARD_ID": CARD_ID})
        disconnect_db()
        if document:
            return cls(**document)  # Create a Card object from the document
        else:
            return None

    @classmethod
    def find_by_contant(cls, contact):
        """Finds a Card document by its CARD_ID."""
        connect_db()
        document = collection.find_one({"USER_CONTACT": contact})
        disconnect_db()
        if document:
            return cls(**document)  # Create a Card object from the document
        else:
            return None

    def update_status(self, STATUS, COMMENT, TIMESTAMP):
        """Appends a new status entry to the STATUS_HISTORY."""
        connect_db()
        new_entry = {
            "STATUS": STATUS,
            "COMMENT": COMMENT,
            "TIMESTAMP": TIMESTAMP
        }
        result = collection.update_one(
            {"CARD_ID": self.CARD_ID},
            {"$push": {"STATUS_HISTORY": new_entry}}
        )
        disconnect_db()
        return result.modified_count  # Returns the number of modified documents
