from lxml import html
import requests
import re

EXCERPT_MARGIN = 25
AGE_REGEX = [
  re.compile(r"(\d\d).year-old"),
  re.compile(r", (\d\d),")
  ]
LOCATION_REGEX = [
  re.compile(r"(Highway \d+)"),
  re.compile(r"\s+((?:north|east|south|west)(?:bound)?)\s+"),
  re.compile(r"(I-\d+)"),
  ]
DATE_REGEX = [
  re.compile(r"(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)"),
  re.compile(r"(\d(?::\d\d)? (?:a\.m\.|p\.m\.))"),
  ]
SEX_REGEX = [
  re.compile(r"(man|woman)"),
  ]

def get_article(url):
  page = requests.get(url)
  tree = html.fromstring(page.content)
  ps = tree.xpath('//div[@id="articleBody"]/p')
  return " ".join(map(lambda a:a.text_content(), ps))
  
def excerpt(article, span):
  start = 0
  if span[0] > EXCERPT_MARGIN:
    start = span[0] - EXCERPT_MARGIN
  end = len(article) - 1
  if (end - span[1]) > EXCERPT_MARGIN:
    end = span[1] + EXCERPT_MARGIN
  return "..." + article[start:end] + "..."

article = get_article("http://www.mercurynews.com/bay-area-news/ci_29795759/crockett-one-dead-traffic-snarled-i-80-after?utm_medium=Social&utm_source=Twitter&utm_campaign=Echobox&utm_term=Autofeed#link_time=1461250080")
#article = get_article("http://www.mercurynews.com/crime-courts/ci_30116648/san-jose-bicyclist-killed-saturday-collision-idd")
