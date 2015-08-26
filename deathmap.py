from flask import Flask, render_template, jsonify
from flask.ext.bower import Bower
app = Flask(__name__)
app.debug = True
Bower(app)

@app.route("/")
def home():
  return render_template("home.html")

@app.route("/data")
def data():
  data = {
    "data": [{
      "people": [{
        "name": "john doe",
        "age": 60
      }],
      "date": "2015-08-23T6:14:00",
      "location" : {
        "lat": 37.338987,
        "lng": -121.842101
      }, 
      "tags": ["hitnrun", "pedestrian"],
      "links": [
        {
          "title": "MercuryNews",
          "link": "http://www.mercurynews.com/news/ci_28688998/hitandrun-kills-pedestrian-in-san-jose"
        }
      ]
    },
    {
      "people": [{
        "name": "jane doe",
        "age": 34
      }],
      "date": "2015-08-22T23:51:00",
      "location" : {
        "lat": 37.310316,
        "lng": -121.823451
      }, 
      "tags": ["solo", "auto"],
      "links": [
        {
          "title": "MercuryNews",
          "link": "http://www.mercurynews.com/news/ci_28688906/san-jose:-woman-dies-in-us101-crash"
        }
      ]
    },
    {
      "people": [{
        "name": "Stephanie Lopez",
        "age": 30
      }],
      "date": "2015-08-13T00:00:00",
      "location" : {
        "lat": 37.372225,
        "lng": -121.850161
      }, 
      "tags": ["passenger"],
      "links": [
        {
          "title": "MercuryNews",
          "link": "http://www.mercurynews.com/news/ci_28659216/san-jose:-woman-killed-in-highway-101-crash-identified?source=infinite"
        }
      ]
    },
    {
      "people": [{
        "name": "Jane Doe",
        "age": 50
      }],
      "date": "2015-08-16T00:00:00",
      "location" : {
        "lat": 37.998256,
        "lng": -121.810995
      }, 
      "tags": ["pedestrian"],
      "links": [
        {
          "title": "MercuryNews",
          "link": "http://www.mercurynews.com/news/ci_28651148/antioch:-woman-killed-on-highway-4"
        }
      ]
    },
    {
      "people": [{
        "name": "Rachel Shahinian",
        "age": 50,
        "name": "Annika Zinsley",
        "age": 10,
        "name": "Shelia Weeks",
        "age": 59
      }],
      "date": "2015-08-15T16:05:00",
      "location" : {
        "lat": 37.839117,
        "lng": -120.626032
      }, 
      "tags": ["auto"],
      "links": [
        {
          "title": "MercuryNews",
          "link": "http://www.mercurynews.com/news/ci_28680985/chp:-alameda-woman-and-daughter-10-killed-in-traffic-collision"
        },
        {
          "title": "ABC 10 News",
          "link": "http://www.news10.net/story/news/2015/08/15/car-accident--tuolumne-county-sparks-wildfire/31801717/"
        }
      ]
    },
    {
      "people": [{
        "name": "Steven Mi",
        "age": 31
      }],
      "date": "2015-08-14T18:25:00",
      "location" : {
        "lat": 37.592398,
        "lng": -121.886151
      }, 
      "tags": ["bicycle", "auto"],
      "links": [
        {
          "title": "MercuryNews",
          "link": "http://www.mercurynews.com/news/ci_28672816/fremont-bicyclist-struck-killed-on-highway-84"
        }
      ]
    },
    {
      "people": [{
        "name": "Reginald Florence",
        "age": 37
      }],
      "date": "2015-08-14T10:16:00",
      "location" : {
        "lat": 37.769194,
        "lng": -122.218955
      }, 
      "tags": ["amtrak", "train", "pedestrian"],
      "links": [
        {
          "title": "MercuryNews",
          "link": "http://www.mercurynews.com/news/ci_28668479/oakland:-authorities-id-man-fatally-hit-by-train"
        }
      ]
    },
    {
      "people": [{
        "name": "Marilyn Ortega",
        "age": 23,
        "name": "Angel Armijo",
        "age": 24,
        "name": "John Doe",
        "age": 26
      }],
      "date": "2015-08-16T22:00:00",
      "location" : {
        "lat": 37.948737,
        "lng": -122.268848
      }, 
      "tags": ["auto"],
      "links": [
        {
          "title": "The Richmand Standard",
          "link": "http://richmondstandard.com/2015/08/online-fundraisers-started-for-victims-of-san-pablo-dam-road-crash/"
        },
        {
          "title": "Pleasant Hill Patch",
          "link": "http://patch.com/california/pleasanthill/man-28-arrested-contra-costa-co-crash-killed-3"
        }
      ]
    }]
  };
  return jsonify(**data)

if __name__ == "__main__":
  app.run()

