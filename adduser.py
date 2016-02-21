from deathmap import db, app, DeathmapUser, user_to_dbuser, dbuser_to_user
from deathdb import User

USERNAME  = "ilya"
PASSWORD  = "password123"
FIRST     = "ilya"
LAST      = "moskovko"
EMAIL     = "ilya@moskovko.com"
INFO      = {"twitter": "jibberboosh"}

with app.app_context():
  db.create_all()

  user = DeathmapUser(username=USERNAME,
                       first=FIRST,
                       last=LAST,
                       email=EMAIL,
                       info=INFO,
                       password=PASSWORD)
  dbuser = user_to_dbuser(user)
  db.session.add(dbuser)
  db.session.commit()

