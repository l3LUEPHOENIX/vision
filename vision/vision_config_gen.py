from os import urandom

with open('vision_key','w') as vision_key_file:
    vision_key_file.write(urandom(16).hex())

