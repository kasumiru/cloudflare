#!/usr/bin/env python3
import sys
import os
import requests
import json

import module_locator
'''for find absolute path dir. see https://coderoad.ru/2632199/Как-получить-путь-к-текущему-исполняемому-файлу-в-Python#2632297
or https://stackoverflow.com/questions/122327/how-do-i-find-the-location-of-my-python-site-packages-directory
'''

fullpath = module_locator.module_path()


headers = {
    'Content-Type': 'application/json'
}

fconfig = fullpath + '/creds.json'

def write_conf(a,b):
    data = {}
    data['X-Auth-Email'] = a
    data['X-Auth-Key']   = b
    print('Writing config: ', data)
    with open(fconfig, 'w') as e:
        json.dump(data, e)

def read_conf():
    try:
        with open(fconfig) as e:
            data = json.load(e)
    except IOError:
        print('''
        Credential file is empty, please paste Your credentials
        and script will generete creds.json autimaticaly,
        or You can manual copy from exampl, see help on github
        ''')
        a = input('Please type "X-Auth-Email" (simple: youremail@gmail.com): ')
        b = input('Please type "X-Auth-Key" (simple: 3210a271xxxxx413d2e8dexxxxxe1ffxxxxca): ')
        try:
            write_conf(a,b)
            sys.exit(0)
        except Exception as e:
            print('variables is lost, try another', e)
            sys.exit(1)

    headers['X-Auth-Email'] = data['X-Auth-Email']
    headers['X-Auth-Key']   = data['X-Auth-Key']


read_conf()



def add(zone,record,ipaddr):
    data = {
        'type':     "A",
        'ttl':      "120",
        'priority': 10,
        'proxied':  False
    }
    data['name']    = record
    data['content'] = ipaddr
    url = 'https://api.cloudflare.com/client/v4/zones/{}/dns_records'.format(str(get_zone_id(zone)))
    r = requests.post(url, headers=headers, json=data)
    try:
        result = r.json()['success']
        if result == True:
            print(f'Success registry {record} with {ipaddr}')
        else:
            print(f'Cloudflare result: {r.json()}')
    except Exception as e:
        print('Exceprion:\n', e)
        print(r.json())


def get_zone_id(zone):
    url = 'https://api.cloudflare.com/client/v4/zones'
    r = requests.get(url, headers=headers,  json='')
    ress = r.json()['result']
    for i in ress:
        if i.get('name') == zone:
            return i.get('id')

def get_a_dns_records(zone):
    url = 'https://api.cloudflare.com/client/v4/zones/{}/dns_records'.format(str(get_zone_id(zone)))
    r = requests.get(url, headers=headers, json='')

    list = []
    for i in r.json().get('result'):
        type = i.get('type')
        if type == 'A':
            list.append(i.get('name'))

    def print_space(n):
        return ' ' * n

    def maxlen(list):
       return max(len(i) for i in list) + 1

    for i in r.json().get('result'):
        name = i.get('name')
        dnstype = i.get('type')
        content = i.get('content')
        if dnstype == 'A':
            num = maxlen(list) - len(name)
            interval = print_space(num)
            print('{0}{1}{2} {3}'.format(name, interval, dnstype, content))
    return r.json()

def get_dns_record_id(zone,record):
    zone_id = str(get_zone_id(zone))
    url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records'
    r = requests.get(url, headers=headers, json='')
    all_records = r.json()
    for i in all_records.get('result'):
        name = i['name']
        id   = i['id']
        if name == record:
            return id

def def_delete(record,zone):
    print(f'now delete {record}:')
    zone_id = str(get_zone_id(zone))
    dns_record_id = get_dns_record_id(zone,record)
    if dns_record_id is not None:
        url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{dns_record_id}'
        r = requests.delete(url, headers=headers, json='')
        print(r.json())

    else:
       print(f'subdomain {record} not exist!')

def get_all_zones_list():
    url = 'https://api.cloudflare.com/client/v4/zones'
    r = requests.get(url, headers=headers, json='')
    result = r.json()['success']
    if result == False:
        print(r.json()['errors'][0]['message'])
        print(r.json().get('errors')[0].get('error_chain'))
        sys.exit(1)
    else:
        domains_list = []
        for i in r.json().get('result'):
            if i is not None:
                domains_list.append(i.get('name'))
        return domains_list



def help():
    print('./cloudflare-python.py add       subdomain.yourDomain.com 8.8.8.8')
    print('./cloudflare-python.py del       subdomain.yourDomain.com ')
    print('./cloudflare-python.py get_all_a yourDomain.com ')
    print('./cloudflare-python.py get_zones')
    sys.exit(1)

if len(sys.argv) == 2:
   if sys.argv[1] == 'get_zones':
       for i in get_all_zones_list():
           print(f'{i}')
   else:
       help()

elif len(sys.argv) == 4:
    mode   = sys.argv[1]
    record = sys.argv[2]
    ipaddr = sys.argv[3]
    zone   = '.'.join(record.split('.')[-2:])
    if mode == 'add':
        add(zone,record,ipaddr)
    else:
        help()

elif len(sys.argv) == 3:
    mode   = sys.argv[1]
    record = sys.argv[2]
    zone   = '.'.join(record.split('.')[-2:])
    if mode == 'del':
        if zone in get_all_zones_list():
            def_delete(record,zone)
        else:
            print(f'Erro: zone "{zone}" does not exist in Your zones!')
            sys.exit(1)
    elif mode == 'get_all_a':
        #get_a_dns_records(zone)
        if zone in get_all_zones_list():
            get_a_dns_records(zone)
        else:
            print(f'Erro: zone "{zone}" does not exist in Your zones!')
            sys.exit(1)
    else:
        help()
else:
    help()

