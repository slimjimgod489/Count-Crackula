# passworcrackalack
This is passwordcrackalack, a surprisingly well-designed hash cracker. 
# examples
to run an dictionary attack you would type:

python3 passwordcrackalack.py -h (your hash) -t (type of hash) -w (dictrionary you prefer)

I included a text file lableled "mega.txt" with a lot of potential passwords and every word in the english dictionary

To run a bruteforce attack you would run

python3 passwordcrackalack.py -h (your hash) -t (type of hash) -n (put this instead of -w)

This linearly guesses words.
Optionally, if you wanted to add "-v" at the end of your prompt and you will print out each guess, but this will make the code take much much longer.

Additionally if you want you can just type "python3 passwordcrackalack.py -i" for a quick tutorial


Thank you to Vanson Spaghetti for helping my brute force algorithim
