from flask import Flask, render_template, jsonify, Response, request, json 
from flask.ext.bower import Bower
from flask.ext.sqlalchemy import SQLAlchemy
import datetime
import os

app = Flask(__name__)
app.debug = True
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
Bower(app)
db = SQLAlchemy(app)

class CrashEncoder(Flask.json_encoder):
  def default(self, crash):
    obj = {}
    obj["victims"] = []
    for v in crash.victims:
      obj["victims"].append({
        "first": v.first,
        "last": v.last,
        "age": v.age
      })
    obj["tags"] = []
    for t in crash.tags:
      obj["tags"].append(t.name)
    obj["links"] = []
    for l in crash.links:
      obj["links"].append({
        "name": l.name,
        "link": l.link
      })
    obj["date"] = crash.date.isoformat()
    obj["latitude"] = crash.latitude
    obj["longitude"] = crash.longitude
    return obj

class CrashDecoder(Flask.json_decoder):
  def decode(self, obj):
    crash = Crash(obj["date"], obj["latitude"], obj["longitude"]);
    for v in obj["victims"]:
      crash.victims.append(Victim(v["first"], v["last"], v["age"]))
    for t in obj["tags"]:
      crash.tags.append(Tag(t))
    for l in obj["links"]:
      crash.links.append(Link(l["name"], l["link"]))
    return crash
    
class Crash(db.Model):
  __tablename__ = "crashes"

  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.DateTime, unique=True)
  latitude = db.Column(db.Float, unique=True)
  longitude = db.Column(db.Float, unique=True)
  victims = db.relationship("Victim", backref="crashes")
  links = db.relationship("Link", backref="crashes")
  tags = db.relationship("Tag")

  def __init__(self, datetime, latitude, longitude):
    self.date = datetime
    self.latitude = latitude
    self.longitude = longitude

  def __repr__(self):
    return "<Crash %s %f %f>" % (self.date, self.latitude, self.longitude)

class Victim(db.Model):
  __tablename__ = "victims"

  id = db.Column(db.Integer, primary_key=True)
  first = db.Column(db.String(64))
  last = db.Column(db.String(64))
  age = db.Column(db.Integer, unique=True)
  crash_id = db.Column(db.Integer, db.ForeignKey("crashes.id"))

  def __init__(self, first, last, age):
    self.first = first
    self.last = last
    self.age = age

  def __repr__(self):
    return "<Victim %s %s %d>" % (self.first, self.last, self.age)

class Link(db.Model):
  __tablename__ = "links"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(256))
  link = db.Column(db.String(512))
  crash_id = db.Column(db.Integer, db.ForeignKey("crashes.id"))

  def __init__(self, name, link):
    self.name = name
    self.link = link

  def __repr__(self):
    return "<Link %s %s>" % (self.name, self.link)

class Tag(db.Model):
  __tablename__ = "tags"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(64))
  crash_id = db.Column(db.Integer, db.ForeignKey("crashes.id"))

  def __init__(self, name):
    self.name = name

  def __repr__(self):
    return "<Tag %s>" % (self.name)

@app.route("/")
def home():
  return render_template("home.html")

@app.route("/crash/add")
def add():
  return render_template("add.html")

@app.route("/crash/all/list")
def crash_list():
  return render_template("list.html")

@app.route("/crash/<crash_id>")
def crash(crash_id=None):
  if str(crash_id) == "all":
    return Response(response=json.dumps(Crash.query.all(), cls=CrashEncoder),
                    status=200,
                    mimetype="application/json")

@app.route("/crash", methods=["POST"])
def crash_add():
    crash = CrashDecoder().decode(request.json)
    db.session.add(crash)
    db.session.commit()
    return render_template("add.html")


if __name__ == "__main__":
  app.run()

