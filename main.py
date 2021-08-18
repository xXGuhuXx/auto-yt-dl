from time import sleep
import pytubDef


print("started loop")
while True:
    print("Checking for new Videos")
    pytubDef.loop()
    sleep(900)
