from flask import Flask, render_template, jsonify, Response
from flask.ext.bower import Bower
from flask.ext.sqlalchemy import SQLAlchemy
import json
import os

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
Bower(app)
db = SQLAlchemy(app)

class CrashEncoder(json.JSONEncoder):
  def default(self, obj):
    crash = {}
    crash['victims'] = []
    for v in obj.victims:
      crash['victims'].append({
        "first": v.first,
        "last": v.last,
        "age": v.age
      })
    crash['tags'] = []
    for t in obj.tags:
      crash['tags'].append(t.name)
    crash['links'] = []
    for l in obj.links:
      crash['links'].append({
        "name": l.name,
        "link": l.link
      })
    crash['date'] = obj.date.isoformat()
    crash['latitude'] = obj.latitude
    crash['longitude'] = obj.longitude
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
    return '<Crash %s %f %f>' % (self.date, self.latitude, self.longitude)

class Victim(db.Model):
  __tablename__ = "victims"

  id = db.Column(db.Integer, primary_key=True)
  first = db.Column(db.String(64))
  last = db.Column(db.String(64))
  age = db.Column(db.Integer, unique=True)
  crash_id = db.Column(db.Integer, db.ForeignKey('crashes.id'))

  def __init__(self, first, last, age):
    self.first = first
    self.last = last
    self.age = age

  def __repr__(self):
    return '<Victim %s %s %d>' % (self.first, self.last, self.age)

class Link(db.Model):
  __tablename__ = "links"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(256))
  link = db.Column(db.String(512))
  crash_id = db.Column(db.Integer, db.ForeignKey('crashes.id'))

  def __init__(self, name, link):
    self.name = name
    self.link = link

  def __repr__(self):
    return '<Link %s %s>' % (self.name, self.link)

class Tag(db.Model):
  __tablename__ = "tags"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(64))
  crash_id = db.Column(db.Integer, db.ForeignKey('crashes.id'))

  def __init__(self, name):
    self.name = name

  def __repr__(self):
    return '<Tag %s>' % (self.name)

@app.route("/")
def home():
  return render_template("home.html")

@app.route("/data")
def data():
  return Response(response=json.dumps(Crash.query.all(), cls=CrashEncoder),
                  status=200,
                  mimetype="application/json")

if __name__ == "__main__":
  app.run()

