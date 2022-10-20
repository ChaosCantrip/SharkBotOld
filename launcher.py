import os
import time

print("Starting SharkBot Launcher Script")

while True:
    os.system("sudo git pull")
    os.system("sudo python3 main.py")

    if not os.path.exists("instant_restart"):
        time.sleep(300)
    else:
        os.remove("instant_restart")
