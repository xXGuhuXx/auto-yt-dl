import string
import pytubDef
from pytube import Channel
from pytube import YouTube


def downloadNewVideo(videoURL):
    video = YouTube(videoURL)
    print("Downloading new Video: " + str(video.title))
    video.streams.get_highest_resolution().download(output_path="Downloads")


def urlAlreadyWritten(url: string, channelName: string):
    urlFile = open("data/" + channelName + ".txt", "rt")
    endOfFileNotReached = True
    returnBool = False
    while endOfFileNotReached:

        line = urlFile.readline()

        if line == "":
            urlFile.close()
            endOfFileNotReached = False

        if str(line).__contains__(str(url)):
            endOfFileNotReached = False
            returnBool = True
            urlFile.close()

    return returnBool


def writeURLsToTxt(selectedChannel: Channel):
    try:
        urlFile = open("data/" + selectedChannel.channel_name + ".txt", "rt")
        print(selectedChannel.channel_name + "´s URL-File already exist")
    except:
        urlFile = open("data/" + selectedChannel.channel_name + ".txt", "x")
        urlFile.mode = "rt"
        print(selectedChannel.channel_name + "´s URL-File does not exist, created File")

    urlFile.close()

    print("Writing URL(s) to " + selectedChannel.channel_name)

    for n in range(selectedChannel.video_urls.__len__()):

        if not urlAlreadyWritten(selectedChannel.video_urls[n], selectedChannel.channel_name):
            urlFile = open("data/" + selectedChannel.channel_name + ".txt", "a")
            urlFile.writelines(" \n" + str(selectedChannel.video_urls[n]))
            urlFile.close()


def writeURLtoFile(selectedChannel: Channel, url: string):
    try:
        urlFile = open("data/" + selectedChannel.channel_name + ".txt", "rt")
        print(selectedChannel.channel_name + "´s URL-File already exist")
    except:
        urlFile = open("data/" + selectedChannel.channel_name + ".txt", "x")
        urlFile.mode = "rt"
        print(selectedChannel.channel_name + "´s URL-File does not exist, created File")

    urlFile.close()

    if not urlAlreadyWritten(url, selectedChannel.channel_name):
        urlFile = open("data/" + selectedChannel.channel_name + ".txt", "a")
        urlFile.writelines(" \n" + url)
        urlFile.close()
        print("Writing URL to " + selectedChannel.channel_name)
    else:
        print("URL is already written")


def loop():
    channelArray = returnMonitoredChannels()

    for m in range(channelArray.__len__()):
        checkForNewURL(channelArray[m])


def checkForNewURL(selectedChannel: Channel):
    foundNewVid = 0

    for n in range(selectedChannel.video_urls.__len__()):
        if not urlAlreadyWritten(selectedChannel.video_urls[n], selectedChannel.channel_name):
             print("Found and downloading a new URL from " + selectedChannel.channel_name)
             foundNewVid = foundNewVid + 1
             downloadNewVideo(selectedChannel.video_urls[n])
             writeURLtoFile(selectedChannel, selectedChannel.video_urls[n])

    print("Found " + str(foundNewVid) + " new Videos from " + str(selectedChannel.channel_name))


def returnMonitoredChannels():
    monitoredChannelsFile = open("data/monitoredChannels.txt", "rt")
    channelURLs = monitoredChannelsFile.readlines()
    monitoredChannelsFile.close()
    monitoredChannelsArray = [Channel]

    for n in range(channelURLs.__len__()):

        if channelURLs[n].__contains__("https://"):
            monitoredChannelsArray.append(Channel(channelURLs[n]))

    monitoredChannelsArray.pop(0)
    return monitoredChannelsArray


def newMonitoredChannel(newChannelURL: string):
    alreadyWritten = False
    try:
        c = Channel(newChannelURL)
    except:
        print("URL is not Valid")
        return False
    else:
        cArray = returnMonitoredChannels()

        for n in range(cArray.__len__()):
            if cArray[n].channel_name.__contains__(c.channel_name):
                alreadyWritten = True
                print("Channel already added")
                break

        if not alreadyWritten:
            monitoredChannelsFile = open("data/monitoredChannels.txt", "a")
            monitoredChannelsFile.write(" \n" + newChannelURL)
            monitoredChannelsFile.close()
            writeURLsToTxt(c)
            return True
        else:
            return False


def removeMonitoredChannel(oldChannelURL: string):
    monitoredChannelsFile = open("data/monitoredChannels.txt", "rt")
    channelURLs = monitoredChannelsFile.readlines()
    monitoredChannelsFile.close()

    for n in range(channelURLs.__len__()):
        if channelURLs[n].__contains__(oldChannelURL):
            del channelURLs[n]
            break

    monitoredChannelsFile = open("data/monitoredChannels.txt", "w")
    for n in range(channelURLs.__len__()):
        monitoredChannelsFile.write(channelURLs[n])