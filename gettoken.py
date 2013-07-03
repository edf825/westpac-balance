#!/usr/bin/python

from getpass import getpass
from sys import exit
from time import time
import os
import requests
import xml.etree.ElementTree as et

# Device id constant that you should probably use between calls
deviceid = 'ffffffffffffffff'
devicename = 'a'
deviceplatform = 'b'
deviceos = 'c'
appversion = 'd'
path = "https://sec.westpac.co.nz/gobal-ui/"
tokenpath = os.path.expanduser("~/.westpac-token")


# Parse the account list xml and return a proper object
def parseAccountsList(xml):
  root = et.fromstring(xml)
  accounts = []

  for product in root:
    account = {}
    for child in product:
      account[child.tag] = child.text
    accounts.append(account)

  return accounts


# Gets the list of accounts. Unfortunately this service requires HTTP basic auth
# otherwise we could just stop here.
def getAccountsList(user, passwd):
  params = { "_" : int(time() * 1000) }

  r = requests.get(path + "productlist/listaccts.xml",
                   params=params, auth=(user, passwd))

  return parseAccountsList(r.text)


def register(user, passwd, num):
  regtext = "<registration>\
             <id>{}</id>\
             <password>{}</password>\
             <deviceId>{}</deviceId>\
             <productNumber>{}</productNumber>\
             <deviceNickname>{}</deviceNickname>\
             <devicePlatform>{}</devicePlatform>\
             <deviceOS>{}</deviceOS>\
             <appVersion>{}</appVersion>\
             </registration>".format(user, passwd, deviceid, num,
                                     devicename, deviceplatform, deviceos, appversion)

  head = {'content-type' : 'application/xml'}

  r = requests.post(path + "registration.xml", data=regtext, headers=head)

  if r.status_code < 200 or r.status_code > 299:
    print "Something went wrong posting registration details."
    print "Status code " + str(r.status_code)
    return

  regroot = et.fromstring(r.text)
  if len(regroot) == 0 or regroot[0].tag != "authenticationToken":
    print "ERROR: Didn't get an authentication token."
    return

  token = regroot[0].text
  query = "{}.xml?deviceId={}&deviceNickname={}&devicePlatform={}&deviceOS={}&appVersion={}"
  
  requests.get(path + token)

  return query.format(token, deviceid, devicename, deviceplatform, deviceos, appversion)


user = raw_input("Username: ")
passwd = getpass("Password: ")

accounts = getAccountsList(user, passwd)

if not accounts:
  print "Could not retreive accounts"
  exit(1)

for account in accounts:
  print '{}: {} {}'.format(account['nickName'], account['availableBalance'], account['balance'])

acct = int(raw_input('Choose an account [0-{}]: '.format(len(accounts))))
token = register(user, passwd, accounts[acct]['productNumber'])

if token:
  with open(tokenpath, 'w') as f:
    f.write(token)
