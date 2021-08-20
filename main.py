from time import sleep
import pytubDef


print("Starting loop....")
while True:
    print("Checking for new Videos")
    pytubDef.loop()
    sleep(900)
