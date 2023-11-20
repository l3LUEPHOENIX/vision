from os import urandom

with open("/opt/vision/secrets/vision_key.txt", "w+") as vision_key_file:
    if len(vision_key_file.read()) <= 1:
        vision_key_file.write(urandom(16).hex())
