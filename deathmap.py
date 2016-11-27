from flask import Flask, render_template, jsonify, Response, request, json, abort, flash, redirect
from flash import url_for, jsonify
from flask.ext.bower import Bower
from flask.ext.login import LoginManager, login_user, logout_user, UserMixin, login_required
from flash.ext.login import fresh_login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from deathdb import db, CrashEncoder, CrashDecoder, Crash, Victim, Link, Tag, User, CreatedBy
from deathdb import UserDecoder, Article
from functools import wraps
import datetime
import os

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

def login_required_if(is_true):
  def decorator(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if is_true(args, kwargs):
          if current_user is None or not current_user.is_authenticated:
              return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
  return decorator

def user_to_dbuser(user):
  return User(username=user.id,
              first=user.first,
              last=user.last,
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

@app.route("/crash/", methods=["GET"])
@app.route("/crash/<crash_id>/", methods=["GET"])
@app.route("/crash/<crash_id>/<out_type>/", methods=["GET"])
@login_required_if(lambda a, k: not (k.get("crash_id", None) == "all"))
def crash(crash_id=None, out_type="json"):
  # return all crashes
  if str(crash_id) == "all":
    order = ORDER.get(request.args.get('order'), ORDER.get("id"))
    crashes = Crash.query.order_by(order)
    if str(out_type) == "json":
      return Response(response=json.dumps(crashes.all(), cls=CrashEncoder),
                      status=200,
                      mimetype="application/json")
    elif str(out_type) == "html":
      return render_template("list.html", crashes=crashes)

  # return edit page for specific crash
  elif crash_id is not None:
    try:
      crash = db.session.query(Crash).get(int(crash_id));
    except ValueError:
      crash = None
    if crash is None:
      abort(400)
    return render_template("crash.html", crash=crash)

  # return add crash page
  if crash_id is None:
    return render_template("crash.html")

@app.route("/crash/", methods=["POST"])
@app.route("/crash/<crash_id>/", methods=["POST"])
@app.route("/crash/<crash_id>/<out_type>/", methods=["POST"])
@login_required
def edit(crash_id=None, out_type="json"):
  new_crash = CrashDecoder().decode(request.json)
  if new_crash is None:
    print "Failed to decode request.json"
    abort(400)

  # retrieve and update crash
  if crash_id:
    crash = db.session.query(Crash).get(crash_id);
    crash.update_with_crash(new_crash)
  # add new crash
  else:
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
    # update user info
    new_user = UserDecoder().decode(request.json)
    if new_user is None:
      print "Failed to decode request.json"
      abort(400)
    dbuser.update_with_user(new_user)

    # change password
    if len(request.json.get("oldpassword", "")) > 0 \
        and len(request.json.get("newpassword", "")) > 0:
      # check old password
      if current_user.check_password(request.json["oldpassword"]):
        current_user.set_password(request.json["newpassword"])
        dbuser.password_hash = current_user.pw_hash

    db.session.commit()
    return jsonify({})

  return render_template("user.html", current_dbuser=dbuser)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("login"))

@app.route("/articles/", methods=["GET"])
@login_required
def articles():
  # return all articles
  articles = Article.query.order_by(Article.id)
  return render_template("articles.html", articles=articles)

if __name__ == "__main__":
  app.run()

