from flask import Flask, render_template, jsonify, Response, request, json, abort, flash, redirect, url_for
from flask.ext.bower import Bower
from flask.ext.login import LoginManager, login_user, logout_user, UserMixin, login_required, fresh_login_required
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import dateutil.parser
import os
from deathdb import db, CrashEncoder, CrashDecoder, Crash, Victim, Link, Tag 


# NOTE: LanterneUser's id must be unicode
class DeathmapUser(UserMixin):
    """ Deathmap user"""

    def __init__(self, name, password):
        self.name = name
        self.id = name
        self.set_password(password)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

app = Flask(__name__)
app.debug = True
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["USERS"] = {
    u"admin": DeathmapUser(u"admin", u"CREAMcgtmddby")
}
app.secret_key = "i am a secret"
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
Bower(app)
db.init_app(app)

# NOTE: How to add functions to templates:
#
# @app.context_processor
# def utility_processor():
#   def is_authenticated():
#     return not login_manager.unauthorized()
#   return dict(is_authenticated=is_authenticated)

@login_manager.user_loader
def load_user(id):
    return app.config["USERS"][id]

ORDER = {
  "id": Crash.id,
  "date": Crash.date
}

@app.route("/")
def home():
  return render_template("home.html")

@app.route("/crash/<crash_id>")
@app.route("/crash/<crash_id>/<out_type>")
def crash(crash_id=None, out_type="json"):
  order = ORDER.get(request.args.get('order'), ORDER.get("id"))
  crashes = Crash.query.order_by(order)
  if str(crash_id) == "all":
    if str(out_type) == "json":
      return Response(response=json.dumps(crashes.all(), cls=CrashEncoder),
                      status=200,
                      mimetype="application/json")
    elif str(out_type) == "html":
      return render_template("list.html", crashes=crashes)

@app.route("/crash/add")
@login_required
def add():
  return render_template("add.html")

@app.route("/crash/<crash_id>/edit")
@login_required
def edit(crash_id=None):
  crash = db.session.query(Crash).get(crash_id);
  return render_template("add.html", crash=crash)

@app.route("/crash", methods=["POST"])
@app.route("/crash/<crash_id>", methods=["POST"])
@login_required
def crash_add(crash_id=None):
  new_crash = CrashDecoder().decode(request.json)
  if crash_id:
    crash = db.session.query(Crash).get(crash_id);
    crash.update_crash(new_crash)
  else:
    db.session.add(new_crash)
  db.session.commit()
  return render_template("add.html")

@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "POST" \
      and "username" in request.form \
      and "password" in request.form:
    name = request.form["username"]
    password = request.form["password"]
    if name in app.config["USERS"].keys():
        user = app.config["USERS"][name]
        if user.check_password(password):
          login_user(user)
          flash("Logged in!")
          return redirect(request.args.get("next"))
    else:
        flash("Invalid username.")
  return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("login"))

if __name__ == "__main__":
  app.run()

