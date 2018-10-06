# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 17:48:03 2018

@author: marik
"""

import sys
try:
    import requests, getopt
except ImportError:
    print("This script requires 'requests' and 'getopt' module! Please install it with pip!")
    raise Exception('exit')

def addWordlist(filename):
    try:
        wordlist = open(filename, "r")
        return wordlist
    except:
        return None


def checkUrl(url):
    site = requests.get(url, allow_redirects=True)
    return site.url

def main(args):
        
    try:
        opt, vals = getopt.getopt(args, "hu:w:", ["help", "url=", "wordlist="])
    except getopt.GetoptError:
        print("use -h for help")
        return
    
    words = None    
    
    for o, val in opt:
        if o in ("-h", "--help"):
            print(sys.argv[0] + " -u <url> -w <wordlist>")
            return
        if o in ("-u", "--url"):
            url = val
            url = checkUrl(url)
        if o in ("-w", "--wordlist"):
            words = addWordlist(val)
    
    result = open("result.txt", "w")
    
    if words == None:
        print("Error opening the file! Check if the dictionary exists!")
        raise Exception('exit')
    
    site = requests.get(url)
    result.write(str(site.status_code) + ' ' + url)
    result.write('\n')
    
    for word in words:
        site = requests.get(url + word)
        result.write(str(site.status_code) + ' ' + url + word)
        result.write('\n')
        
    result.close()
    words.close()


if __name__ == "__main__":
    main(sys.argv[1:])
