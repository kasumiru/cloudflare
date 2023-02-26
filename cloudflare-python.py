#!/usr/bin/env python3
import sys
import os
import requests
import json
import re


# feature release. =/
dns_provider = 'cloudflare' # 'cloudflare' or 'amazon' 


# colors 
class clr:
    green     = '\033[92m'
    yellow    = '\033[93m'
    red       = '\033[91m'
    blue      = '\033[94m'
    cyan      = '\033[96m'
    magenta   = '\033[95m'
    grey      = '\033[90m'
    rest      = '\033[0m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'
#print(f"{clr.green} Hellllloooow  {clr.rest}")
#print(clr.red + "Hellloowwww" + clr.rest)


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

def set_ipaddr(zone,record,ipaddr):
    ip_check = re.findall("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$", ipaddr)
    if not ip_check:
        print(f'Ip address {ipaddr} not valid, exit now!')
        exit(1)
    if not zone:
        print('Cant recognize zone: {zone}, exit 1')
        exit(1)
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

def set_txt_record(zone,record,record_txt):
    data = {
        'type':     "TXT",
        'ttl':      "60", # set default to 120
        'priority': 10,
        'proxied':  False
    }
    data['name']    = record
    data['content'] = record_txt
    zone_id = str(get_zone_id(zone))
    url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records'
    r = requests.post(url, headers=headers, json=data)
    try:
        result = r.json()['success']
        if result == True:
            print(f'Success registry {record} with {record_txt}')
        else:
            print(f'Cloudflare result: {r.json()}')
    except Exception as e:
        print('Exceprion:\n', e)
        print(r.json())

def get_a_dns_records(zone):
    zone_id = get_zone_id(zone)
    url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records'
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

def get_dns_record_id(zone,record,record_type):
    zone_id = str(get_zone_id(zone))
    url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records'
    r = requests.get(url, headers=headers, json='')
    all_records = r.json()

    for i in all_records.get('result'):
        name = i['name']
        id   = i['id']
        type = i['type']
        if name == record and type == record_type:
            return id

def del_txt_record(zone,dns_name):
    print(f'now delete txt record from dns name: {dns_name}:')
    zone_id = str(get_zone_id(zone))
    record_type = 'TXT'
    dns_record_id = get_dns_record_id(zone,dns_name,record_type)
    if dns_record_id is not None:
        url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{dns_record_id}'
        r = requests.delete(url, headers=headers, json='')
        print(r.json())
    else:
        print(f'TXT dns record "{dns_name}" not exist!')

def def_delete(record,zone):
    print(f'now delete A {record}:')
    zone_id = str(get_zone_id(zone))
    record_type = 'A'
    dns_record_id = get_dns_record_id(zone,record,record_type)
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
    print(f'{clr.yellow}add/del TXT record{clr.rest}:')
    print('dns set TXT subdomain.yourDomain.com "some txt text"')
    print('dns del TXT subdomain.yourDomain.com')
    print(f'{clr.yellow}add/del A record{clr.rest}:')
    print('dns set A   subdomain.yourDomain.com 8.8.8.8')
    print('dns del A   subdomain.yourDomain.com ')
    print(f'{clr.yellow}view all A records in by domain{clr.rest}:')
    print('dns get_all_a yourDomain.com ')
    print(f'{clr.yellow}view all zones (your root domains){clr.rest}:')
    print('dns get_zones')
    sys.exit(1)


def var_exist(var):
     var_exists = var in locals() or var in globals()
     return var_exists

def main():

    lambd_lower = lambda a: a.lower()

    #'''Get all zones'''
    if len(sys.argv) == 2:
       if sys.argv[1] == 'get_zones':
           for i in get_all_zones_list():
               print(f'{i}')
       else:
           help()

    #'''get_a_dns_records(zone)'''
    elif len(sys.argv) == 3:
        mode   = sys.argv[1]
        record = sys.argv[2]
        zone   = '.'.join(record.split('.')[-2:])

        if zone in get_all_zones_list():
            get_a_dns_records(zone)
        else:
            print(f'Erro: zone "{zone}" does not exist in Your zones!')
            sys.exit(1)

    #''' set TXT or A record'''
    elif len(sys.argv) == 5:
        set_mode_list = ['set', 'add']

        if sys.argv[1].lower() in map(lambd_lower, set_mode_list):
            print(f'now adding block')
            txt_mode_list = ['txt', 'text']
            a_mode_list   = ['a']
            if   sys.argv[2].lower() in map(lambd_lower, txt_mode_list):
                dns_name   = sys.argv[3]
                zone   = '.'.join(dns_name.split('.')[-2:])
                record = sys.argv[4]
                print(f'adding TXT dns_name = {dns_name}, record = {record}')
                set_txt_record(zone,dns_name,record)

            elif sys.argv[2].lower() in map(lambd_lower, a_mode_list):
                dns_name = sys.argv[3]
                zone   = '.'.join(dns_name.split('.')[-2:])
                ipaddr = sys.argv[4]
                print(f'adding A dns_name = {dns_name}, ipaddr = {ipaddr}')
                set_ipaddr(zone,dns_name,ipaddr)
            else:
                print(f'deb 01.')
                help()
        else:
            print('deb 02.')
            help()

    #''' del TXT or A record'''
    elif len(sys.argv) == 4:
        del_mode_list = ['del', 'delete']
        if sys.argv[1].lower() in map(lambd_lower, del_mode_list):
            print('now deleting block')
            txt_mode_list = ['txt', 'text']
            a_mode_list   = ['a']
            if   sys.argv[2].lower() in map(lambd_lower, txt_mode_list):
                dns_name   = sys.argv[3]
                zone   = '.'.join(dns_name.split('.')[-2:])
                print(f'deleting TXT dns_name = {dns_name}')
                del_txt_record(zone,dns_name)

            elif sys.argv[2].lower() in map(lambd_lower, a_mode_list):
                dns_name = sys.argv[3]
                zone   = '.'.join(dns_name.split('.')[-2:])
                print(f'deleting A dns_name = {dns_name}')
                def_delete(dns_name,zone)
            else:
                print(f'deb 03.')
                help()
            
        else:
            print('deb 04.')
            help()
    else:
        help()

if __name__ == "__main__":
    main()
