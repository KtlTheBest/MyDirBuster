# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 17:48:03 2018

@author: marik
"""

import sys, os
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
    url_template = re.compile(r'http(s)?://.+\.\w{2,4}')
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

    wordlists = []
    wordlistOK = False

    for o, val in opt:
        if o in ("-h", "--help"):
            print(sys.argv[0] + " -u <url> -w <wordlist>")
            return
        if o in ("-u", "--url"):
            url = val
            url = checkUrl(url)
        if o in ("-w", "--wordlist"):
            wordlists.append(val)
            wordlistOK = True


    if wordlistOK == True:
        if addWordlist(wordlists[0]) == None:
            print("Error opening the file! Check if the filename specified!")
            raise Exception('exit')
    else:
        # Need to iterate over files in wordlists directory
        wordlistDir = '.' + os.sep + 'wordlists'
        for subdir, dirs, files in os.walk(wordlistDir):
            for file in files:
                if file.endswith(".txt"):
                    wordlists.append(os.path.join(subdir, file))


    result = open("result.txt", "w")

    site = requests.get(url)
    result.write(str(site.status_code) + ' ' + url)
    result.write('\n')

    for wordlist in wordlists:
        words = addWordlist(wordlist)

        # print("Checking for " + wordlist + "...")
        for word in words:
            site = requests.get(url + word)
            result.write(str(site.status_code) + ' ' + url + word)
            result.write('\n')
        # print("OK")

        words.close()

    result.close()

if __name__ == "__main__":
    main(sys.argv[1:])
