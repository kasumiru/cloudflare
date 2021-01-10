# Cloudflare api DNS control

A short script for control your cloudflare dns records. 
Now support only A dns records.


### Installation

Create link into your path or add script to $PATH.

```
$ ln -s  $(pwd)/cloudflare-python.py /usr/sbin/cf

#Optional for install bash completion:

$ ln -s  $(pwd)/cloudflare_completion.sh /etc/bash_completion.d/cloudflare_completion.sh
$ echo 'source /etc/bash_completion.d/cloudflare_completion.sh' >> ~/.bashrc
```


## Getting Started

copy creds.json.example to creds.json and cnahge it.
```
$ copy creds.json.example creds.json
$ vim creds.json   #(nano creds.json)
```
put your credentials from https://dash.cloudflare.com/profile


### Script usage

You can see help in any place type:
```
$ cf 
```
Get all your zone:
```
$ cf get_zonez
```
Get all A record:
```
$ cf get_all_a yourDomain.com
```
Add A record:
cf add your-subdomain.your-domain.com ip_address
example:
```
$ cf add subdomain.yourDomain.com 8.8.8.8
```
Delete A record:
```
$ cf del subdomain.yourDomain.com
```
