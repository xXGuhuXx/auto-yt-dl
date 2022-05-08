import string
import pytubDef
from pytube import Channel
from pytube import YouTube
from pytube import Playlist
from configparser import ConfigParser
import logging
import youtube_dl


def log():
    try:
        file = "data/config.ini"
        config = ConfigParser()
        config.read(file)
        logging.debug("Returning log bool from config" + str(config.getboolean("Settings", "log")))
        try:
            return config.getboolean("Settings", "log")
        except:
            config.set("Settings", "log", "False")
            with open('data/config.ini', 'w') as conf:
                config.write(conf)
            return log()
    except Exception as e:
        logging.debug(e)
        logging.info("Config does not seem to exist, creating a new one")
        createConfig()
        return log()

def returnInterval():
    try:
        file = "data/config.ini"
        config = ConfigParser()
        config.read(file)
        logging.debug("Returning interval from config" + str(config["Settings"]["interval"]))
        return config["Settings"]["interval"]
    except Exception as e:
        logging.debug(e)
        logging.info("Config does not seem to exist, creating a new one")
        createConfig()
        return returnInterval()


def returnChannelDir():
    try:
        file = "data/config.ini"
        config = ConfigParser()
        config.read(file)
        logging.debug("Returning channelDir from config" + str(config.getboolean("Settings", "channelDir")))
        return config.getboolean("Settings", "channelDir")
    except Exception as e:
        logging.debug(e)
        logging.info("Config does not seem to exist, creating a new one")
        createConfig()
        return returnChannelDir()


def returnYTAgent():
    try:
        file =  "data/config.ini"
        config = ConfigParser()
        config.read(file)
        logging.debug("Returning ytagent from config" + str(config.getboolean("Settings", "ytagent")))
        return config.getboolean("Settings", "ytagent")
    except Exception as e:
        logging.debug(e)
        logging.info("Config does not seem to exist, creating a new one")
        createConfig()
        return returnChannelDir()


def updateInterval(interval: int):
    if interval > 59:
        try:
            file = "data/config.ini"
            config = ConfigParser()
            config.read(file)
            config.set("Settings", "interval", str(interval))
            with open(file, 'w') as configfile:
                config.write(configfile)
            logging.info("New interval " + str(interval) + " set")
        except Exception as e:
            logging.debug(e)
            logging.info("Config does not seem to exist, creating a new one")
            createConfig()
            updateInterval(interval)
    else:
        logging.info("Illegal interval: " + str(interval))
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
        logging.info("Toggled channelDir")
    except Exception as e:
        logging.debug(e)
        logging.info("Config does not seem to exist, creating a new one")
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
        logging.info("Toggled ytagent")
    except Exception as e:
        logging.debug(e)
        logging.info("Config does not seem to exist, creating a new one")
        createConfig()
        toggleYtAgent()


def createConfig():
    config_object = ConfigParser()
    config_object["Settings"] = {
        "interval": "900",
        "channelDir": "True",
        "ytagent": "False",
        "log": "False"
    }
    with open('data/config.ini', 'w') as conf:
        config_object.write(conf)
    logging.info("New config has been created")


def downloadNewVideo(videoURL, path):
    video = YouTube(videoURL)
    logging.info("Downloading: " + videoURL)
    print("Downloading new Video: " + str(video.title))
    try:
        if returnYTAgent():
            logging.info()
            video.streams.get_highest_resolution().download(output_path=path, filename="[" + video.video_id + "].mp4")
        else:
            video.streams.get_highest_resolution().download(output_path=path)
    except Exception as e:
        logging.debug(e)
        logging.error("Failed to download: " + str(videoURL) + "with pytube")
        logging.info("Downloading " + str(videoURL) + " with youtube_dl")
        try:
            if returnYTAgent():
                ydl_opts = {
                    'outtmpl': path + "/[" + "%(id)s" + "].mp4"
                }
            else:
                ydl_opts = {
                    'outtmpl': path + "/%(title)s.mp4"
                }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([videoURL])
        except:
            print("Failed to download video: " + str(video.title) + ". Is it a livestream?")
            return False
    return True


def urlAlreadyWritten(url: string, channelName: string):
    urlFile = open("data/" + replaceIllegalCharacters(channelName) + ".txt", "rt")
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


def replaceIllegalCharacters(input: str):
    tmp = input
    tmp = tmp.replace("<", "").replace(">", "").replace(":", "").replace('"', "").replace("/", "").replace("\\", "")
    return tmp.replace("|", "").replace("?", "").replace("*", "")


def writeChannelURLsToTxt(selectedChannel: Channel):
    try:
        urlFile = open("data/" + replaceIllegalCharacters(selectedChannel.channel_name) + ".txt", "rt")
        print(selectedChannel.channel_name + "´s URL-File already exist")
    except Exception as e:
        logging.debug(e)
        urlFile = open("data/" + replaceIllegalCharacters(selectedChannel.channel_name) + ".txt", "x")
        urlFile.mode = "rt"
        logging.info("Created new .txt for" + replaceIllegalCharacters(selectedChannel.channel_name))
        print(selectedChannel.channel_name + "´s URL-File does not exist, created File")

    urlFile.close()

    print("Writing URL(s) to " + selectedChannel.channel_name)
    logging.info("Writing URLs of already existing videos of" + selectedChannel.channel_name + "to .txt")
    for n in range(selectedChannel.video_urls.__len__()):

        if not urlAlreadyWritten(selectedChannel.video_urls[n], selectedChannel.channel_name):
            urlFile = open("data/" + replaceIllegalCharacters(selectedChannel.channel_name) + ".txt", "a")
            urlFile.writelines(" \n" + str(selectedChannel.video_urls[n]))
            urlFile.close()


def writePlaylistURLsToTxt(selectedPlaylist: Playlist):
    try:
        urlFile = open("data/" + replaceIllegalCharacters(selectedPlaylist.title) + ".txt", "rt")
        print(selectedPlaylist.title + "´s URL-File already exist")
    except Exception as e:
        logging.debug(e)
        urlFile = open("data/" + replaceIllegalCharacters(selectedPlaylist.title) + ".txt", "x")
        urlFile.mode = "rt"
        print(selectedPlaylist.title + "´s URL-File does not exist, created File")
        logging.info("Created new .txt for" + replaceIllegalCharacters(selectedPlaylist.title))

    urlFile.close()

    print("Writing URL(s) to " + selectedPlaylist.title)
    logging.info("Writing URLs of already existing videos of" + selectedPlaylist.title + "to .txt")
    for n in range(selectedPlaylist.video_urls.__len__()):

        if not urlAlreadyWritten(selectedPlaylist.video_urls[n], selectedPlaylist.title):
            urlFile = open("data/" + replaceIllegalCharacters(selectedPlaylist.title) + ".txt", "a")
            urlFile.writelines(" \n" + str(selectedPlaylist.video_urls[n]))
            urlFile.close()


def writeChannelURLtoFile(selectedChannel: Channel, url: string):
    try:
        urlFile = open("data/" + replaceIllegalCharacters(selectedChannel.channel_name) + ".txt", "rt")
        print(selectedChannel.channel_name + "´s URL-File already exist")
    except Exception as e:
        logging.debug(e)
        urlFile = open("data/" + replaceIllegalCharacters(selectedChannel.channel_name) + ".txt", "x")
        urlFile.mode = "rt"
        print(selectedChannel.channel_name + "´s URL-File does not exist, created File")
        logging.info("Created new .txt for" + selectedChannel.channel_name)

    urlFile.close()

    if not urlAlreadyWritten(url, selectedChannel.channel_name):
        urlFile = open("data/" + replaceIllegalCharacters(selectedChannel.channel_name) + ".txt", "a")
        urlFile.writelines(" \n" + url)
        urlFile.close()
        print("Writing URL to " + selectedChannel.channel_name)
        logging.info("Added new URL to " + selectedChannel.channel_name + ":" + url)
    else:
        logging.info("URL: " + url + " already saved in " + selectedChannel.channel_name)
        print("URL is already written")


def writePlaylistURLtoFile(selectedPlaylist: Playlist, url: string):
    try:
        urlFile = open("data/" + replaceIllegalCharacters(selectedPlaylist.title) + ".txt", "rt")
        print(selectedPlaylist.title + "´s URL-File already exist")
    except Exception as e:
        logging.debug(e)
        urlFile = open("data/" + replaceIllegalCharacters(selectedPlaylist.title) + ".txt", "x")
        urlFile.mode = "rt"
        print(selectedPlaylist.title + "´s URL-File does not exist, created File")
        logging.info("Created new .txt for" + selectedPlaylist.title)

    urlFile.close()

    if not urlAlreadyWritten(url, selectedPlaylist.title):
        urlFile = open("data/" + replaceIllegalCharacters(selectedPlaylist.title) + ".txt", "a")
        urlFile.writelines(" \n" + url)
        urlFile.close()
        print("Writing URL to " + selectedPlaylist.title)
        logging.info("Added new URL to " + selectedPlaylist.title + ":" + url)
    else:
        print("URL is already written")
        logging.info("URL: " + url + " already saved in " + selectedPlaylist.title)


def loop():
    channelArray = returnMonitoredChannels()
    playlistArray = returnMonitoredPlaylist()

    for m in range(channelArray.__len__()):
        try:
            checkForNewURLFromChannel(channelArray[m])
        except Exception as e:
            logging.debug(e)
            logging.error("Something went wrong while checkig for new Videos from " + channelArray[m].channel_name)
            print("Oops. Something went wrong while checkig for new Videos")

    for m in range(playlistArray.__len__()):
        try:
            checkForNewURLFromPlaylist(playlistArray[m])
        except Exception as e:
            logging.debug(e)
            logging.error("Something went wrong while checkig for new Videos from " + playlistArray[m].title)
            print("Oops. Something went wrong while checkig for new Videos")


def checkForNewURLFromChannel(selectedChannel: Channel):
    foundNewVid = 0
    logging.info("Searching for new videos of " + selectedChannel.channel_name)
    for n in range(selectedChannel.video_urls.__len__()):
        if not urlAlreadyWritten(selectedChannel.video_urls[n], selectedChannel.channel_name):
             logging.info("Found new video of" + selectedChannel.channel_name + ": " + selectedChannel.video_urls[n])
             print("Found and downloading a new URL from " + selectedChannel.channel_name)
             foundNewVid = foundNewVid + 1
             if returnChannelDir():
                 path="Downloads/" + replaceIllegalCharacters(str(selectedChannel.channel_name))
             else:
                 path="Downloads"
             if returnYTAgent():
                 path="Downloads/[" + str(selectedChannel.channel_id) + "]"
             logging.info("Initiating download of " + selectedChannel.video_urls[n])
             if downloadNewVideo(selectedChannel.video_urls[n], path):
                writeChannelURLtoFile(selectedChannel, selectedChannel.video_urls[n])


def checkForNewURLFromPlaylist(selectedPlaylist: Playlist):
    foundNewVid = 0
    logging.info("Searching for new videos from the playlist " + selectedPlaylist.title)
    for n in range(selectedPlaylist.video_urls.__len__()):
        if not urlAlreadyWritten(selectedPlaylist.video_urls[n], selectedPlaylist.title):
             logging.info("Found new video from the playlist: " + selectedPlaylist.title + ": Link:" + selectedPlaylist.video_urls[n])
             print("Found and downloading a new URL from " + selectedPlaylist.title)
             foundNewVid = foundNewVid + 1
             if returnChannelDir():
                 path="Downloads/" + replaceIllegalCharacters(str(selectedPlaylist.title))
             else:
                 path="Downloads"
             if returnYTAgent():
                 path="Downloads/[" + str(selectedPlaylist.playlist_id) + "]"
             logging.info("Initiating download of " + selectedPlaylist.video_urls[n])
             downloadNewVideo(selectedPlaylist.video_urls[n],path)
             writePlaylistURLtoFile(selectedPlaylist, selectedPlaylist.video_urls[n])


def returnMonitoredChannels():
    try:
        monitoredChannelsFile = open("data/monitoredChannels.txt", "rt")
    except Exception as e:
        logging.debug(e)
        logging.info("monitoredChannels.txt does not seem to exist, creating a new one")
        monitoredChannelsFile = open("data/monitoredChannels.txt", "x")
        monitoredChannelsFile.mode = "r"
        logging.info("monitoredChannels.txt created")

    channelURLs = monitoredChannelsFile.readlines()

    monitoredChannelsFile.close()
    monitoredChannelsArray = [Channel]

    logstr = ""
    for n in range(channelURLs.__len__()):

        if channelURLs[n].__contains__("https://"):
            monitoredChannelsArray.append(Channel(channelURLs[n]))
            logstr = logstr + monitoredChannelsArray[monitoredChannelsArray.__len__()-1].channel_name

    monitoredChannelsArray.pop(0)
    logging.info("Currently monitored channels: " + logstr)
    return monitoredChannelsArray


def returnMonitoredPlaylist():
    try:
        monitoredPlaylistFile = open("data/monitoredPlaylist.txt", "rt")
    except Exception as e:
        logging.debug(e)
        logging.info("monitoredPlaylist.txt does not seem to exist, creating a new one")
        monitoredPlaylistFile = open("data/monitoredPlaylist.txt", "x")
        monitoredPlaylistFile.mode = "r"
        logging.info("monitoredPlaylist.txt created")

    playlistURLs = monitoredPlaylistFile.readlines()

    monitoredPlaylistFile.close()
    monitoredPlaylistArray = [Playlist]
    logstr = ""
    for n in range(playlistURLs.__len__()):

        if  playlistURLs[n].__contains__("https://"):
            monitoredPlaylistArray.append(Playlist(playlistURLs[n]))
            logstr = logstr + monitoredPlaylistArray[monitoredPlaylistArray.__len__() - 1].title

    monitoredPlaylistArray.pop(0)
    logging.info("Currently monitored playlists: " + logstr)
    return monitoredPlaylistArray


def newMonitoredChannel(newChannelURL: string):
    if newChannelURL == "":
        return False

    logging.info("Adding new channel:" + newChannelURL)
    alreadyWritten = False
    try:
        c = Channel(newChannelURL)
        c.channel_url
    except Exception as e:
        logging.debug(e)
        logging.warning("Illegal channel-URL")
        print("URL is not Valid")
        return False
    else:
        cArray = returnMonitoredChannels()

        for n in range(cArray.__len__()):
            if cArray[n].channel_name.__contains__(c.channel_name):
                alreadyWritten = True
                logging.info("Channel already monitored: " + cArray[n].channel_name)
                print("Channel already added")
                break

        if not alreadyWritten:
            monitoredChannelsFile = open("data/monitoredChannels.txt", "a")
            monitoredChannelsFile.write(" \n" + c.channel_url)
            monitoredChannelsFile.close()
            writeChannelURLsToTxt(c)
            logging.info("Added " + newChannelURL + " to monitored channels")
            return True
        else:
            return False


def newMonitoredPlaylist(newPlaylistURL: string):
    if newPlaylistURL == "":
        return False

    logging.info("Adding new playlist:" + newPlaylistURL)
    alreadyWritten = False

    try:
        p = Playlist(newPlaylistURL)
        p.playlist_url
    except Exception as e:
        logging.debug(e)
        logging.warning("Illegal playlist-URL")
        return False
    else:
        pArray = returnMonitoredPlaylist()

        for n in range(pArray.__len__()):
            if pArray[n].playlist_url.__contains__(p.playlist_url):
                alreadyWritten = True
                logging.info("Channel already monitored: " + pArray[n].title)
                print("Playlist already added")
                break

        if not alreadyWritten:
            monitoredPlaylistFile = open("data/monitoredPlaylist.txt", "a")
            monitoredPlaylistFile.write(" \n" + p.playlist_url)
            monitoredPlaylistFile.close()
            writePlaylistURLsToTxt(p)
            logging.info("Added " + newPlaylistURL + " to monitored channels")
            return True
        else:
            return False


def removeMonitoredChannel(oldChannelURL: string):
    logging.info("Removing " + oldChannelURL + "from monitored channels")
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
    logging.info("Removing " + oldPlaylistURL + "from monitored playlists")
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
