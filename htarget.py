#-*-coding:utf-8-*-
from argparse import ArgumentParser
from socket import gethostbyname
from os import name, system, getcwd
from requests import get


if name == "posix":
    bold, underline, endcolor = "\033[1m", "\033[4m", "\033[0m"
    green, blue, yellow, red = "\033[92m", "\033[94m", "\033[93m", "\033[91m"
    clear = "clear"
else:
    bold, underline, endcolor = "", "", ""
    green, blue, yellow, red = "", "", "", ""
    clear = "cls"

def logo():
    system(clear)
    print "--==["+bold+blue+"nickname"+endcolor+"] [ ExitStars"
    print "--==["+bold+yellow+"MyGitHub"+endcolor+"] [ http://github.com/ExitStars"
    print "--==["+bold+green+"software"+endcolor+"] [ Hacker Target / Information Gathering Tool"
    print "-"*60

def scan(targetDomain, targetIP):
    def dnsLookupScan():
        address = "http://api.hackertarget.com/dnslookup/?q={}".format(targetDomain)
        payload = get(address).text
        return payload

    def dnsReverseLookupScan():
        address = "https://api.hackertarget.com/reversedns/?q={}".format(targetIP)
        payload = get(address).text
        return payload

    def hostSearchScan():
        address = "http://api.hackertarget.com/hostsearch/?q={}".format(targetDomain)
        payload = get(address).text
        return payload

    def zoneTransferScan():
        address = "http://api.hackertarget.com/zonetransfer/?q={}".format(targetDomain)
        payload = get(address).text
        return payload

    def whoisScan():
        address = "http://api.hackertarget.com/whois/?q={}".format(targetDomain)
        payload = get(address).text
        return payload

    def httpHeadersScan():
        address = "http://api.hackertarget.com/httpheaders/?q=http://www.{}".format(targetDomain)
        payload = get(address).text
        return payload

    print bold+yellow+"<< DNS Lookup >>".center(60)+endcolor
    print dnsLookupScan()

    print bold+yellow+"<< Reverse DNS Lookup >>".center(60)+endcolor
    print dnsReverseLookupScan()

    print bold+yellow+"<< Find DNS Host Records >>".center(60)+endcolor
    print hostSearchScan()

    print bold+yellow+"<< Zone Transfer >>".center(60)+endcolor
    print zoneTransferScan()

    print bold+yellow+"<< HTTP Headers >>".center(60)+endcolor
    print httpHeadersScan()

    print bold+yellow+"<< Whois Lookup >>".center(60)+endcolor
    try:
        text = open(targetDomain+".txt", "w")
        text.write(whoisScan())
        text.close()
        print bold+yellow+"Saved to Directory: "+endcolor+getcwd()+"/"+targetDomain+".text"
    except Exception as e:
        print bold+red+"Error:\n\t"+endcolor, e

def main():
    logo()
    parser = ArgumentParser(usage = bold+yellow+"Usage:\n\t"+green+"es@coderlab "+blue+"~ $"+endcolor+" python htarget.py -d <example.com>")
    parser.add_argument("-d", type=str, help="Target Domain Adress")
    options = parser.parse_args()

    if options.d == None:
        print parser.usage
        quit()
    else:
        targetDomain = options.d
        targetDomain = targetDomain.replace("http://", "")
        targetDomain = targetDomain.replace("https://", "")
        targetDomain = targetDomain.replace("www.", "")
        targetDomain = targetDomain.replace("/", "")

        try:
            targetIP = gethostbyname(targetDomain)
        except Exception as e:
            print bold+red+"Error:\n\t"+endcolor, e
            quit()

        scan(targetDomain, targetIP)

if __name__ == '__main__':
    main()
