import praw

BotName          = "jasonator"
UserAgentStr     = "Bot to upload jasons videos"
SubredditName    = "PatriotPartyPodcast"

class RedditBot:


    def __init__(self, botName = BotName, userAgentStr = UserAgentStr):

        self.reddit = praw.Reddit(botName, user_agent=userAgentStr)


    def uploadVid(self, fileName, submissionTitle):

        self.reddit.subreddit(SubredditName).submit_video(submissionTitle, fileName)


if __name__ == "__main__":

    bot = RedditBot()

    bot.uploadVid("./YoutubeVids/0ZxyziQzmi4.mp4", "Test")

