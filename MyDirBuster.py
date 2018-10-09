# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 17:48:03 2018

@author: marik
"""

import sys
try:
    import requests, getopt, re
except ImportError:
    print("This script requires 'requests', 're' and 'getopt' module! Please install it with pip!")
    raise Exception('exit')

def addWordlist(filename):
    try:
        wordlist = open(filename, "r")
        return wordlist
    except:
        return None


def checkUrl(url):
    # Need to check if the url has the 'https://example.com' format
    # Need to resolve the syntax errors    
    url_template = re.compile(r'http(s)?://.+\.[2-3]')
    check = url_template.match(url)
    if not check:
        url = "http://" + url;
    
    try:
        site = requests.get(url, allow_redirects=True)
    except:
        print("There's probably a typo in a url...")
        raise Exception('exit')
        
    return site.url

def main(args):
    
    try:
        opt, vals = getopt.getopt(args, "hu:w:", ["help", "url=", "wordlist="])
    except getopt.GetoptError:
        print("use -h for help")
        return
    
    words = None
    wordlistOK = False
    
    for o, val in opt:
        if o in ("-h", "--help"):
            print(sys.argv[0] + " -u <url> -w <wordlist>")
            return
        if o in ("-u", "--url"):
            url = val
            url = checkUrl(url)
        if o in ("-w", "--wordlist"):
            words = addWordlist(val)
            wordlistOK = True
    
    result = open("result.txt", "w")
    
    if words == None:
        if wordlistOK == True:
            print("Error opening the file! Check if the filename specified!")
        else:
            print(sys.argv[0] + " -u <url> -w <wordlist>")
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
