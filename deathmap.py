from flask import Flask, render_template, jsonify, Response, request, json, abort 
from flask.ext.bower import Bower
from flask.ext.sqlalchemy import SQLAlchemy
import datetime
import dateutil.parser
import os

app = Flask(__name__)
app.debug = True
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
Bower(app)
db = SQLAlchemy(app)

def list_intersection_update(a, b):
  for ii in a:
    if ii not in b:
      a.remove(ii)

def list_update(a, b):
  for ii in b:
    if ii not in a:
      # NOTE:
      b.remove(ii)
      a.append(ii)

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
    obj["id"] = crash.id
    return obj

class CrashDecoder(Flask.json_decoder):
  def decode(self, obj):
    crash = Crash(dateutil.parser.parse(obj["date"]), float(obj["latitude"]),
                  float(obj["longitude"]));
    for v in obj["victims"]:
      crash.victims.append(Victim(v["first"], v["last"], int(v["age"])))
    for t in obj["tags"]:
      crash.tags.append(Tag(t))
    for l in obj["links"]:
      crash.links.append(Link(l["name"], l["link"]))
    return crash
    
class Crash(db.Model):
  __tablename__ = "crashes"

  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.DateTime)
  latitude = db.Column(db.Float)
  longitude = db.Column(db.Float)
  victims = db.relationship("Victim", backref="crashes",
                            cascade="all, delete-orphan")
  links = db.relationship("Link", backref="crashes",
                          cascade="all, delete-orphan")
  tags = db.relationship("Tag", cascade="all, delete-orphan")

  def __init__(self, datetime, latitude, longitude):
    self.date = datetime
    self.latitude = latitude
    self.longitude = longitude

  def __repr__(self):
    return "<Crash %d %s %f %f>" % (self.id, self.date, self.latitude, self.longitude)

  def update_crash(self, other):
    if self.date != other.date:
      self.date = other.date
    if self.latitude != other.latitude:
      self.latitude = other.latitude
    if self.longitude != other.longitude:
      self.longitude = other.longitude
    list_intersection_update(self.victims, other.victims)
    list_update(self.victims, other.victims)
    list_intersection_update(self.tags, other.tags)
    list_update(self.tags, other.tags)
    list_intersection_update(self.links, other.links)
    list_update(self.links, other.links)

class Victim(db.Model):
  __tablename__ = "victims"

  id = db.Column(db.Integer, primary_key=True)
  first = db.Column(db.String(64))
  last = db.Column(db.String(64))
  age = db.Column(db.Integer)
  crash_id = db.Column(db.Integer, db.ForeignKey("crashes.id"))

  def __init__(self, first, last, age):
    self.first = first
    self.last = last
    self.age = age

  def __repr__(self):
    return "<Victim %s %s %d>" % (self.first, self.last, self.age)

  def __eq__(self, other):
    if self.first != other.first:
      return False
    if self.last != other.last:
      return False
    if self.age != other.age:
      return False
    return True

  def __hash__(self):
    return hash(self.first + "_" + self.last + " " + str(self.age))

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

  def __eq__(self, other):
    if self.name != other.name:
      return False
    if self.link != other.link:
      return False
    return True

class Tag(db.Model):
  __tablename__ = "tags"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(64))
  crash_id = db.Column(db.Integer, db.ForeignKey("crashes.id"))

  def __init__(self, name):
    self.name = name

  def __repr__(self):
    return "<Tag %s>" % (self.name)

  def __eq__(self, other):
    if self.name != other.name:
      return False
    return True

@app.route("/")
def home():
  return render_template("home.html")

@app.route("/crash/add")
def add():
  return render_template("add.html")

@app.route("/crash/all/list")
def crash_list():
  return render_template("list.html", crashes=Crash.query.all())

@app.route("/crash/<crash_id>")
def crash(crash_id=None):
  if str(crash_id) == "all":
    return Response(response=json.dumps(Crash.query.all(), cls=CrashEncoder),
                    status=200,
                    mimetype="application/json")

@app.route("/crash/<crash_id>/edit")
def edit(crash_id=None):
  crash = db.session.query(Crash).get(crash_id);
  return render_template("add.html", crash=crash)

@app.route("/crash/<crash_id>", methods=["POST"])
def crash_add(crash_id=None):
  new_crash = CrashDecoder().decode(request.json)
  if crash_id:
    crash = db.session.query(Crash).get(crash_id);
    crash.update_crash(new_crash)
  else:
    db.session.add(new_crash)
  db.session.commit()
  return render_template("add.html")

if __name__ == "__main__":
  app.run()

