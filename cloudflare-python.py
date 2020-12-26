#!/usr/bin/env python3 
import sys
import os
import requests
import json


# version 2020122702




headers = {
    'Content-Type':  'application/json'
}


with  open('creds.json') as e:
    data = json.load(e)

headers["X-Auth-Email"] = data["X-Auth-Email"]
headers["X-Auth-Key"]   = data["X-Auth-Key"]



def add(zone,record,ipaddr): 
    data = {
        "type":     "A",
        "ttl":      "120", 
        "priority": 10, 
        "proxied":  False
    }
    data['name']    = record
    data['content'] = ipaddr
    url = 'https://api.cloudflare.com/client/v4/zones/{}/dns_records'.format(str(get_zone_id(zone)))
    r = requests.post(url, headers=headers, json=data)
    result = r.json()['success']
    print('Cloudflare result: {}'.format(result))
    if result == False:
        print(r.json()['errors'][0]['message'])

def get_zone_id(zone):
    url = 'https://api.cloudflare.com/client/v4/zones'
    r = requests.get(url, headers=headers,  json="")
    for i in r.json()["result"]:
        if i.get("name") == zone:
            return(i.get("id"))


def get_all_dns_records(zone):
    url = 'https://api.cloudflare.com/client/v4/zones/{}/dns_records'.format(str(get_zone_id(zone)))
    r = requests.get(url, headers=headers, json="")
    return(r.json())


def pr(n):
    return(' ' * n)


def get_a_dns_records(zone): 
    url = 'https://api.cloudflare.com/client/v4/zones/{}/dns_records'.format(str(get_zone_id(zone)))
    r = requests.get(url, headers=headers, json="")

    list = []
    for i in r.json().get("result"):
        type = i.get('type')
        if type == "A":
            list.append(i.get("name"))

    def maxlen(list):
       x = 1
       for i in list:
           num = len(i)
           if num > x:
               x = num
       x += 1
       return(x)

    for i in r.json().get("result"):
        name = i.get('name')
        type = i.get('type')
        content = i.get('content')
        if type == "A":
            add = maxlen(list) - len(name)
            interval = pr(add)
            print('{0}{1}{2} {3}'.format(name,interval,type,content))
    return(r.json())


def get_dns_record_id(zone,record):
    all_recs = get_all_dns_records(zone)
    for i in all_recs.get("result"):
        name = i["name"]
        id   = i["id"]
        if name == record:
            return(id)

def delete(record,zone):
    print('now delete zone'.format(record))
    zone_id = str(get_zone_id(zone))
    dns_record_id = get_dns_record_id(zone,record)
    url = "https://api.cloudflare.com/client/v4/zones/{}/dns_records/{}".format(zone_id,dns_record_id)
    r = requests.delete(url, headers=headers, json="")
    print(r.json())



def get_all_zones_list():
    url = 'https://api.cloudflare.com/client/v4/zones'
    r = requests.get(url, headers=headers, json="")
    for i in r.json()["result"]:
        print(i["name"])


def help():
    print('./cloudflare-python.py add       subdomain.yourDomain.com 8.8.8.8')
    print('./cloudflare-python.py del       subdomain.yourDomain.com ')
    print('./cloudflare-python.py get_all_a yourDomain.com ')
    print('./cloudflare-python.py get_zonez')
    sys.exit(1)


if len(sys.argv) == 2:
   if sys.argv[1] == 'get_zonez':
       get_all_zones_list()
   else:
       help()

elif len(sys.argv) == 4:
    mode   = sys.argv[1]
    record = sys.argv[2]
    ipaddr = sys.argv[3]
    zone   = ".".join(record.split(".")[-2:])
    if mode == 'add':
        add(zone,record,ipaddr)   
    else:
        help()

elif len(sys.argv) == 3:
    mode   = sys.argv[1]
    record = sys.argv[2]
    zone   = ".".join(record.split(".")[-2:])
    if mode == 'del':
        delete(record,zone)
    elif mode == 'get_all_a':
        get_a_dns_records(zone)
    else: 
        help()
else:
    help()

