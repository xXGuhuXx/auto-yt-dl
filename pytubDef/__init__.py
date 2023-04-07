import string
import pytubDef
from configparser import ConfigParser
import logging
from yt_dlp import YoutubeDL

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


def loop():
    playlistArray = returnMonitoredPlaylist()

    for m in range(len(playlistArray)):
        try:
            checkForNewURLFromPlaylist(str(playlistArray[m]))
        except Exception as e:
            logging.debug(e)
            logging.error("Something went wrong while checkig for new Videos from " + playlistArray[m])
            print("Oops. Something went wrong while checkig for new Videos: " + str(e))


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
        file = "data/config.ini"
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


def downloadVideo(video_url, path):
    logging.info("Downloading: " + video_url)
    print("Downloading new Video: " + video_url)
    try:
        if returnYTAgent():
            ydl_opts = {
                'outtmpl': path + "/[" + "%(id)s" + "].mp4", 'cachedir': "data/cache"
            }
        else:
            ydl_opts = {
                'outtmpl': path + "/%(title)s.mp4", 'cachedir': "data/cache"
            }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download(video_url)
    except:
        print("Failed to download video: " + video_url + ". Is it a livestream?")
        return False
    return True


def checkForNewURLFromPlaylist(playlist_url):
    playlist_name = getPlaylistName(playlist_url)
    foundNewVid = 0
    print("Searching for new videos of " + playlist_name)
    logging.info("Searching for new videos of " + playlist_name)
    video_urls = videoURLs(playlist_url)
    for n in range(len(video_urls)):
        if not urlAlreadyWritten(video_urls[n], playlist_name):
            foundNewVid += 1
            if downloadVideo(video_urls[n],
                             compute_path(video_urls[n], playlist_name, getPlaylistID(playlist_url))):
                writeChannelURLtoFile(playlist_name, video_urls[n])


def writeChannelURLtoFile(playlist_name, url: string):
    try:
        urlFile = open("data/" + replaceIllegalCharacters(playlist_name) + ".txt", "rt")
        print(playlist_name + "´s URL-File already exist")
    except Exception as e:
        logging.debug(e)
        urlFile = open("data/" + replaceIllegalCharacters(playlist_name) + ".txt", "x")
        urlFile.mode = "rt"
        print(playlist_name + "´s URL-File does not exist, created File")
        logging.info("Created new .txt for" + playlist_name)

    urlFile.close()

    if not urlAlreadyWritten(url, playlist_name):
        urlFile = open("data/" + replaceIllegalCharacters(playlist_name) + ".txt", "a")
        urlFile.writelines(" \n" + url)
        urlFile.close()
        print("Writing URL to " + playlist_name)
        logging.info("Added new URL to " + playlist_name + ":" + url)
    else:
        logging.info("URL: " + url + " already saved in " + playlist_name)
        print("URL is already written")


def compute_path(url, name, ident):
    logging.info("Found new video of" + name + ": " + url)
    print("Found and downloading a new URL from " + name)
    if returnChannelDir():
        path = "Downloads/" + replaceIllegalCharacters(str(name))
    else:
        path = "Downloads"
    if returnYTAgent():
        path = "Downloads/[" + str(ident) + "]"
    logging.info("Initiating download of " + url)
    return path


def urlAlreadyWritten(url: string, channelName: string):
    urlFile = open("data/" + replaceIllegalCharacters(channelName) + ".txt", "rt")
    endOfFileNotReached = True
    returnBool = False
    while endOfFileNotReached:

        line = urlFile.readline()

        if line == "":
            urlFile.close()
            endOfFileNotReached = False

        if str(url) in str(line):
            endOfFileNotReached = False
            returnBool = True
            urlFile.close()

    return returnBool


def newMonitoredPlaylist(playlist_url: string):
    logging.info("Adding new playlist/channel:" + playlist_url)
    try:
        playlistName = getPlaylistName(playlist_url)
        actualUrl = getPlaylistURL(playlist_url)

        for playlistURLs in returnMonitoredPlaylist():
            if actualUrl in playlistURLs:
                logging.info("Playlist " + playlist_url + " is already monitored (URL in monitoredPlaylist.txt " +
                             playlistURLs + ")")
                print("Playlist " + playlist_url + " is already monitored (URL in monitoredPlaylist.txt " + playlistURLs
                      + ")")
                return False
        monitoredPlaylistFile = open("data/monitoredPlaylist.txt", "a")
        monitoredPlaylistFile.write(" \n" + actualUrl)
        monitoredPlaylistFile.close()
        urlFile = open("data/" + replaceIllegalCharacters(playlistName) + ".txt", "x")
        for video in videoURLs(playlist_url):
            urlFile.write(" \n" + video)
        urlFile.close()
    except Exception as e:
        logging.debug("Something wrent wrong while adding playlist: " + e)
        print("Something wrent wrong while adding playlist: " + e)


def replaceIllegalCharacters(dirtyString: str):
    tmp = dirtyString
    tmp = tmp.replace("<", "").replace(">", "").replace(":", "").replace('"', "").replace("/", "").replace("\\", "")
    return tmp.replace("|", "").replace("?", "").replace("*", "")


def videoURLs(playlist_url):

    ydl_opts = {"extract_flat": True, 'outtmpl': '%(id)s.%(ext)s', 'cachedir': "data/cache"}
    with YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(playlist_url, download=False)

    videos = []
    for n in range(0, len(result["entries"])):
        try:
            for vid in result['entries'][n]['entries']:
                videos.append("https://www.youtube.com/watch?v=" + vid["id"])
        except Exception:
            try:
                videos.append("https://www.youtube.com/watch?v=" + result['entries'][n]["id"])
            except Exception as e:
                print("Could not fetch videos from " + playlist_url + ": " + str(e))
    return videos


def getPlaylistName(playlist_url):
    try:
        file = "data/config.ini"
        config = ConfigParser()
        config.read(file)
        logging.debug("Returning playlist name from config" + str(config[playlist_url]["name"]))
        return config[playlist_url]["name"]
    except Exception as e:
        logging.debug(e)
        logging.info("Config entry for " + playlist_url + "does not seem to exist, creating a new one")
        createPlaylistConfigEntry(playlist_url)
        return getPlaylistName(playlist_url)


def getPlaylistURL(playlist_url):
    ydl_opts = {
        'playlist_items': '1', 'cachedir': "data/cache"
    }
    with YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(playlist_url, download=False)
    return result['webpage_url']


def createPlaylistConfigEntry(url):
    config_object = ConfigParser()
    playlist_data = getPlaylistIDInformation(url)
    config_object[url] = {
        "id": playlist_data[0],
        "name": playlist_data[1],
    }
    with open('data/config.ini', 'a') as conf:
        config_object.write(conf)
    logging.info("New config entry for " + url + " has been created")


def getPlaylistID(playlist_url):
    try:
        file = "data/config.ini"
        config = ConfigParser()
        config.read(file)
        logging.debug("Returning playlist id from config" + str(config[playlist_url]["id"]))
        return config[playlist_url]["id"]
    except Exception as e:
        logging.debug(e)
        logging.info("Config entry for " + playlist_url + "does not seem to exist, creating a new one")
        createPlaylistConfigEntry(playlist_url)
        return getPlaylistID(playlist_url)


def getPlaylistIDInformation(playlist_url):
    information = []
    # Fetch the playlists ID
    ydl_opts = {
        'playlist_items': '1', 'cachedir': "data/cache"
    }
    with YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(playlist_url, download=False)
    information.append(result["entries"][0]["id"])

    # Fetch the playlists Name
    information.append(result['title'])

    return information


def returnMonitoredPlaylist():
    try:
        monitoredPlaylistFile = open("data/monitoredPlaylist.txt", "rt")
    except Exception as e:
        logging.debug(e)
        logging.info("monitoredPlaylist.txt does not seem to exist, creating a new one")
        monitoredPlaylistFile = open("data/monitoredPlaylist.txt", "x")
        monitoredPlaylistFile.mode = "r"
        logging.info("monitoredPlaylist.txt created")

    lines = monitoredPlaylistFile.readlines()
    monitoredPlaylistFile.close()

    playlistURLs = []
    for line in lines:
        if "https://" in line:
            playlistURLs.append(line.replace("\n", "").replace(" ", ""))

    return playlistURLs


def removeMonitoredPlaylist(oldPlaylistURL: string):
    logging.info("Removing " + oldPlaylistURL + "from monitored playlists")
    monitoredPlaylistFile = open("data/monitoredPlaylist.txt", "rt")
    playlistURLs = monitoredPlaylistFile.readlines()
    monitoredPlaylistFile.close()

    for n in range(len(playlistURLs)):
        if oldPlaylistURL in playlistURLs[n]:
            del playlistURLs[n]
            break

    monitoredPlaylistFile = open("data/monitoredPlaylist.txt", "w")
    for n in range(len(playlistURLs)):
        monitoredPlaylistFile.write(playlistURLs[n])