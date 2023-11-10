import random
import string
import hashlib
import time

#to operate, run the code. Input thing to try and bruteforce. Kill terminal and run again to retry.

def bruteForce(password):
    tries = 0
    startTime = time.time()
    print("Crackalackinationalating...")
    while True:
        guess = ''.join(random.choices(string.printable, k=len(password)))
        tries += 1
        # print(tries,guess) #uncomment to print each guess and try in chat
        if guess == password:
            print("it took", (time.time()) - startTime, "seconds")
            return tries,guess

def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature   



password = (input("Enter the password to crack: "))

tries , guess = bruteForce(password)

msg = "This is how many guesses it took to crack your password: "
msgTwo = "This is the password: "
print(msg + str(tries))
print(msgTwo + guess)
