
# Sicarius

![alt text](https://img.shields.io/github/stars/unp4ck/Sicarius "")
![alt text](https://img.shields.io/github/languages/top/unp4ck/Sicarius "")
![alt text](https://img.shields.io/github/license/unp4ck/Sicarius "")
<a href="https://twitter.com/unp4ck"><img src="https://img.shields.io/twitter/follow/unp4ck.svg?logo=twitter"></a>


![/static/banner.png](/static/banner.png)


<h4 align="center">Fast subdomain enumeration tool.</h4>

### Install
```bash

git clone github.com/unp4ck/sicarius.git

cd sicarius

touch config/config.yaml

# add your apis keys here!

pip3 install -r requirements.txt --user
```



### Post Installation

API Key is needed before querying on third-party sites 
* ```Shodan``` 
* ```SecurityTrails```
* ```Virustotal``` 
* ```BinaryEdge```
* Etc..

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

 

	 version/codename: darky 👹 {1.0.0#dev}@unp4ck

	░██████╗██╗░█████╗░░█████╗░██████╗░██╗██╗░░░██╗░██████╗
	██╔════╝██║██╔══██╗██╔══██╗██╔══██╗██║██║░░░██║██╔════╝
	╚█████╗░██║██║░░╚═╝███████║██████╔╝██║██║░░░██║╚█████╗░
	░╚═══██╗██║██║░░██╗██╔══██║██╔══██╗██║██║░░░██║░╚═══██╗
	██████╔╝██║╚█████╔╝██║░░██║██║░░██║██║╚██████╔╝██████╔╝
	╚═════╝░╚═╝░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░╚═════╝░╚═════╝░

	    =- Fast subdomain enumeration tool =-




[22:19:49] [ INFO]: alienvault.com 136 domains founded!✅
[22:19:50] [ INFO]: certspotter.com 5 domains founded!✅
[22:19:50] [ INFO]: urlscan.io 53 domains founded!✅
[22:19:50] [ INFO]: hackertarget.com 10 domains founded!✅
[22:19:50] [ INFO]: binaryedge.io 8 domains founded!✅
[22:19:51] [ INFO]: virustotal 46 domains founded!✅
[22:19:51] [ INFO]: crt.sh 250 domains founded!✅
[22:19:51] [ INFO]: wayback 8685 domains founded!✅
[22:19:56] [ INFO]: securitytrails.com 54 domains founded!✅

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

### Features

![/static/sc.gif](/static/sc.gif)

- Modular,fast,lightweigth;
- Wildcard elimination module;
- Scope limitation based on given IP ranges list;

