from time import sleep
import pytubDef
import logging
import os.path


def findLink(url):
    return pytubDef.getPlaylistURL(url.replace("\n", "").replace(" ", ""))


if pytubDef.log():
    logging.basicConfig(filename='data/mainDebug.log', encoding='utf-8', level=logging.DEBUG)

if os.path.exists("data/monitoredChannels.txt"):
    print("Deprecated monitoredChannel.txt file still exists. Converting...")
    try:
        success = True
        monitoredChannelsFile = open("data/monitoredChannels.txt", "rt")
        channelURLs = monitoredChannelsFile.readlines()
        monitoredChannelsFile.close()
        monitoredPlaylistFile = open("data/monitoredPlaylist.txt", "a")
        for line in channelURLs:
            if "https://" in line:
                print("Trying to find new link to " + line)
                try:
                    monitoredPlaylistFile.write(" \n" + findLink(line))
                except:
                    try:
                        monitoredPlaylistFile.write(" \n" + findLink(line.replace("/c/", "/channel/")))
                    except:
                        try:
                            monitoredPlaylistFile.write(" \n" + findLink(line.replace("/c/", "/@")))
                        except:
                            print("Could not find channel url for deprecated " + line)
                            print("Please add " + line + " manually.")
                            success = False
        monitoredPlaylistFile.close()
        if success:
            os.remove("data/monitoredChannels.txt")
        else:
            os.rename("data/monitoredChannels.txt", "data/DEPRECATEDmonitoredChannels.txt")
        print("Deprecated monitoredChannel.txt has been converted.")
    except Exception as e:
        print("Something went wrong while merging the deprecated monitoredChannel.txt file with the "
              "monitoredPlaylist.txt: " + str(e))
        logging.debug(e)
        logging.info("Something went wrong while merging the deprecated monitoredChannel.txt file with the "
                     "monitoredPlaylist.txt")

for playlist in pytubDef.returnMonitoredPlaylist():
    try:
        pytubDef.urlAlreadyWritten("",pytubDef.getPlaylistName(playlist))
    except:
        pytubDef.removeMonitoredPlaylist(playlist)
        pytubDef.newMonitoredPlaylist(playlist)
    try:
        pytubDef.getPlaylistName(playlist)
    except:
        pytubDef.createPlaylistConfigEntry(playlist)


logging.info("Service started.")
print("Starting loop....")

while True:
    logging.info("Checking for new videos")
    print("Checking for new Videos")
    try:
        pytubDef.loop()
    except Exception as e:
        logging.info("An error occurred while checking for new videos.")
        logging.debug(e)
        print("An error occurred while checking for new videos: " + str(e))
    print("Sleeping for " + pytubDef.returnInterval() + " Seconds till next check")
    sleep(int(pytubDef.returnInterval()))
