from deathmap import db, app
from deathdb import Crash

# NOTE:
# DATABASE_URL=$(heroku config:get DATABASE_URL -a appname) python deletecrash.py

CRASH_ID  = 15

with app.app_context():
  crash = db.session.query(Crash).get(CRASH_ID);
  db.session.delete(crash)
  db.session.commit()

