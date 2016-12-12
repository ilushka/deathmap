#import twitter
#api = twitter.Api(consumer_key="YzTB78V2Mdv2fx06bFnC3tKc4",
#                  consumer_secret="U0x7ILednvZTdV9OVjamTquqd2TZwduHkpYvY7UHb0e20XlNLk",
#                  access_token_key="547980984-y3q8bbQON6oKnlcQL6DHyjoputD0LoYwqSz4gdrE",
#                  access_token_secret="jMyABFPqh9tcrkA2Uu7TcQW74k7XTzVAF9ADe0Lo0o2DR")
from twitterfeed import TwitterFeed, TwitterPost

feed = TwitterFeed("mercnews")
posts = feed.get_posts()
for p in posts:
  print(p.title)
  print(p.link)
  print(p.date)
marker = feed.get_last_post_marker()
print marker

feed = TwitterFeed(feed_name="mercnews", marker=marker)
posts = feed.get_posts()
for p in posts:
  print(p.title)
  print(p.link)
  print(p.date)
