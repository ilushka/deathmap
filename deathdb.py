from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.types import TypeDecorator, VARCHAR
import json
import dateutil.parser

# NOTE: flask app is set in deathmap.py
db = SQLAlchemy()

# NOTE: use these list_update functions to record db entry changes

def list_intersection_update(a, b):
  for ii in a:
    if ii not in b:
      a.remove(ii)

def list_update(a, b):
  """ move db entries from list b to list a that are not yet in list a """
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
  """ Create JSON object form Crash object """

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
    obj["city"] = crash.city
    obj["state"] = crash.state
    obj["zipcode"] = crash.zipcode
    return obj

class CrashDecoder(Flask.json_decoder):
  """ Create Crash object from JSON object """

  def decode(self, obj):
    # check for required fields
    if obj is None \
        or obj.get("date") is None \
        or obj.get("latitude") is None \
        or obj.get("longitude") is None \
        or obj.get("zipcode", 0) == 0 \
        or len(obj.get("city", "")) == 0 \
        or len(obj.get("state", "")) == 0 \
        or len(obj.get("victims", [])) == 0:
      return None

    # create crash
    try:
      crash = Crash(dateutil.parser.parse(obj["date"]), float(obj["latitude"]),
                    float(obj["longitude"]), obj["city"], obj["state"], obj["zipcode"]);
    except ValueError as err:
      print "Crash Decode Error: " + str(err.args)
      return None

    # add victims (required)
    for v in obj["victims"]:
      # check for required fields in a victim
      try:
        crash.victims.append(Victim(v["first"], v["last"], int(v["age"])))
      except ValueError as err:
        print "Victim Decode Error: " + str(err.args)
    # crash cannot have zero victims
    if len(crash.victims) == 0:
      return None

    # add tags (optional)
    if "tags" in obj:
      for t in obj["tags"]:
        try:
          crash.tags.append(Tag(t))
        except ValueError as err:
          print "Tag Decode Error: " + str(err.args)

    # add links (optional)
    if "links" in obj:
      for l in obj["links"]:
        try:
          crash.links.append(Link(l["name"], l["link"]))
        except ValueError as err:
          print "Link Decode Error: " + str(err.args)

    return crash

class UserDecoder(Flask.json_decoder):
  def decode(self, obj):
    # check for required fields
    if obj is None \
        or len(obj.get("first", "")) == 0 \
        or len(obj.get("last", "")) == 0:
      return None
    info = {}
    if obj.get("twitter") != None:
      info["twitter"] = obj["twitter"]
    return User(None, obj["first"], obj["last"], None, None, info)

class ArticleDecoder(Flask.json_decoder):
  def decode(self, obj):
    # check for required fields
    if obj is None \
        or len(obj.get("title", "")) == 0 \
        or len(obj.get("link", "")) == 0:
      return None
    return Article(obj["title"], obj["link"])
  
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
  created_by = db.relationship("CreatedBy", backref="crash",
                               cascade="all, delete-orphan")
  city = db.Column(db.String(128))
  state = db.Column(db.String(64))
  zipcode = db.Column(db.Integer)

  def __init__(self, datetime, latitude, longitude, city, state, zipcode):
    if datetime is None or latitude == 0 or longitude == 0 \
        or city is None or state is None or zipcode == 0:
      raise ValueError("Wrong parameter for Crash.")
    self.date = datetime
    self.latitude = latitude
    self.longitude = longitude
    self.city = city
    self.state = state
    self.zipcode = zipcode

  def __repr__(self):
    return "<Crash %d %s %f %f>" % (self.id, self.date, self.latitude, self.longitude)

  def update_with_crash(self, other):
    # record column change ony if necessary
    if self.date != other.date:
      self.date = other.date
    if self.latitude != other.latitude:
      self.latitude = other.latitude
    if self.longitude != other.longitude:
      self.longitude = other.longitude
    if self.city != other.city:
      self.city = other.city
    if self.state != other.state:
      self.state = other.state
    if self.zipcode != other.zipcode:
      self.zipcode = other.zipcode
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
    if first is None or last is None \
        or len(first) == 0 or len(last) == 0:
      raise ValueError("Wrong parameter for Victim.")
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
    if name is None or link is None \
        or len(link) == 0 or len(name) == 0:
      raise ValueError("Wrong parameter for Link.")
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
    if name is None or len(name) == 0:
      raise ValueError("Wrong parameter for Tag.")
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
  created_by = db.relationship("CreatedBy", backref="user",
                               cascade="all, delete-orphan")

  def __init__(self, username, first, last, email, password_hash, info):
    self.username = username
    self.first = first
    self.last = last
    self.email = email
    self.password_hash = password_hash
    self.info = info

  def update_info(self, info):
    """ merge two infos """
    # copy current info dictionary
    self.info = dict(self.info)
    for k, v in info.iteritems():
      self.info[k] = v

  def update_with_user(self, other):
    """ update this user obj with data from other obj """
    self.first = other.first
    self.last = other.last
    if other.info is not None:
      self.update_info(other.info)

class CreatedBy(db.Model):
  __tablename__ = "createdby"

  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
  crash_id = db.Column(db.Integer, db.ForeignKey("crashes.id"))
  
  def __init__(self, _user, _crash):
    self.user = _user
    self.crash = _crash

class Article(db.Model):
  __tablename__ = "articles"

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(256))
  link = db.Column(db.String(512))  # TODO: use Link

  def __init__(self, title, link):
    if title is None or link is None \
        or len(title) == 0 or len(link) == 0:
      raise ValueError("Wrong parameter for Article.")
    self.title = title
    self.link = link

  def __repr__(self):
    return "<Article %s %s>" % (self.title, self.link)

  def __eq__(self, other):
    if self.title != other.title:
      return False
    if self.link != other.link:
      return False
    return True

  def __hash__(self):
    return hash(self.link)

class FeedMarker(db.Model):
  __tablename__ = "feedmarkers"

  id = db.Column(db.Integer, primary_key=True)
  feed_name = db.Column(db.String(256))
  marker = db.Column(db.String(256))

  def __init__(self, feed_name, marker):
    if feed_name is None or marker is None \
        or len(feed_name) == 0 or len(marker) == 0:
      raise ValueError("Wrong parameter for FeedMarker.")
    self.feed_name = feed_name
    self.marker = marker

  def __repr__(self):
    return "<FeedMarker %s %s>" % (self.feed_name, self.marker)

  def __eq__(self, other):
    if self.feed_name != other.feed_name:
      return False
    if self.marker != other.marker:
      return False
    return True

  def __hash__(self):
    return hash(self.feed_name)

