import string
import pytubDef
from pytube import Channel
from pytube import YouTube
from configparser import ConfigParser

def returnInterval():
    try:
        file =  "data/config.ini"
        config = ConfigParser()
        config.read(file)
        return config["Settings"]["interval"]
    except:
        createConfig()
        return returnInterval()


def returnChannelDir():
    try:
        file =  "data/config.ini"
        config = ConfigParser()
        config.read(file)
        return config.getboolean("Settings", "channelDir")
    except:
        createConfig()
        return returnChannelDir()

def updateInterval(interval: int):
    if interval>59:
        try:
            file =  "data/config.ini"
            config = ConfigParser()
            config.read(file)
            config.set("Settings","interval",str(interval))
            with open(file, 'w') as configfile:
                config.write(configfile)
        except:
            createConfig()
            updateInterval(interval)
    else:
        print("Interval must atleast be 60")

def toggleChannelDir():
    try:
        file = "data/config.ini"
        config = ConfigParser()
        config.read(file)
        if returnChannelDir():
            config.set("Settings", "channelDir", "False")
        else:
            config.set("Settings", "channelDir", "True")
        with open(file, 'w') as configfile:
            config.write(configfile)
    except:
        createConfig()
        toggleChannelDir()

def createConfig():
    config_object = ConfigParser()
    config_object["Settings"] = {
        "interval": "900",
        "channelDir": "True"
    }
    with open('data/config.ini', 'w') as conf:
        config_object.write(conf)

def downloadNewVideo(videoURL,path):
    video = YouTube(videoURL)
    print("Downloading new Video: " + str(video.title))
    try:
        video.streams.get_highest_resolution().download(output_path=path)
    except:
        print("Failed to download video: " + str(video.title) + ". Is it a livestream?" )


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
             if returnChannelDir():
                 path="Downloads/" + str(selectedChannel.channel_name)
             else:
                 path="Downloads"
             downloadNewVideo(selectedChannel.video_urls[n],path)
             writeURLtoFile(selectedChannel, selectedChannel.video_urls[n])


def returnMonitoredChannels():
    try:
        monitoredChannelsFile = open("data/monitoredChannels.txt", "rt")
    except:
        monitoredChannelsFile = open("data/monitoredChannels.txt", "x")
        monitoredChannelsFile.mode = "rt"

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