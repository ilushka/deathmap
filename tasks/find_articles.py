from deathmap import db, app
from deathdb import Article, FeedMarker
from twitterfeed import TwitterFeed, TwitterPost

TWITTER_ACCOUNTS = ["mercnews"]

with app.app_context():
  for acc_name in TWITTER_ACCOUNTS:
    # prepare twitter feed
    feed = TwitterFeed("mercnews")
    # retrieve stored marker in db
    dbmarker = db.session.query(FeedMarker).filter_by(feed_name=feed.get_feed_name()).first()
    if dbmarker is not None;
      feed.set_last_post_marker(dbmarker.marker)

    # process all the post since marker
    posts = feed.get_posts()
    for p in posts:
      article = Article(p.title, p.link)
      db.session.add(article)

    # store new marker
    marker = feed.get_last_post_marker()
    if marker is not None:
      print marker
      if dbmarker is None:
        dbmarker = FeedMarker(feed.get_feed_name(), feed.get_last_post_marker())
        db.session.add(dbmarker)     
      else:
        dbmarker.marker = feed.get_last_post_marker()

    db.session.commit()

