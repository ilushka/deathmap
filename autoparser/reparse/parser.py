from functions import functions
import reparse
import os

article_titles = ["Attorney: Hayward Target fatal stabbing was self-defense",
  "Mountain View: Motorcyclist killed in crash formally ID'd",
  "Cops: Drunken driver in deadly crash had DUI warrant",
  "Police: Mom driving drunk on Hwy. 101 crashes, injures child",
  "Woman dies, 2 children injured in Colorado chairlift fall:",
  "Cops: Teen accidentally shot in head at East Bay shelter",
  "Barbara Tarbuck of 'General Hospital' dies at 74",
  "DA drops DUI charge for man who tested positive for caffeine",
  "Attorney: Hayward Target fatal stabbing was self-defense",
  "Antioch: City Council watchdog, candidate Karl Dietzel dies",
  "California Highway Patrol plans crackdown of DUIs on New Year's Eve",
  "DA drops DUI charge for man who tested positive for caffeine",
  "Burlingame: Coroner IDs man hit, killed by Caltrain",
  "Alameda: Alameda native, beautician Myra Strehlow dies at 100 in Napa",
  "Cells dripped into the brain help man fight a deadly cancer",
  "Relax, Queen Elizabeth is not dead",
  "Woman dies, 2 children injured in Colo. chairlift fall",
  "Relax, Queen Elizabeth is not dead",
  "Police: One of two men shot near SF Civic Center dies at hospital",
  "WATCH: Brent Burns surprises soda drinkers by crashing digital screen",
  "Man shot dead outside popular restaurant in Mission District",
  "3 men nabbed in fatal November stabbing in SF's Tenderloin",
  "Pittsburg: Pedestrian ID'd in fatal collision; 2016 deadly traffic year for city",
  "WATCH: Brent Burns surprises soda drinkers by crashing digital screen",
  "Sunnyvale: Pedestrian dies after being hit by vehicle on El Camino Real",
  "Man fatally shot in East Oakland",
  "Man shot dead in Oakland",
  "69-year-old woman struck and killed by car in Sunnyvale",
  "69-year-old woman struck and killed by car in Sunnyvale",
  "Bay Point: Car chase ends in crash, arrest",
  "Concord: 74-year-old woman dies in solo-car crash Friday",
  "Homicides in 2016 include two deadly shootings by officers",
  "A Twitter hoax briefly convinced some that Queen Elizabeth II was dead",
  "A Twitter hoax briefly convinced some that Queen Elizabeth II was dead",
  "2 reported dead in New Year's attack on Istanbul nightclub",
  "2 reported dead in New Year's attack on Istanbul nightclub",
  "Agent: 'M*A*S*H' actor William Christopher dead at 84",
  "Marilyn Sachs, SF author and political activist, dies",
  "William Christopher, Father Mulcahy on 'M*A*S*H,' dies at 84",
  "William Christopher, Father Mulcahy on 'M*A*S*H,' dies at 84",
  "Authorities hunt gunman who killed 39 in Istanbul club",
  "Concord: DUI suspected after man hits bicyclist with car",
  "Antioch: One dead, another hurt in New Year's Eve shooting",
  "Good Samaritan saves driver from fiery rollover crash in San Jose.",
  "Good Samaritan saves driver from fiery rollover crash",
  "2 men fatally shot in SF in first killings of 2017",
  "At least 60 inmates killed in prison riot in northern Brazil",
  "At least 60 inmates killed in prison riot in northern Brazil",
  "Man killed in New Year's Eve car wreck in Santa Cruz Mountains",
  "At least 60 inmates killed in Brazil prison riot",
  "Pacheco: Highway 4 crash victim ID'd as Martinez woman",
  "Raiders hoping to have enough healthy bodies for playoff game vs. Texans",
  "Raiders hoping to have enough healthy bodies for playoff game vs. Texans",
  "Cops and Courts: Jan. 3, 2017: Man killed in New Year's Eve",
  "1st bishop indicted in US on sex-abuse claim dies at 83",
  "Raiders hoping to have enough healthy bodies for playoff game",
  "105-year-old orca is missing, presumed dead",
  "Marin County woman accused of trying to fatally stab relative",
  "Oakland: Woman charged with murder in fatal shooting of another woman",
  "Brooklyn train crash injures at least 30",
  "Traffic Alert: One-car crash on Highway 4, major injuries possible",
  "Daryl Spencer, an original San Francisco Giant who made home run history, dies at 88",
  "Saratoga: Woman hit and killed by bus at West Valley College",
  "West Oakland fatal shooting is city's first homicide of 2017",
  "UPDATE Saratoga: Woman hit and killed by Google-contracted bus at West Valley College",
  "BART: Dog found dead on tracks near El Cerrito del Norte Station",
  "BART: Dog found dead on tracks near El Cerrito del Norte Station",
  "Search for couple leads to grim discovery at Hwy. 1 crash",
  "Train crashes at end of platform; 100 people injured",
  "'Daddy's dead?' Chilling 911 call played in church case",
  "Oakland: Mosswood Park fatal stabbing victim identified",
  "Missing Soquel man found dead in Hester Creek",
  "Cops and Courts Jan. 6, 2017: Missing Soquel man found dead in Hester Creek",
  "San Jose: Two shot dead in city's first killings of 2017",
  "2 killed, 1 wounded in shooting at San Jose taqueria:",
  "SJPD: 2 killed, 1 wounded in shooting at taqueria",
  "San Jose: Two shot dead in city's first killings of 2017",
  "SeaWorld: Tilikum, orca that killed trainer, has died",
  "US approves fix for some Volkswagen diesels",
  "UPDATE Shooting at Fort Lauderdale airport leaves multiple people dead",
  "UPDATE Police: 5 dead, 8 injured in shooting at Florida airport",
  "Tilikum, killer whale linked to three human deaths, dies",
  "Dozens of Brazilian inmates killed in 2nd prison riot this week",
  "Man who was pinned between BART car and platform dies",
  "Man who was pinned between BART car, platform dies",
  "Los Gatos man dies after fall from cliff",
  "Bay Area Beat poet David Meltzer dies at age 79",
  "Oakland Beat poet David Meltzer dies at age 79",
  "San Lorenzo man dies in surgery after being trapped between BART cars",
  "San Lorenzo man dies in surgery after being trapped between BART cars",
  "Pinole: Driver of black Charger killed in solo-vehicle crash on I-80 at Appian Way",
  "San Ramon: Woman killed by falling tree at golf course",
  "Woman killed by falling tree on stormy golf course",
  "Norman Rosenberg, toy-store magnate and kids show star, dies",
  "Columnist Nat Hentoff dies at 91",
  "BART: A year goes by, still no leads in fatal shooting on Oakland BART train",
  "BART: A year goes by, still no leads in fatal shooting on Oakland BART train",
  "Bay Area Storm: Heavy rain arrives, two dead, flash-flood warnings in effect",
  "Bay Area Storm: Heavy rain arrives, two dead, flash-flood warnings in effect",
  "SCCSO: Southbound HWY 1 @ the fishhook is down to one lane due to a Vehicle accident",
  "Bay Area wrecks leave at least 1 dead, prompt Oakland water rescue.",
  "Cab driver dies in car plunge into Oakland estuary:",
  "Bay Area wrecks leave at least 1 dead, prompt water rescue",
  "Trial to begin over deadly Oklahoma State homecoming crash",
  "Northbound Lanes of Highway 17 are closed due to an accident at Glenwood Cutoff",
  "Aaaaand, another injury accident on the NB lanes of Highway 17 just below summit. #santacruzstor",
  "Storm death toll hits 3, including woman killed by tree",
  "San Jose: Man, 71, killed by car in city's first traffic fatality of 2017",
  "San Ramon: Woman killed by falling tree identified as travel blogger",
  "San Jose: Taqueria fatal shooting victims identified by authorities",
  "Oakland: Authorities ID man who crashed into estuary near Oakland Airport",
  "Deputy killed while pursuing Orlando suspect",
  "1 man killed when car plunges into Marin County creek",
  "Driver dead in Marin County after car plunges into creek",
  "Driver dead in Marin County after car plunges into creek",
  "CHP: Injury accident on SB Hwy 17 at 12:20 p.m. near Glenwood Drive. Airbags deployed. #santacruzstor",
  "Fremont: Driver in fatal crash on I-880 identified",
  "CHP: New accident on Highway 17 in Scotts Valley, vehicle is in \"turning lane to Timber Ridge.\" Tow truck en route",
  "San Jose man gets prison for bizarre Wal-mart, Chevron crashes that injured 7",
  "Oakland: Authorities ID man who crashed into estuary near Oakland Airport",
  "San Leandro: No charges in fatal stabbing during robbery",
  "San Ramon: Woman killed by falling tree identified as travel blogger",
  "Richmond: Source of diesel spill at Point Isabel investigated",
  "Denver police horse dies after officer forgot he was tied in stall without food or water",
  "Denver police horse dies after officer forgot he was tied in stall without food or water",
  "San Jose man gets prison for bizarre Wal-mart, Chevron crashes that injured 7",
  "Pleasant Hill: Car crashes into building",
  "San Jose: Driver dies in Highway 87 crash near airport"
]

path = os.getcwd() + "/"
parse_title = reparse.parser(
  parser_type = reparse.basic_parser,
  expressions_yaml_path = path + "expressions.yml",
  patterns_yaml_path = path + "patterns.yml",
  functions = functions
)

WEIGHT_THRESHOLD = 15

def total_weight(matches):
  sum = 0
  for m in matches:
    sum += m.weight
  return sum

for a in article_titles:
  matches = parse_title(a)
  if matches is None:
    print "NOT MATCHED: " + a
  elif total_weight(matches) >= WEIGHT_THRESHOLD:
    print "MATCHED: " + a + " " + str(matches) + " " + str(total_weight(matches))
  else:
    print "NOT MATCHED: " + a + " " + str(matches) + " " + str(total_weight(matches))

