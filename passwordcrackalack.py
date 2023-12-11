#imports and stuff
import getopt
import hashlib
import sys
import os
import time
import itertools , string

#introductory
print("  ")
print("Passwordcrackalack")
print("for my vampire teacher")

#simple tutorial
def tutorial():
    print(" ")
    print("Information:")
    print(" Options:")
    print(" (-h) Hash")
    print(" (-t) Type of hash, supported = md5, sha1 ")
    print(" (-w) Wordlist, this is your dictionary attack")
    print(" (-n) replace -w with this to bruteforce")
    print(" (-v) Verbose prints every try, just takes longer\n")

#thought it'd be cool to have your OS print out. so awesome
def checkOS():
    if os.name == "nt":
        operatingSystem = "Windows"
    elif os.name == "linux":
        operatingSystem = "Linux"
    else:
        operatingSystem = "Wth are you running this on"
    return operatingSystem


class hashCracking:
    

    # This section is the main stuff
    def hashCrackWordlist(self, userHash, hashType, wordlist, verbose, bruteForce = False):
        start = time.time()
        solved = False
        self.lineCount = 0
        if "md5" in hashType:
            h = hashlib.md5
        elif "sha1" in hashType:
            h = hashlib.sha1
        elif "sha224" in hashType:
            h = hashlib.sha224
        elif "sha256" in hashType:
            h = hashlib.sha256
        elif "sha384" in hashType:
            h = hashlib.sha384
        elif "sha512" in hashType:
            h = hashlib.sha512
        else:
            print(f"[-] Is {hashType} a supported hash type?")
            exit()
        #the bruteforce algorithim
        if bruteForce is True:
            while True:
                attempts = 0
                alphabet = string.printable
                for length in range (1 , len(alphabet)):
                    for combination in itertools.product(alphabet , repeat = length):
                        bruteForceGuess = "".join(combination)
                        attempts += 1
                        if verbose is True:
                            print(attempts , bruteForceGuess)
                        if h(bruteForceGuess.encode('utf-8')).hexdigest() == userHash:
                            end = time.time()
                            print(f"\n[+] Hash is: {bruteForceGuess}")
                            print(f"Combinations tried: {attempts}")
                            print(f" Time: {round((end - start), 2)} seconds")
                exit()
        else:
            #dictionary algorithim
            with open(wordlist, "r") as file:
                for line in file:
                    line = line.strip()
                    encodeLine= str.encode(line)
                    lineHash = h(encodeLine).hexdigest()
                    if verbose is True:
                        sys.stdout.write('\r' + str(line) + ' ' * 20)
                        sys.stdout.flush()

                    if str(lineHash) == str(userHash.lower()):
                        end = time.time()
                        print(f"\n[+] Hash is: {line}")
                        print(f" Words tried: {self.lineCount}")
                        print(f" Time: {round((end - start), 2)} seconds")
                        savedHashFile = open('SavedHashes.txt', 'a+')
                        for solvedHash in savedHashFile:
                            if lineHash in solvedHash.split(":")[1].strip():
                                solved = True
                        if solved is False:
                            print(" Hash to SavedHashes.txt")
                            savedHashFile.write('%s:{}'.format(lineHash) % line)
                            savedHashFile.write('\n')
                        savedHashFile.close()
                        exit()
                    else:
                        self.lineCount = self.lineCount + 1

            end = time.time()
            print("\n[-] Cracking Failed")
            print(" Reached end of wordlist")
            print(f" Words tried: {self.lineCount}")
            print(f" Time: {round((end - start), 2)} seconds")
            exit()

#this is what runs at the beginning, minor tutorial and other stuff
def main(argv):
    hashType = None
    userHash = None
    wordlist = None
    verbose = None
    numbersBruteForce = False
    print(f"[Running on {checkOS()}]\n")
    try:
        opts, args = getopt.getopt(argv, "ih:t:w:nv", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print(' type python3 passwordcrackalack.py -h (your hash) -t (type of hash) -w (dictrionary you prefer)')
        print(' Type python3 passwordcrackalack.py -i for tutorial')
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-i':
            tutorial()
            sys.exit()
        elif opt in ("-t", "--type"):
            hashType = arg.strip().lower()
        elif opt in ("-h", "--hash"):
            userHash = arg.strip().lower()
        elif opt in ("-w", "--wordlist"):
            wordlist = arg
        elif opt in ("-v", "--verbose"):
            verbose = True
        elif opt in ("-n", "--numbers"):
            numbersBruteForce = True
    if not (hashType and userHash):
        print(' python3 passwordcrackalack.py -h (your hash) -t (type of hash) -w (dictrionary you prefer)')
        sys.exit()

    with open('SavedHashes.txt', 'a+') as savedHashFile:
        for solvedHash in savedHashFile:
            solvedHash = solvedHash.split(":")
            if userHash.lower() == solvedHash[1].strip():
                print(f" Saved Hash is: {solvedHash[0]}")
                exit()
        else:
            print(f" Hash: {userHash}")
            print(f" Hash type: {hashType}")
            print(f" Wordlist: {wordlist}")
            print("- Cracking...")
            try:
                h = hashCracking()
                h.hashCrackWordlist(userHash, hashType, wordlist, verbose, bruteForce=numbersBruteForce)

            except IndexError:
                print("\n[-] Hash not cracked:")
                print(" Reached end of wordlist")
                print(" Try another wordlist")
                print(f" Words tried: {h.lineCount}")

            except KeyboardInterrupt:
                print("\n[Exiting...]")
                print(f" Words tried: {h.lineCount}")

            except IOError as e:
                print("\n[-] Couldn't find wordlist")
                print(" did you type .txt? or whatever the extention is?")
                print(f"This is what you typed > {wordlist}")


if __name__ == "__main__":
    main(sys.argv[1:])