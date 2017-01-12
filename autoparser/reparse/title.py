from functions import title_functions
import reparse
import os

WEIGHT_THRESHOLD = 15

path = os.getcwd() + "/"
reparse_title = reparse.parser(
  parser_type = reparse.basic_parser,
  expressions_yaml_path = path + "title_expressions.yml",
  patterns_yaml_path = path + "title_patterns.yml",
  functions = functions
)

def _total_weight(matches):
  sum = 0
  for m in matches:
    sum += m.weight
  return sum

def parse_title(title):
  matches = reparse_title(title)
  if matches is not None and _total_weight(matches) >= WEIGHT_THRESHOLD:
    return title
  return None

