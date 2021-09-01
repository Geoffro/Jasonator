import json
import urllib.request
import os
from pytube import YouTube
import argparse

# Global Constants:
BaseSearchUrl    = 'https://www.googleapis.com/youtube/v3/search?'
BaseVideoUrl     = 'https://www.youtube.com/watch?v='
InvalidURL       = "InvalidURLForm"
ConfigLocation   = "YoutubeConfig.json"
VideoUrlFile     = "YoutubeVideos.json"
DownloadLocation = "YoutubeVids"
ChannelIdFile    = "PatriotChannelIds.json"


def getAPIKeyFromFile(fileName = ConfigLocation):

    with open(fileName, "r") as fin:

        data = json.load(fin)

        return data['apiKey']


def saveVideoUrls(videoList, outfileName = VideoUrlFile):

    with open(outfileName, "w") as fout:

        for vid in videoList:

            try:

                fout.write(f"{vid}\n")

            except:

                print(f"Failed to write {vid}")


def getAllVideoInChannel(channelId, vids):

    apiKey        = getAPIKeyFromFile()
    FirstUrl      = f"{BaseSearchUrl}key={apiKey}&channelId={channelId}&part=snippet,id&order=date&maxResults=25"
    videoLinks    = []
    url           = FirstUrl
    nextPageToken = None

    while True:

        if nextPageToken:

            print(f"New page token {nextPageToken}")

        else:

            print(f"Fetching the base page {url}")

        responseItems = []

        inp = urllib.request.urlopen(url, timeout = 1)

        if not inp:

            break

        resp = json.load(inp)

        if resp and 'items' in resp:

            responseItems = resp['items']

        for i in responseItems:

            if i['id']['kind'] == "youtube#video":

                # Store each video as a dict {url: channelId}
                vidId   = i['id']['videoId']

                if vidId in vids:

                    print(f"Previously saved {vidId} to file, not adding to list")

                else:

                    videoLinks.append(f"{BaseVideoUrl}{vidId}")

        if resp and 'nextPageToken' in resp:

            nextPageToken = resp['nextPageToken']
            url           = f"{FirstUrl}&pageToken={nextPageToken}"

        else:

            break

    saveVideoUrls(videoLinks)


def getVideoGUID(url):

    """
        getVideoGUID()
        Strips the GUID of the url off and returns it as a string.
        Youtube video urls have a form like
            https://www.youtube.com/watch?v=XXXXXXX
        In which case we only want "XXXXXXX"
    """

    if url.find(BaseVideoUrl) == -1:

        print(f"Error: The form of the url doesn't fit the expected form:\n{url}")

        return InvalidURL

    _, guid = url.split("v=")

    for ch in guid:

        if not ch.isalnum():

            # Allow some special chars:
            if ch == "-" or ch == "_":

                continue

            else:

                print(f"Error: The url contains special characters and may create issues:\n{url} caused by {ch}")

                quit()

    return guid


def downloadVideo(url):

    vidGuid = getVideoGUID(url)

    if isFileCached(vidGuid):

        print(f"MP4 at url {url} is already cached", end = "\r")

        return False

    print(f"Going to download {url} with GUID {vidGuid}")

    yt = YouTube(url)

    try:
        # This method will raise an exception if it is called on a video that is unavailable:
        yt.check_availability()

    except:

        print(f"Failed to download {url} because it is unavailable")

        return False

    video = yt.streams.filter().first()

    # We must specify the download location and the file name separately to the function:
    outFile = video.download(output_path = getDownloadLocation(), filename = vidGuid + ".mp4", timeout = 15)

    print(f"{yt.title} has been successfully downloaded and saved to {outFile}")

    return True


def isFileCached(vidGuid):

    location = getDownloadLocation()

    filePath = os.path.join(location, vidGuid + ".mp4")

    return os.path.exists(filePath)


def fetchVideoUrls(channels, vids):

    for name in channels:

        channelId = channels[name]

        print(f"Getting {name} : {channelId}")

        getAllVideoInChannel(channelId, vids)


def loadChannelIdsFromFile():

    """
        loadChannelIdsFromFile() reads the channel ids from a file. He has multiple channels and is likely
        to get banned, so this will check a list of channels.

        NOTE: At any channel page with "user" url from YouTube UI, click a video of the channel (in its "VIDEOS" tab)
        and click the channel name on the video. Then you can get to the page with its "channel"
        url for example https://www.youtube.com/channel/UCkjBZZHGbmZALyUDeVCAwzQ.
    """

    channels = None

    with open(ChannelIdFile, "r") as fin:

        channels = json.load(fin)

        print("Found the following channel info:")

        for key in channels:

            print(f"{key} : {channels[key]}")

    return channels


def getDownloadLocation():

    return os.path.join(os.getcwd(), DownloadLocation)


def getSavedVidLinks():

    """
        countSavedVidsPerChannel() figures out the number of videos per channel and stores this in a dict
    """

    if not os.path.exists(VideoUrlFile):

        return []

    with open(VideoUrlFile, "r") as fin:

        data = []

        for vid in fin:

            data.append(vid.strip())

        return data


def downloadVideos(vids):

    counter = 0

    for vidUrl in vids:

        if downloadVideo(vidUrl):

            counter += 1

    print("")
    print(f"Downloaded {counter} video(s)")


def initDownloadLocation():

    initFilePath(getDownloadLocation())


def initFilePath(f):

    if not os.path.exists(f):

        os.mkdir(f)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--fetchVideoUrls",
                        help   = f"Fetches vids from channels listed in the {ChannelIdFile}",
                        action = "store_true")
    parser.add_argument("--downloadVideos",
                        help   = "Download videos from previously stored urls",
                        action = "store_true")

    args = parser.parse_args()

    if args.fetchVideoUrls:

        channels = loadChannelIdsFromFile()

        vids = getSavedVidLinks()

        fetchVideoUrls(channels, vids)

    elif args.downloadVideos:

        initDownloadLocation()

        vids = getSavedVidLinks()

        downloadVideos(vids)

    else:

        parser.print_help()