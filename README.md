
# Sicarius


![alt text](https://img.shields.io/github/stars/unp4ck/Sicarius)
![alt text](https://img.shields.io/github/languages/top/unp4ck/Sicarius)
![alt text](https://img.shields.io/github/license/unp4ck/Sicarius)
<a href="https://twitter.com/unp4ck"><img src="https://img.shields.io/twitter/follow/unp4ck.svg?logo=twitter"></a>


![/static/banner.png](/static/woa.png)

<h4 align="center">  🐴 ⚡️ Fast subdomain enumeration tool 🐴 ⚡️</h4>

### Install
```bash

git clone github.com/unp4ck/sicarius.git

cd sicarius

touch config/config.yaml

# add your apis keys here!

pip3 install -r requirements.txt --user
```

### Post Installation

API Key is needed before querying on third-party sites;

##### Sicarius have 12 Sources to grab subdomains.

* ```Shodan``` 
* ```SecurityTrails```
* ```Virustotal``` 
* ```BinaryEdge```
* ```chaos``` - [https://chaos.projectdiscovery.io/#/docs](https://chaos.projectdiscovery.io/#/docs)
* ```ctrsh```
* ```wayback```
* ```threatcrowd```
* ```certspooter```
* ```hackertarget```
* ```urlscan```
* ```alienvault```

- **The API key setting can be done via `config.yaml`**

An example provider config file 

```yaml
virustotal:
  - XXXXXXXXXXXXXXX
securitytrails: []
shodan:
  - XXXXXXXXXXXXXXXXXXX
```

### Usage



```yaml

INPUT:
   -d --domain string    domains to find subdomains for
   -l DOMAINLIST         file containing list of domains for subdomain discovery
   --scope SCOPE         show only subdomains in scope

OUTPUT:
   -sc, --status-code    show response status code
   -ip, --ip             resolve IP address
   -title, --title       show page title
   -silent, --silent     show only subdomains in output
   -o OUTPUT, --output OUTPUT
                        file to write output to
   
CONFIG:
   -t THREADS, --threads THREADS
                        number of concurrent threads for resolving (default 50)

DEBUG:
   -v                    show verbose output
   -h, --help            show this help message and exit
```

### Running Sicarius
```console
cat domains | python3 Sicarius.py
```


### You can pipe with other tools like nuclei, httpx etc..

```bash
# httpx to probe
echo intigriti.com | python3 Sicarius.py -silent | httpx -silent 
# pipe to nuclei
echo intigriti.com | python3 Sicarius.py -silent | httpx -silent | nuclei -t <path_to_nuclei_templates>

```

```console
python3 Sicarius.py -d intigriti.com

	░██████╗██╗░█████╗░░█████╗░██████╗░██╗██╗░░░██╗░██████╗
	██╔════╝██║██╔══██╗██╔══██╗██╔══██╗██║██║░░░██║██╔════╝
	╚█████╗░██║██║░░╚═╝███████║██████╔╝██║██║░░░██║╚█████╗░
	░╚═══██╗██║██║░░██╗██╔══██║██╔══██╗██║██║░░░██║░╚═══██╗
	██████╔╝██║╚█████╔╝██║░░██║██║░░██║██║╚██████╔╝██████╔╝
	╚═════╝░╚═╝░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░╚═════╝░╚═════╝░

	    -= ⚡️ Fast subdomain enumeration tool ⚡️ =-


	 [Version: 1.0.1 Codename: darky [author: unp4ck][tw: @unp4ck]]

[10:20:48] [ INFO]: urlscan.io 18 domains founded! ✅
[10:20:48] [ INFO]: certspotter.com 6 domains founded! ✅
[10:20:48] [ INFO]: virustotal 76 domains founded! ✅
[10:20:49] [ INFO]: binaryedge.io 61 domains founded! ✅
[10:20:49] [ INFO]: hackertarget.com 37 domains founded! ✅
[10:20:49] [ INFO]: alienvault.com 127 domains founded! ✅
[10:20:50] [ INFO]: securitytrails.com 116 domains founded! ✅
[10:20:50] [ INFO]: wayback 24375 assets founded! ✅
[10:20:50] [ INFO]: crt.sh 179 domains founded! ✅

[22:19:57] [INF]: Found 58 for intigriti.com

www.intigriti.com
mail.intigriti.com
login.intigriti.com
app.intigriti.com
newsletter.intigriti.com
api.intigriti.com
blog.intigriti.com
kb.intigriti.com
communication.intigriti.com
go.intigriti.com
hello.intigriti.com
careers.intigriti.com
swag.intigriti.com
click-uat.intigriti.com
t.intigriti.com
trust.intigriti.com


```

### Congrats
   - Thanks [duty1g](https://github.com/duty1g) ~ [subcat](https://github.com/duty1g/subcat) 🖤


### Features

![/static/sc.gif](/static/sc.gif)

- Modular,fast,lightweigth 🍦 
- Wildcard elimination module 🙅🏽‍♂️ 
- Scope limitation based on given IP ranges list 📸 
- Extracts links and headers, for second order subdomain takeveover or new subs ✨ 🥷 ✨  -> | **Warning: the first time you run this method, it will download Chromium into your home directory (~/.pyppeteer)** ( render Javascript ;) ) ( WORKING PROGRESS !!)

#### Meaning of sicarius

```
Sicarius is a genus of recluse spiders that is potentially medically significant to humans. It is one of three genera in its family, all venomous spiders known for a bite that can induce loxoscelism. They live in deserts and arid regions of the Neotropics, and females use a mixture of sand and silk when producing egg sacs. The name is Latin for assassin.
```