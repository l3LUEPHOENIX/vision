import time
import datetime
import socket
import os

count = 1
while True:
    
    log_message = f"[{datetime.datetime.now()}] {socket.gethostname()} (event_generator.py): This is entry number {count}"
    
    with open('dummy.log', 'a') as myFile:
        myFile.write(log_message + "\n")
    
    print(f"Successful write count: {count}")
    
    if count % 20 == 0:
        with open(f"/opt/log-source/dummy_dir/dummy_doc{str(int(count/20))}.txt", "w") as file:
            file.write(str(os.urandom(1000).hex()))
            
    count += 1

    time.sleep(0.5)