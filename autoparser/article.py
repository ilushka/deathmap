from lxml.html import parse
import requests
import re

def _find_popular_xpath(xpaths):
  result = None
  for (k, v) in xpaths.iteritems():
    if result is None or v > result[1]:
      result = (k, v)
  return result

def _count_words(s):
  return len(s.split())

def _get_children_text(root, parent_xpath):
  text = list()
  for p in root.xpath(parent_xpath + '//p'):
    # if p.text is not None and _count_words(p.text) > 1:
    if p.text is not None:
      text.append(p.text)
  return None if len(text) > 0 else text
  
def get_article_body(url):
  parsed = parse(url)
  doc = parsed.getroot()
  ps = doc.xpath('//p')

  p_counts = dict()
  for p in ps:
    parent = p.getparent()
    parent_path = parsed.getpath(parent)
    if parent_path in p_counts:
      p_counts[parent_path] += 1
    else:
      p_counts[parent_path] = 1
    print "parent path: " + parent_path + ", " + str(p_counts[parent_path])

  pop_xpath = _find_popular_xpath(p_count)
  print "most popular xpath: " + str(pop_xpath)

  return _get_children_text(doc, pop_xpath[0])

