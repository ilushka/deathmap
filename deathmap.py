from flask import Flask, render_template, jsonify, Response, request, json, abort, flash, redirect, url_for, jsonify
from flask.ext.bower import Bower
from flask.ext.login import LoginManager, login_user, logout_user, UserMixin, login_required, fresh_login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import os
from deathdb import db, CrashEncoder, CrashDecoder, Crash, Victim, Link, Tag, User, CreatedBy

# NOTE: LanterneUser's id must be unicode
class DeathmapUser(UserMixin):
    """ Deathmap user"""

    def __init__(self, username, first, last, email, info, password=None, password_hash=None):
        if isinstance(username, unicode):
          self.id = username
        else:
          self.id = unicode(username, "utf-8")
        self.first = first
        self.last = last
        self.email = email
        self.info = info
        if password is not None:
          self.set_password(password)
        if password_hash is not None:
          self.pw_hash = password_hash

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

def user_to_dbuser(user):
  return User(username=user.id,
              first=user.first,
              last=ser.last,
              email=user.email,
              password_hash=user.pw_hash,
              info=user.info)

def dbuser_to_user(dbuser):
  return DeathmapUser(username=dbuser.username,
                      first=dbuser.first,
                      last=dbuser.last,
                      email=dbuser.email,
                      info=dbuser.info,
                      password_hash=dbuser.password_hash)

app = Flask(__name__)
app.debug = True
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
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
    dbuser = User.query.filter_by(username=id).first()
    if dbuser is None:
      return None
    return dbuser_to_user(dbuser)

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

@app.route("/crash/add", methods=["POST"])
@app.route("/crash/<crash_id>/edit", methods=["POST"])
@login_required
def crash_add(crash_id=None):
  new_crash = CrashDecoder().decode(request.json)
  if new_crash is None:
    print "Failed to decode request.json"
    abort(400)

  if crash_id:
    # retrieve and update crash
    crash = db.session.query(Crash).get(crash_id);
    crash.update_crash(new_crash)
  else:
    # add new crash
    dbuser = db.session.query(User).filter_by(username=current_user.id).first()
    cb = CreatedBy(dbuser, new_crash)
    db.session.add(cb)
    db.session.add(new_crash)
  db.session.commit()

  return jsonify({})

@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "POST" \
      and "username" in request.form \
      and "password" in request.form:
    name = request.form["username"]
    password = request.form["password"]
    user = load_user(name)

    if user is None:
      flash("Invalid username.")
    else:
      if user.check_password(password):
        login_user(user)
        flash("Logged in!")
        if request.args.get("next") is not None:
          return redirect(request.args.get("next"))
        else:
          return redirect(url_for("home"))

  if current_user is not None and current_user.is_authenticated:
    return redirect(url_for("home"))
    
  return render_template("login.html")

@app.route("/user", methods=["GET", "POST"])
@login_required
def user():
  dbuser = db.session.query(User).filter_by(username=current_user.id).first()
  if dbuser is None:
    abort(401)

  if request.method == "POST":
    # update first name
    if "firstname" in request.form:
      dbuser.first = request.form["firstname"]
    # update last name
    if "lastname" in request.form:
      dbuser.last = request.form["lastname"]
    # update twitter
    if "twitter" in request.form:
      dbuser.update_info({"twitter": request.form["twitter"]})
    # change password
    if "old-password" in request.form \
        and "new-password" in request.form:
      # check old password
      if current_user.check_password(request.form["old-password"]):
        current_user.set_password(request.form["new-password"])
        dbuser.password_hash = current_user.pw_hash

    db.session.commit()

  return render_template("user.html", current_dbuser=dbuser)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("login"))

if __name__ == "__main__":
  app.run()

