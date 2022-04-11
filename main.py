from time import sleep
import pytubDef
import logging

logging.basicConfig(filename='mainDebug.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.info("Service started.")
print("Starting loop....")
while True:
    logging.info("Checking for new videos")
    print("Checking for new Videos")
    pytubDef.loop()
    sleep(int(pytubDef.returnInterval()))
