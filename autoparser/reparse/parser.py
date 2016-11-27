from functions import functions
from lxml import html
from functions import Age
import requests
import reparse
import os

EXCERPT_MARGIN = 25

path = os.getcwd() + "/"
age_parser = reparse.parser(
  parser_type = reparse.basic_parser,
  expressions_yaml_path = path + "expressions.yml",
  patterns_yaml_path = path + "patterns.yml",
  functions = functions
)

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

article = get_article("http://www.mercurynews.com/crime-courts/ci_29752248/san-bruno-man-running-traffic-killed-by-hit")
print(article)
print(age_parser(article)[0].get_age())


