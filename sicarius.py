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
import argparse
import warnings
from datetime import datetime
import runner.navigator as navigator
from colored import fore, back, style, fg, bg, attr, stylize


warnings.filterwarnings("ignore")

domainList = []
scopeList = []

class Colors:
    def __init__(self) -> None:
        self.animation = "🕸🕷"
        self.reset = attr('reset')
        self.light_grey = fg('light_gray')
        self.dark_grey = fg('dark_gray')
        self.red = fg('red')
        self.green = fg('green')
        self.bold = attr('bold')
        self.white = fg('white')
        self.magenta = fg('magenta')
        self.yellow = fg('yellow')
        self.blue = fg('blue')
        self.purple = fg('purple_4a')
        self.pink = fg('pink_3')
        self.cyan = fg('cyan')
        self.purple_3 = fg('purple_3')


color = Colors()
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
\t {5}version/codename: darky 👹 {0}{{{2}1.0.0{5}#dev}}{0}@{3}unp4ck{1}
\t {4}                 
\t░██████╗██╗░█████╗░░█████╗░██████╗░██╗██╗░░░██╗░██████╗
\t██╔════╝██║██╔══██╗██╔══██╗██╔══██╗██║██║░░░██║██╔════╝
\t╚█████╗░██║██║░░╚═╝███████║██████╔╝██║██║░░░██║╚█████╗░
\t░╚═══██╗██║██║░░██╗██╔══██║██╔══██╗██║██║░░░██║░╚═══██╗
\t██████╔╝██║╚█████╔╝██║░░██║██║░░██║██║╚██████╔╝██████╔╝
\t╚═════╝░╚═╝░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░╚═════╝░╚═════╝░   
\t       
\t    =- Fast subdomain enumeration tool =-
\t                    
\t  
\t  
'''
    logo = logo.format(light_grey, dark_grey, red, white, color.reset, magenta)
    os.system('cls' if os.name == 'nt' else 'clear')
    print(bold + logo + reset)


class Sicarius:
    def __init__(self, domain, output, threads=50, scope=False, debug=False, statusCode=False, title=False, ip=False,
                 silent=False):
        self.domain = domain
        self.threads = threads
        self.scope = scope
        self.debug = debug
        self.silent = silent
        self.statusCode = statusCode
        self.title = title
        self.ip = ip
        self.output = output
        self.scopeList = []
        if self.scope:
            self._log('Loading scope list')
            with open(self.scope) as f:
                lines = f.readlines()
            self._log('Resolving scope list to IPV4')
            for line in lines:
                for ip in ipaddress.IPv4Network(line.strip()):
                    self.scopeList.append(str(ip))

    def log(self, line):
        if self.output and not self.silent:
            with open(self.output, 'a') as output_file:
                output_file.write("%s\n" % line)

    def fetchWorker(self, q):
        domainAndIp = q
        domainReturn = domainAndIp
        if self.statusCode:
            try:
                statusCode = navigator.Navigator().downloadResponse('http://{}'.format(domainAndIp), 'STATUS',
                                                                    'HEAD').status_code
            except:
                statusCode = 'TIMEOUT'

            if statusCode is not None:
                if statusCode == 200:
                    domainReturn += ' [{0}{1}{2}]'.format(green, statusCode, reset)
                    if self.title:
                        title = navigator.Navigator().downloadResponse('http://{}'.format(domainAndIp), 'TITLE',
                                                                       'GET')
                        domainReturn += ' [{0}{1}{2}]'.format(dark_grey, title, reset)
                elif statusCode == 'TIMEOUT':
                    domainReturn += ' [{0}{1}{2}]'.format(red, statusCode, reset)
                else:
                    domainReturn += ' [{0}{1}{2}]'.format(dark_grey, statusCode, reset)

            # if self.title and statusCode != 'TIMEOUT':
            #     title = navigator.Navigator().downloadResponse('http://{}'.format(domainAndIp), 'TITLE',
            #                                                    'GET')
            #     domainReturn += ' [{0}{1}{2}]'.format(dark_grey, title, reset)

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

    def getIP(self, subdomain):
        try:
            return socket.gethostbyname(subdomain)
        except:
            return '0.0.0.0'


def argParserCommands():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--domain', dest="domain", help='domains to find subdomains for',
                        required=False)
    parser.add_argument('-l', default=(None if sys.stdin.isatty() else sys.stdin), type=argparse.FileType('r'),
                        dest="domainList", help='file containing list of domains for subdomain discovery',
                        required=False)
    parser.add_argument('-sc', '--status-code', dest="statusCode",
                        help='show response status code', default=False,
                        action="store_true")
    parser.add_argument('-title', '--title', dest="title",
                        help='show page title', default=False,
                        action="store_true")
    parser.add_argument('--scope', dest="scope",
                        help='show only subdomains in scope', default=False)
    parser.add_argument('-t', '--threads', type=int, dest="threads", default=50,
                        help="number of concurrent threads for resolving (default 40)")
    parser.add_argument('-ip', '--ip', dest="ip", help='Resolve IP address', default=False,
                        action="store_true")
    parser.add_argument('-v', dest="verbose", help='show verbose output', default=False,
                        action="store_true")
    parser.add_argument('-silent', '--silent', dest="silent", help='show only subdomains in output', default=False,
                        action="store_true")
    parser.add_argument("-o", "--output", help="file to write output to")

    return parser


if __name__ == "__main__":
    args = argParserCommands().parse_args()
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
        argParserCommands().print_help()
