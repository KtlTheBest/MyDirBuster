# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 17:48:03 2018

@author: marik
"""

try:
    import requests
except ImportError:
    print("This script requires 'requests' module! Please install it with pip!")
    raise Exception('exit')

def addWordlist(filename):
    try:
        wordlist = open(filename, "r")
        return wordlist
    except:
        return None
        
filename = "wordlist.txt"
url = "https://www.google.com/"
words = addWordlist(filename)

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
    