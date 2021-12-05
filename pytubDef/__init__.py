import string
import pytubDef
from pytube import Channel
from pytube import YouTube
from pytube import Playlist
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

def returnYTAgent():
    try:
        file =  "data/config.ini"
        config = ConfigParser()
        config.read(file)
        return config.getboolean("Settings", "ytagent")
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
        print("Interval must be atleast 60")

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

def toggleYtAgent():
    try:
        file = "data/config.ini"
        config = ConfigParser()
        config.read(file)
        if returnYTAgent():
            config.set("Settings", "ytagent", "False")
        else:
            config.set("Settings", "ytagent", "True")
        with open(file, 'w') as configfile:
            config.write(configfile)
    except:
        createConfig()
        toggleYtAgent()

def createConfig():
    config_object = ConfigParser()
    config_object["Settings"] = {
        "interval": "900",
        "channelDir": "True",
        "ytagent": "False"
    }
    with open('data/config.ini', 'w') as conf:
        config_object.write(conf)

def downloadNewVideo(videoURL,path):
    video = YouTube(videoURL)
    print("Downloading new Video: " + str(video.title))
    try:
        if returnYTAgent():
            video.streams.get_highest_resolution().download(output_path=path, filename="[" + video.video_id + "].mp4")
        else:
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

def writeChannelURLsToTxt(selectedChannel: Channel):
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

def writePlaylistURLsToTxt(selectedPlaylist: Playlist):
    try:
        urlFile = open("data/" + selectedPlaylist.title + ".txt", "rt")
        print(selectedPlaylist.title + "´s URL-File already exist")
    except:
        urlFile = open("data/" + selectedPlaylist.title + ".txt", "x")
        urlFile.mode = "rt"
        print(selectedPlaylist.title + "´s URL-File does not exist, created File")

    urlFile.close()

    print("Writing URL(s) to " + selectedPlaylist.title)

    for n in range(selectedPlaylist.video_urls.__len__()):

        if not urlAlreadyWritten(selectedPlaylist.video_urls[n], selectedPlaylist.title):
            urlFile = open("data/" + selectedPlaylist.title + ".txt", "a")
            urlFile.writelines(" \n" + str(selectedPlaylist.video_urls[n]))
            urlFile.close()

def writeChannelURLtoFile(selectedChannel: Channel, url: string):
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

def writePlaylistURLtoFile(selectedPlaylist: Playlist, url: string):
    try:
        urlFile = open("data/" + selectedPlaylist.title + ".txt", "rt")
        print(selectedPlaylist.title + "´s URL-File already exist")
    except:
        urlFile = open("data/" + selectedPlaylist.title + ".txt", "x")
        urlFile.mode = "rt"
        print(selectedPlaylist.title + "´s URL-File does not exist, created File")

    urlFile.close()

    if not urlAlreadyWritten(url, selectedPlaylist.title):
        urlFile = open("data/" + selectedPlaylist.title + ".txt", "a")
        urlFile.writelines(" \n" + url)
        urlFile.close()
        print("Writing URL to " + selectedPlaylist.title)
    else:
        print("URL is already written")

def loop():
    channelArray = returnMonitoredChannels()
    playlistArray = returnMonitoredPlaylist()

    for m in range(channelArray.__len__()):
        try:
            checkForNewURLFromChannel(channelArray[m])
        except:
            print("Oops. Something went wrong while checkig for new Videos")

    for m in range(playlistArray.__len__()):
        try:
            checkForNewURLFromPlaylist(playlistArray[m])
        except:
            print("Oops. Something went wrong while checkig for new Videos")

def checkForNewURLFromChannel(selectedChannel: Channel):
    foundNewVid = 0

    for n in range(selectedChannel.video_urls.__len__()):
        if not urlAlreadyWritten(selectedChannel.video_urls[n], selectedChannel.channel_name):
             print("Found and downloading a new URL from " + selectedChannel.channel_name)
             foundNewVid = foundNewVid + 1
             if returnChannelDir():
                 path="Downloads/" + str(selectedChannel.channel_name)
             else:
                 path="Downloads"
             if returnYTAgent():
                 path="Downloads/[" + str(selectedChannel.channel_id) + "]"
             downloadNewVideo(selectedChannel.video_urls[n],path)
             writeChannelURLtoFile(selectedChannel, selectedChannel.video_urls[n])

def checkForNewURLFromPlaylist(selectedPlaylist: Playlist):
    foundNewVid = 0

    for n in range(selectedPlaylist.video_urls.__len__()):
        if not urlAlreadyWritten(selectedPlaylist.video_urls[n], selectedPlaylist.title):
             print("Found and downloading a new URL from " + selectedPlaylist.title)
             foundNewVid = foundNewVid + 1
             if returnChannelDir():
                 path="Downloads/" + str(selectedPlaylist.title)
             else:
                 path="Downloads"
             if returnYTAgent():
                 path="Downloads/[" + str(selectedPlaylist.playlist_id) + "]"
             downloadNewVideo(selectedPlaylist.video_urls[n],path)
             writePlaylistURLtoFile(selectedPlaylist, selectedPlaylist.video_urls[n])

def returnMonitoredChannels():
    try:
        monitoredChannelsFile = open("data/monitoredChannels.txt", "rt")
    except:
        monitoredChannelsFile = open("data/monitoredChannels.txt", "x")
        monitoredChannelsFile.mode = "r"

    channelURLs = monitoredChannelsFile.readlines()

    monitoredChannelsFile.close()
    monitoredChannelsArray = [Channel]

    for n in range(channelURLs.__len__()):

        if channelURLs[n].__contains__("https://"):
            monitoredChannelsArray.append(Channel(channelURLs[n]))

    monitoredChannelsArray.pop(0)
    return monitoredChannelsArray

def returnMonitoredPlaylist():
    try:
        monitoredPlaylistFile = open("data/monitoredPlaylist.txt", "rt")
    except:
        monitoredPlaylistFile = open("data/monitoredPlaylist.txt", "x")
        monitoredPlaylistFile.mode = "r"

    playlistURLs = monitoredPlaylistFile.readlines()

    monitoredPlaylistFile.close()
    monitoredPlaylistArray = [Playlist]

    for n in range(playlistURLs.__len__()):

        if  playlistURLs[n].__contains__("https://"):
            monitoredPlaylistArray.append(Playlist(playlistURLs[n]))

    monitoredPlaylistArray.pop(0)
    return monitoredPlaylistArray

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
            monitoredChannelsFile.write(" \n" + c.channel_url)
            monitoredChannelsFile.close()
            writeChannelURLsToTxt(c)
            return True
        else:
            return False

def newMonitoredPlaylist(newPlaylistURL: string):
    alreadyWritten = False
    try:
        p = Playlist(newPlaylistURL)
    except:
        print("URL is not Valid")
        return False
    else:
        pArray = returnMonitoredPlaylist()

        for n in range(pArray.__len__()):
            if pArray[n].playlist_url.__contains__(p.playlist_url):
                alreadyWritten = True
                print("Playlist already added")
                break

        if not alreadyWritten:
            monitoredPlaylistFile = open("data/monitoredPlaylist.txt", "a")
            monitoredPlaylistFile.write(" \n" + p.playlist_url)
            monitoredPlaylistFile.close()
            writePlaylistURLsToTxt(p)
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

def removeMonitoredPlaylist(oldPlaylistURL: string):
    monitoredPlaylistFile = open("data/monitoredPlaylist.txt", "rt")
    playlistURLs = monitoredPlaylistFile.readlines()
    monitoredPlaylistFile.close()

    for n in range(playlistURLs.__len__()):
        if playlistURLs[n].__contains__(oldPlaylistURL):
            del playlistURLs[n]
            break

    monitoredPlaylistFile = open("data/monitoredPlaylist.txt", "w")
    for n in range(playlistURLs.__len__()):
        monitoredPlaylistFile.write(playlistURLs[n])