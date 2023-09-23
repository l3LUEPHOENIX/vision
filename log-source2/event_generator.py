import time
import datetime
import socket

count = 1
while True:
    
    log_message = f"[{datetime.datetime.now()}] {socket.gethostname()} (event_generator.py): This is entry number {count}"
    
    with open('dummy.log', 'a') as myFile:
        myFile.write(log_message + "\n")
    
    print(f"Successful write count: {count}")
    
    count += 1
    
    time.sleep(0.1)