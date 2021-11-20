import string
import pytubDef
from pytube import Channel
from pytube import YouTube
from pytube import Playlist
from configparser import ConfigParser


def return_interval()->String:
    try:
        file = "data/config.ini"
        config = ConfigParser()
        config.read(file)
        return config["Settings"]["interval"]
    except:
        create_config()
        return return_interval()


def return_channel_dir()->String:
    try:
        file = "data/config.ini"
        config = ConfigParser()
        config.read(file)
        return config.getboolean("Settings", "channelDir")
    except:
        create_config()
        return return_channel_dir()


def update_interval(interval: int)->None:
    if interval > 59:
        try:
            file = "data/config.ini"
            config = ConfigParser()
            config.read(file)
            config.set("Settings", "interval", str(interval))
            with open(file, 'w') as configfile:
                config.write(configfile)
        except:
            create_config()
            update_interval(interval)
    else:
        print("Interval must be atleast 60")


def toggle_channel_dir()->None:
    try:
        file = "data/config.ini"
        config = ConfigParser()
        config.read(file)
        if return_channel_dir():
            config.set("Settings", "channelDir", "False")
        else:
            config.set("Settings", "channelDir", "True")
        with open(file, 'w') as configfile:
            config.write(configfile)
    except:
        create_config()
        toggle_channel_dir()


def create_config()->None:
    config_object = ConfigParser()
    config_object["Settings"] = {
        "interval": "900",
        "channelDir": "True"
    }
    with open('data/config.ini', 'w') as conf:
        config_object.write(conf)


def download_video(video_url, path)->None:
    video = YouTube(video_url)
    print("Downloading new Video: " + str(video.title))
    try:
        video.streams.get_highest_resolution().download(output_path=path)
    except:
        print("Failed to download video: " + str(video.title) + ". Is it a livestream?")

def url_already_written(url: string, channel_name: string)->Boolean:
    url_file = open("data/" + channel_name + ".txt", "rt")
    end_of_file_reached = False
    return_bool = False
    while not end_of_file_reached:

        line = url_file.readline()

        if line == "":
            url_file.close()
            end_of_file_reached = True

        if str(line).__contains__(str(url)):
            end_of_file_reached = True
            return_bool = True
            url_file.close()

    return return_bool


def write_channel_urls_to_txt(selected_channel: Channel)->None:
    try:
        url_file = open("data/" + selected_channel.channel_name + ".txt", "rt")
        print(selected_channel.channel_name + "´s URL-File already exist")
    except:
        url_file = open("data/" + selected_channel.channel_name + ".txt", "x")
        url_file.mode = "rt"
        print(selected_channel.channel_name + "´s URL-File does not exist, created File")

    url_File.close()

    print("Writing URL(s) to " + selected_channel.channel_name)

    for n in range(selected_channel.video_urls.__len__()):

        if not url_already_written(selectedChannel.video_urls[n], selected_channel.channel_name):
            url_file = open("data/" + selected_channel.channel_name + ".txt", "a")
            url_file.writelines(" \n" + str(selected_channel.video_urls[n]))
            url_file.close()


def write_playlist_urls_to_txt(selected_playlist: Playlist)->:
    try:
        url_file = open("data/" + selected_playlist.title + ".txt", "rt")
        print(selected_playlist.title + "´s URL-File already exist")
    except:
        url_file = open("data/" + selected_playlist.title + ".txt", "x")
        url_file.mode = "rt"
        print(selected_playlist.title + "´s URL-File does not exist, created File")

    url_file.close()

    print("Writing URL(s) to " + selected_playlist.title)

    for n in range(selected_playlist.video_urls.__len__()):

        if not url_already_written(selected_playlist.video_urls[n], selected_playlist.title):
            url_file = open("data/" + selected_playlist.title + ".txt", "a")
            url_file.writelines(" \n" + str(selected_playlist.video_urls[n]))
            url_file.close()


def write_channel_url_to_file(selected_channel: Channel, url: string):
    try:
        url_file = open("data/" + selected_channel.channel_name + ".txt", "rt")
        print(selected_channel.channel_name + "´s URL-File already exist")
    except:
        url_file = open("data/" + selected_channel.channel_name + ".txt", "x")
        url_file.mode = "rt"
        print(selected_channel.channel_name + "´s URL-File does not exist, created File")

    url_file.close()

    if not url_already_written(url, selected_channel.channel_name):
        url_file = open("data/" + selected_channel.channel_name + ".txt", "a")
        url_file.writelines(" \n" + url)
        url_file.close()
        print("Writing URL to " + selected_channel.channel_name)
    else:
        print("URL is already written")


def write_playlist_url_to_file(selected_playlist: Playlist, url: string):
    try:
        url_file = open("data/" + selected_playlist.title + ".txt", "rt")
        print(selected_playlist.title + "´s URL-File already exist")
    except:
        url_file = open("data/" + selected_playlist.title + ".txt", "x")
        url_file.mode = "rt"
        print(selected_playlist.title + "´s URL-File does not exist, created File")

    url_file.close()

    if not url_already_written(url, selected_playlist.title):
        url_file = open("data/" + selected_playlist.title + ".txt", "a")
        url_file.writelines(" \n" + url)
        url_file.close()
        print("Writing URL to " + selected_playlist.title)
    else:
        print("URL is already written")


def loop():
    channel_array = return_monitored_channels()
    playlist_array = return_monitored_playlist()

    for m in range(channel_array.__len__()):
        check_for_new_url_from_channel(channel_array[m])

    for m in range(playlist_array.__len__()):
        check_for_new_url_from_playlist(playlist_array[m])


def check_for_new_url_from_channel(selected_channel: Channel):
    for n in range(selected_channel.video_urls.__len__()):
        if not url_already_written(selected_channel.video_urls[n], selected_channel.channel_name):
            print("Found and downloading a new URL from " + selected_channel.channel_name)
            if return_channel_dir():
                path = "Downloads/" + str(selected_channel.channel_name)
            else:
                path = "Downloads"
            download_video(selected_channel.video_urls[n], path)
            write_channel_url_to_file(selected_channel, selected_channel.video_urls[n])


def check_for_new_url_from_playlist(selected_playlist: Playlist):
    for n in range(selected_playlist.video_urls.__len__()):
        if not url_already_written(selected_playlist.video_urls[n], selected_playlist.title):
            print("Found and downloading a new URL from " + selected_playlist.title)
            if return_channel_dir():
                path = "Downloads/" + str(selected_playlist.title)
            else:
                path = "Downloads"
            download_video(selected_playlist.video_urls[n], path)
            write_playlist_url_to_file(selected_playlist, selected_playlist.video_urls[n])


def return_monitored_channels():
    try:
        monitored_channels_file = open("data/monitoredChannels.txt", "rt")
    except:
        monitored_channels_file = open("data/monitoredChannels.txt", "x")
        monitored_channels_file.mode = "r"

    channel_urls = monitored_channels_file.readlines()

    monitored_channels_file.close()
    monitored_channels_array = [Channel]

    for n in range(channelURLs.__len__()):
        if channel_urls[n].__contains__("https://"):
            monitored_channels_array.append(Channel(channel_urls[n]))

    monitored_channels_array.pop(0)
    return monitored_channels_array


def return_monitored_playlist():
    try:
        monitored_playlist_file = open("data/monitoredPlaylist.txt", "rt")
    except:
        monitored_playlist_file = open("data/monitoredPlaylist.txt", "x")
        monitored_playlist_file.mode = "r"

    playlist_urls = monitored_playlist_file.readlines()

    monitored_playlist_file.close()
    monitored_playlist_array = [Playlist]

    for n in range(playlist_urls.__len__()):

        if playlistURLs[n].__contains__("https://"):
            monitored_playlist_array.append(Playlist(playlist_urls[n]))

    monitored_playlist_array.pop(0)
    return monitored_playlist_array


def new_monitored_channel(new_channel_url: string):
    already_written = False
    try:
        c = Channel(new_channel_url)
    except:
        print("URL is not Valid")
        return False
    else:
        channel_array = return_monitored_channels()

        for n in range(channel_array.__len__()):
            if channel_array[n].channel_name.__contains__(c.channel_name):
                already_written = True
                print("Channel already added")
                break

        if not already_written:
            monitored_channels_file = open("data/monitoredChannels.txt", "a")
            monitored_channels_file.write(" \n" + new_channel_url)
            monitored_channels_file.close()
            write_channel_urls_to_txt(c)
            return True
        else:
            return False


def new_monitored_playlist(new_playlist_url: string):
    already_written = False
    try:
        p = Playlist(new_playlist_url)
    except:
        print("URL is not Valid")
        return False
    else:
        playlist_array = return_monitored_playlist()

        for n in range(pArray.__len__()):
            if playlist_array[n].playlist_url.__contains__(p.playlist_url):
                already_written = True
                print("Playlist already added")
                break

        if not already_written:
            monitored_playlist_file = open("data/monitoredPlaylist.txt", "a")
            monitored_playlist_file.write(" \n" + new_playlist_url)
            monitored_playlist_file.close()
            write_playlist_urls_to_txt(p)
            return True
        else:
            return False


def remove_monitored_channel(old_channel_uRL: string):
    monitored_channels_file = open("data/monitoredChannels.txt", "rt")
    channel_urls = monitored_channels_file.readlines()
    monitored_channels_file.close()

    for n in range(channel_urls.__len__()):
        if channel_urls[n].__contains__(old_channel_uRL):
            del channel_urls[n]
            break

    monitored_channels_file = open("data/monitoredChannels.txt", "w")
    for n in range(channel_urls.__len__()):
        monitored_channels_file.write(channel_urls[n])


def remove_monitored_playlist(old_playlist_url: string):
    monitored_playlist_file = open("data/monitoredPlaylist.txt", "rt")
    playlist_urls = monitored_playlist_file.readlines()
    monitored_playlist_file.close()

    for n in range(playlist_urls.__len__()):
        if playlist_urls[n].__contains__(old_playlist_url):
            del playlist_urls[n]
            break

    monitored_playlist_file = open("data/monitoredPlaylist.txt", "w")
    for n in range(playlistURLs.__len__()):
        monitored_playlist_file.write(playlist_urls[n])
