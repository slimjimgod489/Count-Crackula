import getopt
import hashlib
import sys
import os
import time

print("  ")
print("Passwordcrackalack")
print("for my vampire teacher")


def tutorial():
    print(" ")
    print("Information:")
    print(" Options:")
    print(" (-h) Hash")
    print(" (-t) Type of hash, supported = md5, sha1 ")
    print(" (-w) Wordlist, this is your dictionary attack")
    print(" (-n) Numbers of each attempt")
    print(" (-v) Verbose prints every try, just takes longer\n")


def checkOS():
    if os.name == "nt":
        operatingSystem = "Windows"
    elif os.name == "linux":
        operatingSystem = "Linux"
    else:
        operatingSystem = "Wth are you running this on"
    return operatingSystem


class hashCracking:

    def hashCrackWordlist(self, userHash, hashType, wordlist, verbose, bruteForce=False):
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
        if bruteForce is True:
            while True:
                line = self.lineCount
                line.strip()
                numberHash = h(line).hexdigest().strip()
                if verbose is True:
                    sys.stdout.write('\r' + str(line) + ' ' * 20)
                    sys.stdout.flush()
                if numberHash.strip() == userHash.strip().lower():
                    end = time.time()
                    print("\n[+] Hash is: %s" % self.lineCount)
                    print(" Time: %s seconds" % round((end - start), 2))
                    savedHashFile = open('SavedHashes.txt', 'a+')
                    for solvedHash in savedHashFile:
                        if numberHash in solvedHash.split(":")[1].strip():
                            solved = True
                    if solved is False:
                        print(" Hash to SavedHashes.txt")
                        savedHashFile.write('%s:{}'.format(numberHash) % line)
                        savedHashFile.write('\n')
                    savedHashFile.close()
                    exit()
                else:
                    self.lineCount = self.lineCount + 1
        else:
            with open(wordlist, "r") as infile:
                for line in infile:
                    line = line.strip()
                    encodeline= str.encode(line)
                    lineHash = h(encodeline).hexdigest()
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
        print(' type python passwordcrackalack -h (your hash) -t (type of hash) -w (dictrionary you prefer)')
        print(' Type python passwordcrackalack -i for tutorial')
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
        print(' python passwordcrackalack -h (your hash) -t (type of hash) -w (dictrionary you prefer)')
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
                print(" Is this right?")
                print(f"[>] {wordlist}")


if __name__ == "__main__":
    main(sys.argv[1:])