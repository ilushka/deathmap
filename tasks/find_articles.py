from deathmap import db, app
from deathdb import Article

with app.app_context():
  article = Article("Foo bar", "http://news.google.com/")
  db.session.add(article)
  db.session.commit()

