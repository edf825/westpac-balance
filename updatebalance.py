#!/usr/bin/python

from time import time
import os
import requests
import xml.etree.ElementTree as et

path = "https://sec.westpac.co.nz/gobal-ui/"
tokenpath = os.path.expanduser("~/.westpac-token")
balancepath = os.path.expanduser("~/.westpac-balance")

try:
  f = open(tokenpath, "r")
except:
  exit(1)

url = "{}balance/{}&_={}".format(path, f.readline(), int(time() * 1000))

r = requests.get(url)

text = ""

if r.status_code < 200 or r.status_code > 299:
  print "ERROR: Server returned status code " + str(r.status_code)
  text = "$$$E" + str(r.status_code)

balance = {}
balxml = et.fromstring(r.text)
for i in balxml:
  if i.tag != "product":
    continue
  for j in i:
    balance[j.tag] = j.text

text = "$" + balance["availableBalance"]

f = open(balancepath, "w")
f.write(text)
f.close()
