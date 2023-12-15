# A place to store constants for the Vision tool
from Crypto.Cipher import AES
import os
import pymongo
from hashlib import sha256

# Create a mongodb client
# Get the Vision database from mongodb
# Get/Create the sources collection in monogdb
CLIENT = pymongo.MongoClient(
    os.environ["MONGODB_HOSTNAME"],
    27017,
    username=os.environ["MONGODB_USERNAME"],
    password=os.environ["MONGODB_PASSWORD"],
)
DB = CLIENT["vision_db"]
VISION_VIEWER_SOURCES = DB["vision_viewer_sources"]

LDAP_BASE_DN = os.environ["LDAP_BASE_DN"]
LDAP_VISION_GROUP = os.environ["LDAP_VISION_GROUP"]
LDAP_USER_OU = os.environ["LDAP_USER_OU"]
LDAP_HOST = os.environ["LDAP_HOST"]

with open("/opt/vision/secrets/vision_key.txt", "r") as vision_key:
    VISION_KEY = vision_key.read()


def hashed_key(provided_key):
    return sha256(provided_key.encode("utf-8")).hexdigest()


def encrypt(text, HexKey):
    key = bytes.fromhex(HexKey)
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(bytes(text, encoding="ascii"))
    enc = cipher.nonce + ciphertext + tag
    return enc.hex()


def decrypt(text, HexKey):
    key = bytes.fromhex(HexKey)
    data = bytes.fromhex(text)
    cipher = AES.new(key, AES.MODE_GCM, data[:16])  # nonce
    try:
        plaintext = cipher.decrypt_and_verify(
            data[16:-16], data[-16:]
        )  # ciphertext, tag
        return str(plaintext, encoding="ascii")
    except ValueError:
        return "<DECRYPTION FAILED>"


def indexer_update(authentication, content):
    apikey = {"apikey_sum": hashed_key(authentication)}
    if content["action_type"] == "created":
        new_object = {
            "file_name": content["file_name"],
            "file_size": content["file_size"],
        }
        push_data = {"$addToSet": {"files": new_object}}
        VISION_VIEWER_SOURCES.update_one(apikey, push_data)
    elif content["action_type"] == "deleted":
        pull_data = {"$pull": {"files": {"file_name": content["file_name"]}}}
        VISION_VIEWER_SOURCES.update_one(apikey, pull_data)
    elif content["action_type"] == "modified":
        apikey["files.file_name"] = content["file_name"]
        set_data = {"$set": {"files.$.file_size": content["file_size"]}}
        VISION_VIEWER_SOURCES.update_one(apikey, set_data)

class mongo_document_validator():
    def __init__(self, key):
        self.key = hashed_key(key)
        self.document = VISION_VIEWER_SOURCES.find_one({"apikey_sum": self.key})

    def valid_key(self):
        if self.document:
            return True
        else:
            return False
        

    def valid_containers(self, containers):
        def container_check(containers):
            for container in containers:
                if container in self.document["containerIds"]:
                    return True
                else:
                    return False
        
        if isinstance(containers, str):
            containers = [containers]

        if self.document:
            return container_check(containers)
        else:
            return False    