# Cloudflare api DNS control

UPD 2022.02.15: added control TXT records ::so-happy::                                                                                                        
A short script for control your cloudflare dns records. 
Now support A, TXT dns records.


### Installation

Create link into your path or add script to $PATH.

```
$ ln -s  $(pwd)/cloudflare-python.py /usr/sbin/dns

#Optional for install bash completion:

$ ln -s  $(pwd)/cloudflare_completion.sh /etc/bash_completion.d/cloudflare_completion.sh
$ echo 'source /etc/bash_completion.d/cloudflare_completion.sh' >> ~/.bashrc
```


## Getting Started

You can just start:
```
$ dns
``` 
and script asked login and password creds for cloudflare,
or manual copy creds.json.example to creds.json and cnahge it:
```
$ copy creds.json.example creds.json
$ vim creds.json   #(nano creds.json)
```
take your credentials from https://dash.cloudflare.com/profile


### Script usage

You can see help in any place type:
```
$ dns 
```
shown help:
```
set/del TXT record:
dns set TXT subdomain.yourDomain.com "some txt text"
dns del TXT subdomain.yourDomain.com
set/del A record:
dns set A   subdomain.yourDomain.com 8.8.8.8
dns del A   subdomain.yourDomain.com
view all A records in by domain:
dns get_all_a yourDomain.com
view all zones (your root domains)
dns get_zones
```


Get all your zone:
```
$ dns get_zonez
```
Get all A record:
```
$ dns get_all_a yourDomain.com
```
Add A record:
dns set your-subdomain.your-domain.com ip_address
example:
```
$ dns set subdomain.yourDomain.com 8.8.8.8
```
Delete A record:
```
$ dns del subdomain.yourDomain.com
```

