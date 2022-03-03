# Password_Cracking
Repository to store all ventures on cracking passwords for INFOSEC lab

Used MANY different word lists and password lists

Some of the Large ones I could not add to the file:
https://crackstation.net/crackstation-wordlist-password-cracking-dictionary.htm

Multiple resources from this:
https://github.com/xajkep/wordlists

All of the input files from this github repo:
https://github.com/danielmiessler/SecLists

Some Heuristic Inputs

# Running the program
### Pre-Requisite
Download the "wordLists" folder from the github repo [here](https://github.com/Gouldilocks/Password_Cracking/tree/master/wordLists)


### Running the command
You can run the program by typing the following command:
```
python3 hash.py
```

There are a multitude of ways to modify the running of the program.
* I added several commands and functions to allow for all sorts of changes to be made.
* there are two main running configuration:
  * The first is running "without pre-determined corpus", which essentially means I am generating the passwords myself from scratch or from a little list of characters. I used this to do things like brute force crack the 4-digit passwords.
  * The second is running "with pre-determined corpus", which essentially means I am taking a large list of passwords and checking if any of those passwords are in the list of hashes. I used this to find the larger passwords like "pneumoencephalographically"
  * You can also combine these with functions which I made as "modifier" functions. If I uncomment a certain line, like "get_extension_of_list()", I can get permutations of a list of passwords. That function in particular will add all permutations of 3 characters added to the end of a password, and return an array of those new passwords. I used this to get passwords like "password#^$".

* In its current state, it runs all word lists in text files located in the "wordLists" folder.

# Program's Design
* Like I mentioned before, I had many different ways to run the program, which included modifiers and list getters.
* I also implemented a password management system because of this. I used a text file called "Found_Passwords.txt" to store all passwords which I have already found, and then would run random permutations of all my list functions and modifier functions until I came across a new password that did not exist in that list. I did this since it was very hard for me to tell when I had found a new password that I never had seen before, or when it was a new one entirely. Then, at the end of my time working on the project, I simply ran the code with my list of found passwords to generate my "cracked.txt" file for submission.
* There is also one special function which I implemented solely for the purpose of running a 65GB wordlist I found on the internet. It turns out that storing all those words in an array takes way too much space, so every now and then, while running it, I would search for passwords that exist in my current list, and then empty the list. That function would run alone in main, and it is called "large_file_hash()". The wordlist is [The b0n3z Wordlist](http://download.g0tmi1k.com/wordlists/large/b0n3z-wordlist-sorted_REPACK-69.3GB.7z)