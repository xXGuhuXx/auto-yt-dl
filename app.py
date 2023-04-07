from flask import Flask, render_template, request
from werkzeug.datastructures import ImmutableMultiDict
import pytubDef
import logging

if pytubDef.log():
    logging.basicConfig(filename='data/flaskDebug.log', encoding='utf-8', level=logging.DEBUG)
app = Flask(__name__)


@app.route('/')
def index():
    monitoredPlaylist = pytubDef.returnMonitoredPlaylist()
    monitoredPlaylistTitles = []

    for playlist in monitoredPlaylist:
        monitoredPlaylistTitles.append(pytubDef.getPlaylistName(playlist))

    zipped = zip([], [])
    zipped1 = zip(monitoredPlaylistTitles, monitoredPlaylist)
    return render_template("index.html", channels=zipped, playlist=zipped1)


@app.route('/settings.html')
def settings():
    return render_template("settings.html", channelDir=pytubDef.returnChannelDir(), interval=pytubDef.returnInterval(),
                           ytagent=pytubDef.returnYTAgent())


@app.route('/index.html', methods=["GET", "POST"])
def back():
    return index()


@app.route('/', methods=["GET", "POST"])
def addChannel():
    monitoredPlaylist = pytubDef.returnMonitoredPlaylist()
    monitoredPlaylistTitles = []

    for playlist in monitoredPlaylist:
        monitoredPlaylistTitles.append(pytubDef.getPlaylistName(playlist))

    if request.method == "POST":

        for n in range(monitoredPlaylist.__len__()):
            if request.form == ImmutableMultiDict([(str(monitoredPlaylistTitles[n]), 'Remove')]):
                pytubDef.removeMonitoredPlaylist(str(monitoredPlaylist[n]))
                monitoredPlaylist = pytubDef.returnMonitoredPlaylist()
                monitoredPlaylistTitles = []

                for playlist in monitoredPlaylist:
                    monitoredPlaylistTitles.append(pytubDef.getPlaylistName(playlist))

                zipped = zip([], [])
                zipped1 = zip(monitoredPlaylistTitles, monitoredPlaylist)
                return render_template("index.html", channels=zipped, playlist=zipped1)

        if request.form["inputSubmit"]:
            newURL = request.form['inputField']
            if pytubDef.newMonitoredPlaylist(newURL):
                print("Success")
            else:
                print("URL Invalid")

    monitoredPlaylist = pytubDef.returnMonitoredPlaylist()
    monitoredPlaylistTitles = []

    for playlist in monitoredPlaylist:
        monitoredPlaylistTitles.append(pytubDef.getPlaylistName(playlist))

    zipped = zip([], [])
    zipped1 = zip(monitoredPlaylistTitles, monitoredPlaylist)
    return render_template("index.html", channels=zipped, playlist=zipped1)


@app.route('/settings.html', methods=["POST"])
def updateSettings():
    if request.method == "POST":
        if request.form.get("IntervalSubmit"):
            pytubDef.updateInterval(int(request.form['Interval']))
        if request.form.get("toggleChannelDir"):
            pytubDef.toggleChannelDir()
        if request.form.get("toggleytagent"):
            pytubDef.toggleYtAgent()

    return settings()


if __name__=='__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
