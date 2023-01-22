# -*- coding: utf-8 -*-
import glob
import signal
import threading
import multiprocessing
import ipaddress
import time
import os
import sys
import socket
import warnings
from datetime import datetime
import runner.navigator as navigator
from utils import colors
from cli import cli
from crawlers import links
warnings.filterwarnings("ignore")

domainList = []
scopeList = []

color = colors.Colors()
animation = color.animation
reset = color.reset
yellow = color.yellow
white = color.white
red = color.red
dark_grey = color.dark_grey
light_grey = color.light_grey
blue = color.blue
bold = color.bold
green = color.green
magenta = color.magenta
purple = color.purple
pink = color.pink
purple3 = color.purple_3


def banner():
    logo = ''' 
\t
\t 
\t                  
\t░██████╗██╗░█████╗░░█████╗░██████╗░██╗██╗░░░██╗░██████╗
\t██╔════╝██║██╔══██╗██╔══██╗██╔══██╗██║██║░░░██║██╔════╝
\t╚█████╗░██║██║░░╚═╝███████║██████╔╝██║██║░░░██║╚█████╗░
\t░╚═══██╗██║██║░░██╗██╔══██║██╔══██╗██║██║░░░██║░╚═══██╗
\t██████╔╝██║╚█████╔╝██║░░██║██║░░██║██║╚██████╔╝██████╔╝
\t╚═════╝░╚═╝░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░╚═════╝░╚═════╝░   
\t       
\t    -= ⚡️ Fast subdomain enumeration tool ⚡️ =-
\t                    
\t  
\t {2}[{4}{5}Version: 1.0.1{4} {3}Codename: darky {4}{0}[author: unp4ck]{4}{1}[tw: @unp4ck]{4}{2}] 
'''
    logo = logo.format(light_grey, dark_grey, red, white, color.reset, magenta)
    os.system('cls' if os.name == 'nt' else 'clear')
    print(bold + logo + reset)


class Sicarius:
    def __init__(self, domain, output, threads=50, scope=False, debug=False, statusCode=False, title=False, ip=False,
                 silent=False, extract=False):
        self.domain = domain
        self.threads = threads
        self.scope = scope
        self.debug = debug
        self.silent = silent
        self.statusCode = statusCode
        self.title = title
        self.ip = ip
        self.output = output
        self.extract = extract
        self.scopeList = []
        
        
        if self.scope:
            self._log('Loading scope list')
            with open(self.scope) as f:
                lines = f.readlines()
            self._log('Resolving scope list to IPV4')
            for line in lines:
                for ip in ipaddress.IPv4Network(line.strip()):
                    self.scopeList.append(str(ip))

    def fetchWorker(self, q):
        domainAndIp = q
        domainReturn = domainAndIp
        if self.statusCode:
            try:
                statusCode = navigator.Navigator().downloadResponse('http://{}'.format(domainAndIp), 'STATUS', 'HEAD').status_code
            except:
                statusCode = 'TIMEOUT'

            if statusCode is not None:
                if statusCode == 200:
                    if self.extract and self.output:
                        urls = {}
                        urls["http"] = "http://{0}".format(domainAndIp)
                        urls["https"] = "https://{0}".format(domainAndIp)
                        for url in urls.values():
                            links.Crawler(url)

                    domainReturn += ' [{0}{1}{2}]'.format(green, statusCode, reset)
                    if self.title:
                        title = navigator.Navigator().downloadResponse('http://{}'.format(domainAndIp), 'TITLE',
                                                                       'GET')
                        domainReturn += ' [{0}{1}{2}]'.format(dark_grey, title, reset)
                elif statusCode == 'TIMEOUT':
                    domainReturn += ' [{0}{1}{2}]'.format(red, statusCode, reset)
                else:
                    domainReturn += ' [{0}{1}{2}]'.format(dark_grey, statusCode, reset)

            if self.title and statusCode != 'TIMEOUT':
                title = navigator.Navigator().downloadResponse('http://{}'.format(domainAndIp), 'TITLE',
                                                               'GET')
                domainReturn += ' [{0}{1}{2}]'.format(dark_grey, title, reset)

        if self.ip:
            ipDomain = self.getIP(domainAndIp)
            if self.scope:
                if ipDomain in self.scopeList:
                    domainReturn += ' {}'.format(ipDomain)
                    sys.stdout.write(domainReturn + '\n')
                self.log(domainReturn)
            else:
                domainReturn += ' {}'.format(ipDomain)
                sys.stdout.write(domainReturn + '\n')
                self.log(domainReturn)
        elif self.scope:
            ipDomain = self.getIP(domainAndIp)
            if ipDomain in self.scopeList:
                sys.stdout.write(domainReturn + '\n')
                self.log(domainReturn)
        else:
            domainReturn += ''
            sys.stdout.write(domainReturn + '\n')
            self.log(domainReturn)

    def ModulesWorker(self, q):
        module = q
        mod = __import__('modules.{0}'.format(module))
        rr = getattr(mod, module).returnDomains(self.domain, self.silent)
        return rr


    def init_worker(self):
        signal.signal(signal.SIGINT, signal.SIG_IGN)

    def fetchDomains(self, sublist):
        try:
            pool = multiprocessing.Pool(self.threads, initializer=self.init_worker)
            pool.map(self.fetchWorker, sublist)
            pool.close()
            pool.join()
        except KeyboardInterrupt:
            self._warn('Shutting down...')
            pool.terminate()

    def fetch(self):
        self._log('loading Modules')
        dir_path =  os.path.dirname(os.path.realpath(__file__)) + '/modules/*.py'
        modules = []
        for path in glob.glob(dir_path):
            if os.path.isfile(os.path.join(dir_path, path)):
                if '__init__.py' not in path:
                    modules.append(os.path.basename(path).replace('.py',''))

        try:
            pool = multiprocessing.Pool(self.threads)
            result = pool.map_async(self.ModulesWorker, modules)
            pool.close()
            load = 1
            while result._number_left > 1:
                if not self.silent:
                    self._info('{0} Enumerating subdomains for {4}{2}{5}{5}'.format(animation[
                                                                                        load % len(animation)], 0,
                                                                                    self.domain, purple, red, reset),
                               r=True)
                    sys.stdout.flush()
                    load += 1
                    time.sleep(0.09)
                    sys.stdout.flush()
            pool.join()
            domainList = []
            for __ in result.get():
                for _ in __:
                    domainList.append(_.lower())
                domainList = list(dict.fromkeys(domainList))
            sys.stdout.write('\x1b[2K\n')
            self._info('Found {2}{0}{4} for {3}{1}{4}\n\n'.format(len(domainList), self.domain, purple, purple3, reset), r=True)
            self.fetchDomains(domainList)

        except KeyboardInterrupt:
            self._warn('Shutting down...')
            pool.terminate()

    def getDomains(self):
        th = threading.Thread(target=self.fetch)
        th.daemon = True
        th.start()
        th.join()
        print()

    def getIP(self, subdomain):
        try:
            return socket.gethostbyname(subdomain)
        except:
            return '0.0.0.0'

    """
    
    Only loggers :)
    
    """
    ## save output
    def log(self, line):
        if self.output and not self.silent:
            with open(self.output, 'a') as output_file:
                output_file.write("%s\n" % line)

    # save crawler output
    def log_crawler(self, line):
        if self.extract and self.output:
            crawler_outname = self.output + "_data_crawler.txt"
            with open(crawler_outname, 'a') as output_crawler:
                output_crawler.write("{0}\n".format(line))
        
    def _log(self, *args):
        if self.debug and not self.silent:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print(
                '[' + magenta + current_time + reset + '] [' + pink + 'DEBUG' + reset + ']:' + reset + ' {0}'.format(
                    *args))

    def _info(self, *args, r=False):
        if not self.silent:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            if r:
                sys.stdout.write('\r'
                                 '[' + magenta + current_time + reset + '] [' + magenta + 'INF' + reset + ']:' + reset + ' {0}'.format(
                    *args))
            else:
                print(
                    '[' + magenta + current_time + reset + '] [' + magenta + 'INF' + reset + ']:' + reset + ' {0}'.format(
                        *args))

    def _warn(self, *args):
        if not self.silent:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print(
                '\n' + reset + '[' + magenta + current_time + reset + '] [' + red + 'WRN' + reset + ']:' + reset + ' {0}'.format(
                    *args))


if __name__ == "__main__":
    args = cli.Cli.argParserCommands().parse_args()
    if not args.silent:
        banner()

    if args.domainList and args.domain is None:
        dlist = args.domainList.read()
        for d in dlist.split('\n'):
            sicarius = Sicarius(d.strip(), args.output, args.threads, args.scope, args.verbose, args.statusCode, args.title,
                            args.ip, args.silent)
            sicarius.getDomains()
    elif args.domain and args.domainList is None:
        sicarius = Sicarius(args.domain, args.output, args.threads, args.scope, args.verbose, args.statusCode, args.title,
                        args.ip, args.silent)
        sicarius.getDomains()
    elif args.domain and args.domainList:
        dlist = args.domainList.read()
        for d in dlist.split('\n'):
            sicarius = Sicarius(d.strip(), args.output, args.threads, args.scope, args.verbose, args.statusCode, args.title,
                            args.ip, args.silent)
            sicarius.getDomains()
    else:
        cli.Cli.argParserCommands().print_help()
