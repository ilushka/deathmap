import re
import sys
from deathmap import db, app
from deathdb import Article, FeedMarker
from twitterfeed import TwitterFeed, TwitterPost
from autoparser.reparse.title import get_title_weight

TWITTER_ACCOUNTS = ["mercnews", "sfgate", "eastbaytimes", "scsentinel"]
DEBUG = False

def title_matches(title):
  return re.search("dies|fatal|dead|killed|crash|accident|DUI|dead", title)

with app.app_context():
  for acc_name in TWITTER_ACCOUNTS:
    # prepare twitter feed
    feed = TwitterFeed(acc_name)
    # retrieve stored marker in db
    if DEBUG:
      dbmarker = None
    else:
      dbmarker = db.session.query(FeedMarker).filter_by(feed_name=feed.get_feed_name()).first()
    if dbmarker is not None:
      feed.set_last_post_marker(dbmarker.marker)

    # process all the posts since marker
    posts = reversed(feed.get_posts())  # add oldest posts first
    for p in posts:
      if title_matches(p.title):
        article = Article(p.title, p.link, get_title_weight(p.title))
        if DEBUG:
          print "matched article: " + p.title + " " + get_title_weight(p.title)
        else:
          db.session.add(article)

    # store new marker
    marker = feed.get_last_post_marker()
    if marker is not None:
      if DEBUG:
        print "marker: " + feed.get_feed_name() + " - " + marker
      else:
        if dbmarker is None:
          dbmarker = FeedMarker(feed.get_feed_name(), marker)
          db.session.add(dbmarker)     
        else:
          dbmarker.marker = marker

    if not DEBUG:
      db.session.commit()

