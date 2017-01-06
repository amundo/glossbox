#!/usr/bin/python2.7
import json

"""
toolbox2json.py

A simple approach to converting a Toolbox file to LaTeX output
suitable for gloss rendering with expex.

Usage: 

  $ python toolbox2json.py <input_file.txt>

For example, if you have a input file called Toolbox_test.txt,
you can run:

  $ python toolbox2json.py Toolbox_test.txt

...And array of objects will be printed to the terminal with one
IU per object.

"""

def strip_prolog_and_postlog(content):
  return content.strip().split('\n\n')[1:-1]

def analyze_toolbox_line(line):
  key = line.split()[0].replace('\\','')
  content = ' '.join(line.split()[1:])
  return (key, content)

def process_iu(iu):
  iu_object = {}
  lines = iu.strip().splitlines()
  for line in lines:
    key, content = analyze_toolbox_line(line)
    iu_object[key] = content
  return iu_object

def toSeconds(HMSm):
    HMSm = HMSm.replace('.', ' ').replace(':', ' ').split(' ')
    H, M, S, m = HMSm
    return float(H) * 3600 + float(M) * 60 + float(S) + float(m) / 1000.0

def convert_timestamps(iu):
  if 'ELANBegin' not in iu or 'ELANBegin' not in iu: 
    print iu; exit()
  #iu["ELANBegin"] = float(iu["ELANBegin"])
  #iu["ELANEnd"] = float(iu["ELANEnd"])
  iu["ELANBeginStamp"] = iu["ELANBegin"]
  iu["ELANEndStamp"] = iu["ELANEnd"]
  iu["ELANBegin"] = toSeconds(iu["ELANBegin"])
  iu["ELANEnd"] = toSeconds(iu["ELANEnd"])
  return iu

def toolbox2json(content):
  """
  Reads content of a toolbox file (as a Unicode string)
  and convert into an array of objects representing IUs
  """
  ius = strip_prolog_and_postlog(content)
  ius = [process_iu(iu) for iu in ius]
  ius = [convert_timestamps(iu) for iu in ius]
  return ius

if __name__ == "__main__":
  import sys
  toolbox_file = sys.argv[1]
  content = open(toolbox_file, 'U').read().decode('utf-8')
  print json.dumps(toolbox2json(content), indent=2)
