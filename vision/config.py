# A place to store constants for the Vision tool
from Crypto.Cipher import AES
import os
import pymongo
from hashlib import sha256
import base64

def hashed_key(provided_key):
    return sha256(provided_key.encode('utf-8')).hexdigest()

def encrypt(text, HexKey):
    key = bytes.fromhex(HexKey)
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(bytes(text, encoding='ascii'))
    enc = cipher.nonce + ciphertext + tag
    return enc.hex()

def decrypt(text, HexKey):
    key = bytes.fromhex(HexKey)
    data = bytes.fromhex(text)
    cipher = AES.new(key, AES.MODE_GCM, data[:16]) # nonce
    try:
        plaintext = cipher.decrypt_and_verify(data[16:-16], data[-16:]) # ciphertext, tag
        return str(plaintext, encoding='ascii')
    except ValueError:
        return "<DECRYPTION FAILED>"

# Create a mongodb client
# Get the Vision database from mongodb
# Get/Create the sources collection in monogdb
CLIENT=pymongo.MongoClient(os.environ['MONGODB_HOSTNAME'], 27017, username=os.environ['MONGODB_USERNAME'],password=os.environ['MONGODB_PASSWORD'])
DB = CLIENT["vision_db"]
VISION_VIEWER_SOURCES = DB["vision_viewer_sources"]

with open('/opt/vision/secrets/vision_key.txt','r') as vision_key:
    VISION_KEY=vision_key.read()