import os

print("Starting SharkBot Launcher Script")

while True:
    os.system("sudo git pull")
    os.system("sudo python3 main.py")

    if os.path.exists("maintenance") or not os.path.exists("instant_restart"):
        os.system("sudo python3 maintenance.py")
    else:
        os.remove("instant_restart")
