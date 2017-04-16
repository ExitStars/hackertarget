from argparse import ArgumentParser
from socket import gethostbyname
from os import getcwd
from requests import get
from json import dumps

__description__ = 'Poor CLI for hackertarget.com'

URLs = {
    'needsDomain': [
        'http://api.hackertarget.com/dnslookup/?q={}',
        'http://api.hackertarget.com/hostsearch/?q={}',
        'http://api.hackertarget.com/zonetransfer/?q={}',
        'http://api.hackertarget.com/whois/?q={}',
        'http://api.hackertarget.com/httpheaders/?q=http://www.{}'
    ],
    'needsIP': [
        'https://api.hackertarget.com/reversedns/?q={}'
    ]
}


def createReport(data):
    ' Prints out final report '

    print('DNS LOOKUP\n==========\n{0}\n\n\
REVERSE DNS LOOKUP\n==================\n{1}\n\n\
DNS HOST RECORDS\n================\n{2}\n\n\
ZONE TRANSFER\n=============\n{3}\n\n\
HTTP HEADERS\n============\n{4}\n\n\
WHOIS LOOKUP\n============\n{5}\n\n'.format(data['dnslookup'], data['reversedns'], data['hostsearch'],
                                            data['zonetransfer'], data['httpheaders'], data['whois']))

    with open('report.json', 'w') as report: report.write(dumps(data, indent=4))


def scan(targetDomain=None, targetIP=None):
    ' Runs some scan APIs on given arguments. '

    data = []

    try:
        [data.append(get(URL.format(targetDomain)).text) for URL in URLs['needsDomain']]
        [data.append(get(URL.format(targetIP)).text) for URL in URLs['needsIP']]
    except ConnectionError: print('[!] CONNECTION ERROR!'); quit()

    data = dict(zip(['dnslookup', 'hostsearch',
                     'zonetransfer', 'whois',
                     'httpheaders', 'reversedns'], data))

    createReport(data)


def main():
    ' Parses arguments and sends them to scan function. '

    parser = ArgumentParser(usage='[?] USAGE:\n\t$ python cliHT.py -d <domain>')
    parser.add_argument('-d', '--domain',
                        type=str, help='Domain name (w/o www. and /)')
    flags = parser.parse_args()

    if flags.domain != None:
        targetDomain = flags.domain
        for prefix in ['http://', 'https://']: a = targetDomain.replace(prefix, '') if prefix in targetDomain else None

        try: targetIP = gethostbyname(targetDomain)
        except Exception as e: print("[!] ERROR AT GETTING IP ADDRESS USING DOMAIN NAME!"); quit()

        scan(targetDomain, targetIP)
    else: print(parser.usage); quit()


if __name__ == '__main__': main()
else: print('YOU CANNOT USE THIS SCRIPT WITH YOURS, BELIEVE ME.')
