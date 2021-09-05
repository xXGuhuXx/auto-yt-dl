from flask import Flask, render_template, request
from werkzeug.datastructures import ImmutableMultiDict
import pytubDef

app = Flask(__name__)

@app.route('/')
def index():
    channelNames = []
    channelURLs = []
    monitoredChannels = pytubDef.returnMonitoredChannels()

    for n in range(monitoredChannels.__len__()):
        channelNames.append(str(monitoredChannels[n].channel_name))
        channelURLs.append(str(monitoredChannels[n].channel_url))

    zipped = zip(channelNames, channelURLs)
    return render_template("templates/index.html", channels=zipped)


@app.route('/', methods=["POST"])
def addChannel():
    monitoredChannels = pytubDef.returnMonitoredChannels()

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

                zipped = zip(channelNames, channelURLs)
                return render_template("templates/index.html", channels=zipped)

        if request.form["inputSubmit"]:
            print("i")
            newURL = request.form['inputField']
            if pytubDef.newMonitoredChannel(newURL):
                print("Success")
            else:
                print("URL Invalid")

    channelNames = []
    channelURLs = []
    monitoredChannels = pytubDef.returnMonitoredChannels()

    for n in range(monitoredChannels.__len__()):
        channelNames.append(str(monitoredChannels[n].channel_name))
        channelURLs.append(str(monitoredChannels[n].channel_url))

    zipped = zip(channelNames, channelURLs)
    return render_template("templates/index.html", channels=zipped)


if __name__=='__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
