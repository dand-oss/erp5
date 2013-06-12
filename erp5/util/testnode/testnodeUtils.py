import sys
import json
import shutil
import string

def deunicodeData(data):
  if isinstance(data, int):
    new_data = data
  elif isinstance(data, str):
    new_data = data
  elif isinstance(data, list):
    new_data = []
    for sub_data in data:
      new_data.append(deunicodeData(sub_data))
  elif isinstance(data, unicode):
    new_data = data.encode('utf8')
  elif isinstance(data, dict):
    new_data = {}
    for key, value in data.iteritems():
      key = deunicodeData(key)
      value = deunicodeData(value)
      new_data[key] = value
  else:
    new_data = data
  return new_data
