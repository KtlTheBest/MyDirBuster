# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 17:48:03 2018

@author: marik
"""

printAll = False

import sys, os
try:
    import requests, getopt, re
except ImportError:
    print("This script requires 'requests', 're' and 'getopt' module! Please install it with pip!")
    raise Exception('exit')

def writeCode(site, result):
    result.write(str(site.status_code) + " " + site.url + "\n")

def writeUsefulCode(site, result):
    if site.status_code != 404:
        writeCode(site, result)

def writeResult(site, result):
    if not printAll:
        writeUsefulCode(site, result)
    else:
        writeCode(site, result)

def addWordlist(filename):
    try:
        wordlist = open(filename, "r")
        return wordlist
    except:
        return None


def clean(str):
    return str.rstrip()

def checkUrl(url):
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

def finish():
    raise Exception('exit')

def main(args):
    #Initialization section
    outputFilename = "result.txt"
    global printAll
    #################

    try:
        opt, vals = getopt.getopt(args, "ahu:w:o:", ["all", "help", "url=", "wordlist=", "output="])
    except getopt.GetoptError:
        print("use -h for help")
        return

    wordlists = []
    wordlistOK = False

    for o, val in opt:
        if o in ("-h", "--help"):
            print(sys.argv[0] + " -u <url> -w <wordlist> -o <output-Filename>")
            return
        if o in ("-u", "--url"):
            url = val
            url = checkUrl(url)
        if o in ("-w", "--wordlist"):
            wordlists.append(val)
            wordlistOK = True
        if o in ("-o", "--output"):
            outputFilename = val
        if o in ("-a", "--all"):
            printAll = True

    if wordlistOK == True:
        if addWordlist(wordlists[0]) == None:
            print("Error opening the file! Check if the filename specified!")
            finish()
    else:
        wordlistDir = '.' + os.sep + 'wordlists'
        for subdir, dirs, files in os.walk(wordlistDir):
            for file in files:
                if file.endswith(".txt"):
                    wordlists.append(os.path.join(subdir, file))

    try:
        result = open(outputFilename, "w")
    except:
        print("Some unexpected error when trying to open file!")
        finish()

    site = requests.get(url)
    result.write(str(site.status_code) + ' ' + url)
    result.write('\n')

    for wordlist in wordlists:
        words = addWordlist(wordlist)

        for word in words:
            word = clean(word)
            site = requests.get(url + word)
            print("Checking '/{}' folder".format(word))
            writeResult(site, result)

        words.close()

    result.close()

if __name__ == "__main__":
    main(sys.argv[1:])
    print("Done!")
