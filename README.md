# Cloudflare api DNS control

A short script for control your cloudflare dns records. 
Now support only A dns records.


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
