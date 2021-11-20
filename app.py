from flask import Flask, render_template, request
from werkzeug.datastructures import ImmutableMultiDict
import pytubDef

app = Flask(__name__)

@app.route('/')
def index():
    channel_names = []
    playlist_titles = []
    channel_urls = []
    playlist_urls = []
    monitored_channels = pytubDef.return_monitored_channels()
    monitored_playlist = pytubDef.return_monitored_playlist()

    for n in range(monitored_channels.__len__()):
        channel_names.append(str(monitored_channels[n].channel_name))
        channel_urls.append(str(monitored_channels[n].channel_url))

    for n in range(monitored_playlist.__len__()):
        playlist_titles.append(str(monitored_playlist[n].title))
        playlist_urls.append(str(monitored_playlist[n].playlist_url))

    zipped = zip(channel_names, channel_urls)
    zipped1 = zip(playlist_titles, playlist_urls)
    return render_template("index.html", channels=zipped, playlist=zipped1)

@app.route('/settings.html')
def settings():
    return render_template("settings.html", channelDir=pytubDef.return_channel_dir(), interval=pytubDef.return_interval())

@app.route('/index.html', methods=["GET", "POST"])
def back():
    return index()

@app.route('/', methods=["GET", "POST"])
def add_channel():
    monitored_channels = pytubDef.return_monitored_channels()
    monitored_playlist = pytubDef.return_monitored_playlist()

    if request.method == "POST":

        for n in range(monitored_channels.__len__()):
            if request.form == ImmutableMultiDict([(str(monitored_channels[n].channel_name), 'Remove')]):
                pytubDef.remove_monitored_channel(str(monitored_channels[n].channel_url))
                channel_names = []
                channel_urls = []
                monitored_channels = pytubDef.return_monitored_channels()

                for m in range(monitored_channels.__len__()):
                    channel_names.append(str(monitored_channels[m].channel_name))
                    channel_urls.append(str(monitored_channels[m].channel_url))

                playlist_titles = []
                playlist_urls = []

                for m in range(monitored_playlist.__len__()):
                    playlist_titles.append(str(monitored_playlist[n].title))
                    playlist_urls.append(str(monitored_playlist[n].playlist_url))

                zipped = zip(channel_names, channel_urls)
                zipped1 = zip(playlist_titles, playlist_urls)
                return render_template("index.html", channels=zipped, playlist=zipped1)

        for n in range(monitored_playlist.__len__()):
            if request.form == ImmutableMultiDict([(str(monitored_playlist[n].title), 'Remove')]):
                pytubDef.remove_monitored_playlist(str(monitored_playlist[n].playlist_url))
                channel_names = []
                channel_urls = []
                monitored_playlist = pytubDef.remove_monitored_playlist()

                for m in range(monitored_channels.__len__()):
                    channel_names.append(str(monitored_channels[m].channel_name))
                    channel_urls.append(str(monitored_channels[m].channel_url))

                playlist_titles = []
                playlist_urls = []

                for m in range(monitored_playlist.__len__()):
                    playlist_titles.append(str(monitored_playlist[n].title))
                    playlist_urls.append(str(monitored_playlist[n].playlist_url))

                zipped = zip(channel_names, channel_urls)
                zipped1 = zip(playlist_titles, playlist_urls)
                return render_template("index.html", channels=zipped, playlist=zipped1)

        if request.form["inputSubmit"]:
            newURL = request.form['inputField']
            if pytubDef.newMonitoredChannel(newURL):
                print("Success")
            elif pytubDef.newMonitoredPlaylist(newURL):
                print("Success")
            else:
                print("URL Invalid")

    channelNames = []
    channelURLs = []
    playlistTitles = []
    playlistURLs = []
    monitoredChannels = pytubDef.returnMonitoredChannels()
    monitoredPlaylist = pytubDef.returnMonitoredPlaylist()

    for n in range(monitoredChannels.__len__()):
        channelNames.append(str(monitoredChannels[n].channel_name))
        channelURLs.append(str(monitoredChannels[n].channel_url))

    for n in range(monitoredPlaylist.__len__()):
        playlistTitles.append(str(monitoredPlaylist[n].title))
        playlistURLs.append(str(monitoredPlaylist[n].playlist_url))

    zipped = zip(channelNames, channelURLs)
    zipped1 = zip(playlistTitles, playlistURLs)
    return render_template("index.html", channels=zipped, playlist=zipped1)

@app.route('/settings.html', methods=["POST"])
def update_settings():
    if request.method == "POST":
        if request.form.get("IntervalSubmit"):
            pytubDef.update_interval(int(request.form['Interval']))
        if request.form.get("toggleChannelDir"):
            pytubDef.toggle_channel_dir()
        
    return settings()

if __name__=='__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
