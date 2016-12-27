from deathfeed import DeathPost, DeathFeed
import twitter

class TwitterPost(DeathPost):
  def __init__(self, status):
    self.tweet = status
    link = "about:blank"
    if len(self.tweet.urls) > 0:
      link = self.tweet.urls[0].expanded_url
    super(TwitterPost, self).__init__(title=self.tweet.text,
                                      link=link,
                                      date=self.tweet.created_at)

class TwitterFeed(DeathFeed):
  def __init__(self, feed_name, marker=None):
    super(TwitterFeed, self).__init__(feed_name, marker)
    self.api = twitter.Api(consumer_key="YzTB78V2Mdv2fx06bFnC3tKc4",
                           consumer_secret="U0x7ILednvZTdV9OVjamTquqd2TZwduHkpYvY7UHb0e20XlNLk",
                           access_token_key="547980984-y3q8bbQON6oKnlcQL6DHyjoputD0LoYwqSz4gdrE",
                           access_token_secret="jMyABFPqh9tcrkA2Uu7TcQW74k7XTzVAF9ADe0Lo0o2DR")

  def get_posts(self):
    posts = []
    self.timeline = self.api.GetUserTimeline(screen_name=self.feed_name,
                                             since_id=int(self.marker),
                                             include_rts=False)
    for s in self.timeline:
      posts.append(TwitterPost(s))
    if len(posts) > 0:
      self.marker = str(posts[0].tweet.id)
    return posts

