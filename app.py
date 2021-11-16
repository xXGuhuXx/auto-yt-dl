from flask import Flask, render_template, request
from werkzeug.datastructures import ImmutableMultiDict
import pytubDef

app = Flask(__name__)

@app.route('/')
def index():
    channelNames = []
    playlistTitles = []
    channelURLs = []
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
    return render_template("index.html", channels=zipped, playList=zipped1)

@app.route('/settings.html')
def settings():
    return render_template("settings.html", channelDir=pytubDef.returnChannelDir(), interval=pytubDef.returnInterval())

@app.route('/index.html')
def back():
    return index()

@app.route('/', methods=["POST"])
def addChannel():
    monitoredChannels = pytubDef.returnMonitoredChannels()
    monitoredPlaylist = pytubDef.returnMonitoredPlaylist()

    if request.method == "POST":

        for n in range(monitoredChannels.__len__()):
            if request.form == ImmutableMultiDict([(str(monitoredChannels[n].channel_name), 'Remove')]):
                pytubDef.removeMonitoredChannel(str(monitoredChannels[n].channel_url))
                channelNames = []
                channelURLs = []
                monitoredChannels = pytubDef.returnMonitoredChannels()

                for m in range(monitoredChannels.__len__()):
                    channelNames.append(str(monitoredChannels[m].channel_name))
                    channelURLs.append(str(monitoredChannels[m].channel_url))

                playlistTitles = []
                playlistURLs = []

                for m in range(monitoredPlaylist.__len__()):
                    playlistTitles.append(str(monitoredPlaylist[n].title))
                    playlistURLs.append(str(monitoredPlaylist[n].playlist_url))

                zipped = zip(channelNames, channelURLs)
                zipped1 = zip(playlistTitles, playlistURLs)
                return render_template("index.html", channels=zipped, playlist=zipped1)

        for n in range(monitoredPlaylist.__len__()):
            if request.form == ImmutableMultiDict([(str(monitoredPlaylist[n].title), 'Remove')]):
                pytubDef.removeMonitoredChannel(str(monitoredPlaylist[n].playlist_url))
                channelNames = []
                channelURLs = []
                monitoredPlaylist = pytubDef.returnMonitoredPlaylist()

                for m in range(monitoredChannels.__len__()):
                    channelNames.append(str(monitoredChannels[m].channel_name))
                    channelURLs.append(str(monitoredChannels[m].channel_url))

                playlistTitles = []
                playlistURLs = []

                for m in range(monitoredPlaylist.__len__()):
                    playlistTitles.append(str(monitoredPlaylist[n].title))
                    playlistURLs.append(str(monitoredPlaylist[n].playlist_url))

                zipped = zip(channelNames, channelURLs)
                zipped1 = zip(playlistTitles, playlistURLs)
                return render_template("index.html", channels=zipped, playlist=zipped1)

        if request.form["inputSubmit"]:
            newURL = request.form['inputField']
            if pytubDef.newMonitoredChannel(newURL):
                print("Success")
            else:
                print("URL Invalid")

        if request.form["playlistInputSubmit"]:
            newURL = request.form['playlistInputField']
            if pytubDef.newMonitoredPlaylist(newURL):
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
    return render_template("index.html", channels=zipped)

@app.route('/settings.html', methods=["POST"])
def updateSettings():
    if request.method == "POST":
        if request.form.get("IntervalSubmit"):
            pytubDef.updateInterval(int(request.form['Interval']))
        if request.form.get("toggleChannelDir"):
            pytubDef.toggleChannelDir()
        
    return settings()

if __name__=='__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
