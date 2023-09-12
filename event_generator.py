import time
import datetime

count = 1
while True:
    ct = datetime.datetime.now()
    
    log_message = f"[{ct}] event_generator.py: This is entry number {count}"
    
    with open('dummy.log', 'a') as myFile:
        myFile.write(log_message + "\n")
    
    print(f"Successful write count: {count}")
    
    count += 1
    
    time.sleep(1)