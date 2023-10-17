import os
from config import *
# If there is content in either file, do nothing, else write to file.

constants_in_config = {
    "VISION_KEY": 16,
    "VISION_KEY_IV": 16
}
configs = open('./config.py','a')
for var in constants_in_config.keys():
    try:
        eval(var)
    except:
        configs.write(f"{var}={os.urandom(constants_in_config[var]).hex()}")
configs.close()
