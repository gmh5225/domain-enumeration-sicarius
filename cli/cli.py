import argparse
import sys

class Cli:
    def __init__(self) -> None:
        pass

    def argParserCommands():
        parser = argparse.ArgumentParser()
        parser.add_argument('-d', '--domain', dest="domain", help='domains to find subdomains for',
                            required=False)
        parser.add_argument('-e', '--extract', help="Extract: links ( inside JS to ), headers, useful for new domains and second order subdomain takeover", action='store_true' ,default=False)
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
        parser.add_argument('-t', '--threads', type=int, dest="threads", default=40,
                            help="number of concurrent threads for resolving (default 40)")
        parser.add_argument('-ip', '--ip', dest="ip", help='Resolve IP address', default=False,
                            action="store_true")
        parser.add_argument('-v', dest="verbose", help='show verbose output', default=False,
                            action="store_true")
        parser.add_argument('-silent', '--silent', dest="silent", help='show only subdomains in output', default=False,
                            action="store_true")
        parser.add_argument("-o", "--output", help="file to write output to")

        return parser