from deathmap import db, app, DeathmapUser, duser_to_user, user_to_duser
from deathdb import User

USERNAME  = "ilushka"
PASSWORD  = "password123"
FIRST     = "ilya"
LAST      = "moskovko"
EMAIL     = "ilya@moskovko.com"
INFO      = {"twitter": "jibberboosh"}

with app.app_context():
  db.create_all()

  duser = DeathmapUser(username=USERNAME,
                       first=FIRST,
                       last=LAST,
                       email=EMAIL,
                       info=INFO,
                       password=PASSWORD)
  user = duser_to_user(duser)
  db.session.add(user)
  db.session.commit()

