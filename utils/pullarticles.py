from deathmap import db, app
from deathdb import Article

with app.app_context():
  articles = Article.query.order_by(Article.id)
  for a in articles:
    print a.title

