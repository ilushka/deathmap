from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.types import TypeDecorator, VARCHAR
import json
import dateutil.parser

db = SQLAlchemy()

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

class JSONData(TypeDecorator):
  """ Custom JSON data type for SQLAlchemy """

  impl = VARCHAR

  def process_bind_param(self, value, dialect):
    if value is not None:
      value = json.dumps(value)
    return value

  def process_result_value(self, value, dialect):
    if value is not None:
      value = json.loads(value)
    return value

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

class User(db.Model):
  __tablename__ = "users"

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64))
  first = db.Column(db.String(64))
  last = db.Column(db.String(64))
  email = db.Column(db.String(254))
  password_hash = db.Column(db.String(192))
  info = db.Column(JSONData())

  def __init__(self, username, first, last, email, password_hash, info):
    self.username = username
    self.first = first
    self.last = last
    self.email = email
    self.password_hash = password_hash
    self.info = info

