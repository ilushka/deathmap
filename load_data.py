from deathmap import db, Link, Tag, Victim, Crash
import datetime

link = Link("MercuryNews",
            "http://www.mercurynews.com/news/ci_28688998/hitandrun-kills-pedestrian-in-san-jose")
victim = Victim("John", "Doe", 60)
crash = Crash(datetime.datetime(2015, 8, 23, 6, 14),
              37.338987, -121.842101)
crash.victims.append(victim)
crash.tags.append(Tag("hitnrun"))
crash.tags.append(Tag("pedestrian"))
crash.links.append(link)
db.session.add(crash)

link = Link("MercuryNews",
            "http://www.mercurynews.com/news/ci_28688906/san-jose:-woman-dies-in-us101-crash")
victim = Victim("Jane", "Doe", 34)
crash = Crash(datetime.datetime(2015, 8, 22, 23, 51),
              37.310316, -121.823451)
crash.victims.append(victim)
crash.tags.append(Tag("solo"))
crash.tags.append(Tag("auto"))
crash.links.append(link)
db.session.add(crash)

link = Link("MercuryNews",
            "http://www.mercurynews.com/news/ci_28659216/san-jose:-woman-killed-in-highway-101-crash-identified?source=infinite")
victim = Victim("Stephanie", "Lopez", 30)
crash = Crash(datetime.datetime(2015, 8, 13),
              37.372225, -121.850161)
crash.victims.append(victim)
crash.tags.append(Tag("passenger"))
crash.tags.append(Tag("auto"))
crash.links.append(link)
db.session.add(crash)

link = Link("MercuryNews",
            "http://www.mercurynews.com/news/ci_28651148/antioch:-woman-killed-on-highway-4")
victim = Victim("Jane", "Doe", 50)
crash = Crash(datetime.datetime(2015, 8, 16),
              37.998256, -121.810995)
crash.victims.append(victim)
crash.tags.append(Tag("pedestrian"))
crash.links.append(link)
db.session.add(crash)

crash = Crash(datetime.datetime(2015, 8, 14, 18, 25),
              37.592398, -121.886151)
crash.victims.append(Victim("Steven", "Mi", 31))
crash.tags.append(Tag("auto"))
crash.tags.append(Tag("bicycle"))
crash.links.append(
    Link("MercuryNews",
         "http://www.mercurynews.com/news/ci_28672816/fremont-bicyclist-struck-killed-on-highway-84"))
db.session.add(crash)

crash = Crash(datetime.datetime(2015, 8, 14, 10, 16),
              37.769194, -122.218955)
crash.victims.append(Victim("Reginald", "Florence", 37))
crash.tags.append(Tag("train"))
crash.tags.append(Tag("amtrak"))
crash.tags.append(Tag("pedestrian"))
crash.links.append(
    Link("MercuryNews",
         "http://www.mercurynews.com/news/ci_28668479/oakland:-authorities-id-man-fatally-hit-by-train"))
db.session.add(crash)

crash = Crash(datetime.datetime(2015, 8, 16, 22, 0),
              37.948737, -122.268848)
crash.victims.append(Victim("Marilyn", "Ortega", 23))
crash.victims.append(Victim("Angel", "Armijo", 24))
crash.victims.append(Victim("John", "Doe", 26))
crash.tags.append(Tag("auto"))
crash.links.append(
    Link("The Richmand Standard",
         "http://richmondstandard.com/2015/08/online-fundraisers-started-for-victims-of-san-pablo-dam-road-crash/"))
crash.links.append(
    Link("Pleasant Hill Patch",
         "http://patch.com/california/pleasanthill/man-28-arrested-contra-costa-co-crash-killed-3"))
db.session.add(crash)

db.session.commit()

