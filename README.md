# Welcome to auto-yt-dl!

This docker is specifically used to automatically download new Videos of specific YouTube Channels. It features
a Web Gui to add and remove Channels from your watch list. It was tested and build to run on unRaid.

NOTE: This docker will not download all videos of a Channel only newly added videos.

## How to install

To install auto-yt-dl run:  docker run -p 5000:5000 \ -name auto-yt-dl \

WARNING: This has not been tested on all systems.

>docker run -d --name='auto-yt-dl' --net='bridge' --privileged=false -p '5000:5000/tcp' -v '/test':'/app/Downloads':'rw' 'xxguhuxx/yt-channel-dl:latest'

## How to use
After the docker is started you´ll be able to access the Web Gui on [ipOfYourMachine]:5000.
Enter a Channel URL and press "Add". The Channel Name and URL should now be listed below the input field.
To remove a Channel press "Remove"

## How does it work
This docker utilizes pytube. When add an Channel it will fetch all Video URLs of that Channel and save it.
Every 15 minutes it uses the already saved URL to check if a new video is accessible.
It not find new videos immediately, but usually it should take no longer than 30 minutes.

PS: It might be obvious that this is my first docker and every tricks & tips are greatly appreciated!

