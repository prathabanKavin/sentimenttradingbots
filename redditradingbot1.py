import praw
import config
from textblob import TextBlob

reddit = praw.Reddit(
    client_id=config.REDDIT_ID,
    client_secret=config.REDDIT_SECRET,
    password=config.REDDIT_PASS,
    user_agent="USERAGENT",
    username=config.REDDIT_USER
)

sentimentList = []
neededSentiments = 300


def Average(lst):
    if len(lst) == 0:
        return len(lst)
    else:
        return sum(lst[-neededSentiments:])/neededSentiments


for comment in reddit.subreddit("bitcoinmarkets").stream.comments():
    redditComment = comment.body
    blob = TextBlob(redditComment)
    sent = blob.sentiment
    print(comment.body)
    print("Sentiment is " + str(sent.polarity))

    if sent.polarity != 0.0:
        sentimentList.append(sent)
        if round(Average(sentimentList)) > 0.5 and len(sentimentList) > neededSentiments:
            print("BUY")
        elif round(Average(sentimentList)) < -0.5 and len(sentimentList) > neededSentiments:
            print("SELL")
