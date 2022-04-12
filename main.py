from time import sleep
import pytubDef
import logging

if pytubDef.log():
    logging.basicConfig(filename='data/mainDebug.log', encoding='utf-8', level=logging.DEBUG)
    
logging.info("Service started.")
print("Starting loop....")
while True:
    logging.info("Checking for new videos")
    print("Checking for new Videos")
    pytubDef.loop()
    sleep(int(pytubDef.returnInterval()))
