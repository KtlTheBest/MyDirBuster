import sys, os, Queue, threading
try:
    import requests, getopt, re
except ImportError:
    print("This script requires 'requests', 're' and 'getopt' module! Please install it with pip!")
    raise Exception('exit')


outputFilename = "result.txt"
UrlInOption = False
printAll = False
fastCheck = True
extended = False
wordQueue = Queue.Queue()
finished = threading.Event()
lock = threading.Semaphore()

def writeCode(site, result):
    try:
        result.write(str(site.status_code) + " " + site.url + "\n")
    except:
        pass


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


def cleanWord(str):
    return str.rstrip()


def cleanUrl(url):
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


def inputUrl():
    url = raw_input("Input URL: ")
    url = cleanUrl(url)
    return url


def resolveArgs(opt):
    for o, val in opt:
        if o in ("-h", "--help"):
            print(sys.argv[0] + " -u <url> -w <wordlist> -o <output-Filename>")
            return
        if o in ("-u", "--url"):
            UrlInOption = True
            url = val
            url = cleanUrl(url)
        if o in ("-w", "--wordlist"):
            wordlists.append(val)
            wordlistOK = True
        if o in ("-o", "--output"):
            outputFilename = val
        if o in ("-a", "--all"):
            printAll = True
        if o in ("-f", "--full"):
            fastCheck = False
        if o in ("-e", "--extended"):
            extended = True

def checkUrl(url, result):
    global wordQueue

    while True:
        try:
            word = wordQueue.get(False)
        except Queue.Empty:
            finished.set()
            return

        lock.acquire()
        print("Checking {}{}...".format(url, word))
        lock.release()
        try:
            site = requests.get(url + word)
        except KeyboardInterrupt:
            lock.acquire()
            print("Skipping...")
            lock.release()
            return
        except requests.ConnectionError():
            return

        writeResult(site, result)


def getWordlists(fastCheck):
    wordlistDir = '.' + os.sep + 'wordlists'
    wordlists = []
    if fastCheck == True:
        wordlists.append(wordlistDir + os.sep + "common.txt")
    else:
        for subdir, dirs, files in os.walk(wordlistDir):
            for file in files:
                if file.endswith(".txt"):
                    wordlists.append(os.path.join(subdir, file))
    return wordlists

def addExtensions(word):
    ext_list = [
        ".html",
        ".html"
        ".php",
        ".aspx",
    ]
    for i in ext_list:
        wordQueue.put(word + i)

def main(args):
    try:
        opt, vals = getopt.getopt(args, "ahu:w:o:fe", ["all", "help", "url=", "wordlist=", "output=", "full", "extended"])
    except getopt.GetoptError:
        print("use -h for help")
        return

    wordlistOK = False

    resolveArgs(opt)

    if not UrlInOption:
        url = inputUrl()

    if wordlistOK == True:
        if addWordlist(wordlists[0]) == None:
            print("Error opening the file! Check if the filename specified!")
            finish()
    else:
        wordlists = getWordlists(fastCheck)

    try:
        result = open(outputFilename, "w")
    except:
        print("Some unexpected error when trying to open {}!".format(file))


    site = requests.get(url)
    result.write(str(site.status_code) + ' ' + url)
    result.write('\n')

    for wordlist in wordlists:
        words = addWordlist(wordlist)
        print("DEBUG: " + wordlist)

        for word in words:
            word = cleanWord(word)
            wordQueue.put(word)
            if extended == True:
                addExtensions(word, wordQueue)
            for i in range(10):
                t = threading.Thread(target = checkUrl, args = (url, result))
                t.start()

        if finished.isSet():
            words.close()
            result.close()

if __name__ == "__main__":
    main(sys.argv[1:])
    print("Done!")
