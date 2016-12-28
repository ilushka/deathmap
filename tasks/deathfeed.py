class DeathPost(object):
  def __init__(self, title, link, date):
    self.title = title.encode("utf-8")
    self.link = link.encode("utf-8")
    self.date = date

class DeathFeed(object):
  def __init__(self, feed_name, marker):
    self.feed_name = feed_name
    self.marker = marker

  def get_posts(self):
    pass

  def get_feed_name(self):
    return self.feed_name

  def get_last_post_marker(self):
    return self.marker

  def set_last_post_marker(self, marker):
    self.marker = marker

