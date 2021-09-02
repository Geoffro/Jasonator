# Jasonator

## Setup

### Create a virtual envelope:

    python3 -m venv venv
    source ./venv/bin/activate

### Install libraries:

    pip3 install pytube
    pip3 install praw

## Create accounts for API access

### Google Account Setup

Follow the steps here:

https://developers.google.com/youtube/v3/

Once you are done with that create a json file called YoutubeConfig.json with the following format:

    { 'apiKey': "Your API key obtained above" }

Note: The file is already in the gitignore, so you won't risk accidentally checking yours in.

### Reddit Account Setup

Follow the guide here to setup your API key:

https://www.reddit.com/wiki/api

Create a praw.ini file and put the following info in there:

    [jasonator]
    client_id=<Client ID found above>
    client_secret=<Secret obtained above>
    password=<Your password>
    username=<Your username>





