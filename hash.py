from dataclasses import replace
from fileinput import close
import hashlib
import os
from re import A

# Import the list of passwords I've already cracked
cracked_passwords = []
with open("./miscLists/Found_Passwords.txt", "r") as f:
    for line in f:
        cracked_passwords.append(line.strip())

# Get the salt from the file
with open("./miscLists/salt.txt", "r") as f:
    salt = f.read().strip()

# Get the list of special characters to add to a password
list_of_characters = []
with open("./miscLists/list_of_characters.txt", "r") as f:
    for line in f:
        list_of_characters.append(line.strip())

# Get the list of hashed passwords from the file
hashes = {}
hash_keys = set()
with open("./miscLists/hashes.txt", "r") as f:
    for line in f:
        pass_to_add = line.strip()
        hashes[pass_to_add] = '______'
        hash_keys.add(pass_to_add)


def test_single_word(word_to_test):
    if getHash(word_to_test) in hash_keys:
        print("    **** NEW Password Found **** : " + word_to_test)
    else:
        print("Password Not Found: " + word_to_test)

# Function which returns a list of passwords with the original password + a number. Ex: password -> password22, up to 99


def number_endings(password):
    list_of_others = []
    for i in range(100):
        list_of_others.append((getHash(password + str(i)), password + str(i)))
    return list_of_others


def get_longest_words():
    longest_words = []
    counter = 0
    with open("./miscLists/longest_words.txt", "r") as f:
        for line in f:
            longest_words.append((getHash(line.strip()), line.strip()))
            counter += 1
            if counter % 10000 == 0:
                print("Processed " + str(counter) + " words")
    return longest_words


def capitalize_first_letter(string):
    if len(string) > 0:
        return string[0].upper() + string[1:]
    else:
        return string.upper()

# returns a list of concatenated common words in english


def get_common_words_concatenated():
    common_words = []
    returnMe = []
    with open("./miscLists/common_words.txt", "r") as f:
        for line in f:
            common_words.append(line.strip())
    for first_word in common_words:
        print("first_word: " + first_word)
        for second_word in common_words:
            # print("concatenating " + first_word)
            # print("with " + second_word)
            # print("to get: " + first_word + second_word)
            full_word = first_word + second_word
            returnMe.append((getHash(full_word), full_word))
            for third_word in common_words:
                returnMe.append(
                    (getHash(full_word + third_word), full_word + third_word))
        for val in returnMe:
            # if the password is not in the list of cracked passwords
            if val[1] not in cracked_passwords:
                # if the hash is in the list of hashes, we found a new Password!
                if val[0] in hashes:
                    print("     **** NEW Password Found ****: " + val[1])
                    cracked_passwords.append(val[1])
                    hashes[val[0]] = val[1]
            # If we already found that password, notate it
            else:
              print("Password Already Found: " + val[1])
            returnMe = []
            # for fourth_word in common_words:
            #   returnMe.append((getHash(full_word + third_word + fourth_word), full_word + third_word + fourth_word))
            # for fifth_word in common_words:
            #   returnMe.append((getHash(full_word + third_word + fourth_word + fifth_word), full_word + third_word + fourth_word + fifth_word))
    # return returnMe

# returns a list of all random 4-character strings


def get_random_strings():
    random_strings = []
    with open("./miscLists/longest_words.txt", "r") as f:
        for line in f:
            replaceword = line.strip()
            random_strings.append((getHash(replaceword.replace('a', '@')), replaceword.replace('a', '@')))
            random_strings.append((getHash(replaceword.replace('a', '@').replace('e','3')),replaceword.replace('a','@').replace('e','3'))) 
            random_strings.append((getHash(replaceword.replace('a', '@').replace('e','3').replace('i','1')),replaceword.replace('a','@').replace('e','3').replace('i','1')))
            random_strings.append((getHash(replaceword.replace('a', '@').replace('e','3').replace('i','1').replace('o','0')),replaceword.replace('a','@').replace('e','3').replace('i','1').replace('o','0')))
    random_strings.extend(get_list_of_others(random_strings))
    return random_strings


def large_file_hash():
    print("Processing the 65 gb file Now")
    print("This will take a while")
    print("size of hashes: " + str(len(hashes)))
    print("size of cracked passwords: " + str(len(cracked_passwords)))
    print("size of hash keys: " + str(len(hash_keys)))
    newPasswords = 0
    matches = 0
    currentList = []
    counter = 0
    with open("./mistLists/new_word_in_large.txt", "w") as out:
        with open("./mistLists/sorted-wordlist", "r", errors='ignore') as f:
            try:
                for line in f:
                    currentList.append((getHash(line.strip()), line.strip()))
                    counter += 1
                    if counter % 100000000 == 0:
                        print("Processed " + str(counter) + " words")
                    if counter % 100000000 == 0:
                        print("Reset for RAM SAVING")
                        # process the data and reset currentList
                        for val in currentList:
                            # if the password is not in the list of cracked passwords
                            if val[1] not in cracked_passwords:
                                # if the hash is in the list of hashes, we found a new Password!
                                if val[0] in hashes:
                                    print(
                                        "     **** NEW Password Found ****: " + val[1])
                                    cracked_passwords.append(val[1])
                                    hashes[val[0]] = val[1]
                                    newPasswords += 1
                                    matches += 1
                                    out.write(val[1] + "\n")
                            # If we already found that password, notate it
                            else:
                                # print("Password Already Found: " + val[1])
                                matches += 1
                        currentList = []
            except Exception as e:
                out.close()
                print(e)


# Gather all permutaions up to a 5-letter word
def get_random_permutations():
    returnMe = []
    characters = []
    # read in the file of all alphabetical characters
    with open("./miscLists/alphanum.txt", "r") as f:
        for line in f:
            characters.append(line.strip())
    # get all permutations of the characters
    for first_char in characters:
        returnMe.append((getHash(first_char), first_char))
        print("appending " + first_char)
        for second_char in characters:
            returnMe.append((getHash(first_char + second_char),
                            first_char + second_char))
            # print("appending " + first_char + second_char)
            for third_char in characters:
                returnMe.append((getHash(
                    first_char + second_char + third_char), first_char + second_char + third_char))
                # print("appending " + first_char + second_char + third_char)
                for fourth_char in characters:
                    returnMe.append((getHash(first_char + second_char + third_char +
                                    fourth_char), first_char + second_char + third_char + fourth_char))
                    # print("appending " + first_char + second_char + third_char + fourth_char)
                    for fifth_char in characters:
                        returnMe.append((getHash(first_char + second_char + third_char + fourth_char +
                                        fifth_char), first_char + second_char + third_char + fourth_char + fifth_char))
                        # print("appending " + first_char + second_char + third_char + fourth_char + fifth_char)
    return returnMe

# returns a list of passwords with common words using leet speak


def get_leet_speak():
    leet_speak = {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [], 'I': [], 'J': [], 'K': [], 'L': [], 'M': [
    ], 'N': [], 'O': [], 'P': [], 'Q': [], 'R': [], 'S': [], 'T': [], 'U': [], 'V': [], 'W': [], 'X': [], 'Y': [], 'Z': []}
    returnMe = []
    with open("./miscLists/leet_speak.txt", "r") as f:
        for line in f:
            element = line.split()
            for i in range(len(element)-1):
                # print("first element is: " + element[i])
                # print("second element is: " + element[i+1])
                if len(leet_speak[element[0]]) == 0:
                    leet_speak[element[0]] = [element[i+1]]
                else:
                    leet_speak[element[0]].append(element[i + 1])
    # print(leet_speak)
    files = os.listdir("./wordLists")
    for file in files:
        print("Processing file: " + file)
        with open("./wordLists/" + file, "r") as f:
            for line in f:
                word = line.strip()
                for letter in word:
                    if letter.upper() in leet_speak:
                        for replacement in leet_speak[letter.upper()]:
                            # print("replacing " + str(letter) + " in " + word + " with " + replacement)
                            word = word.replace(letter, replacement)
                            returnMe.append((getHash(word), word))
    return returnMe

# returns a list of words with the original word + 1 - 3 special characters


def get_extension_of_list(list_of_hash_to_pass):
    returnMe = []
    for orig_password in list_of_hash_to_pass:
        for first_char in list_of_characters:
            returnMe.append(
                (getHash(orig_password + first_char), orig_password + first_char))
            for second_char in list_of_characters:
                returnMe.append((getHash(orig_password + first_char +
                                second_char), orig_password + first_char + second_char))
                for third_char in list_of_characters:
                    returnMe.append((getHash(orig_password + first_char + second_char +
                                    third_char), orig_password + first_char + second_char + third_char))
    return returnMe

# returns a set of all possibilities of a string with one extra character


def get_list_of_others(orig_list):
    print('in list of others')
    list_of_others = []
    characters = []
    # read in the file of all alphabetical characters
    with open("./miscLists/alphanum.txt", "r") as f:
        for line in f:
            characters.append(line.strip())
    for orig_password in orig_list:
        print("password: " + orig_password[1])
        for first_char in characters:
          list_of_others.append((getHash(orig_password[1] + first_char), orig_password[1] + first_char))
          # for second_char in characters:
          #     list_of_others.append((getHash(orig_password[1] + first_char + second_char), orig_password[1] + first_char + second_char))
          #     for third_char in characters:
          #         list_of_others.append((getHash(orig_password[1] + first_char + second_char + third_char), orig_password[1] + first_char + second_char + third_char))

        # for each of the elements in the list
        for val in list_of_others: # if the password is not in the list of cracked passwords
            if val[1] not in cracked_passwords:
                # if the hash is in the list of hashes, we found a new Password!
                if val[0] in hashes:
                    print("     **** NEW Password Found ****: " + val[1])
                    cracked_passwords.append(val[1])
                    hashes[val[0]] = val[1]
            # If we already found that password, notate it
            else:
                print("Password Already Found: " + val[1])

    # Append a first-capitalized version of the original password to the list
    # list_of_others.append((getHash(capitalize_first_letter(orig_password)),capitalize_first_letter(orig_password)))

    # Append all possible character combos with the original word to the list
    # list_of_others.extend(get_extension_of_list(list_of_others))

    # return the list
    return list_of_others

# returns the hash of a string


def getHash(password):
    salted_password = (salt + password).encode('utf-8')
    hash_value = hashlib.sha256(salted_password).hexdigest()
    return hash_value

# Crack the passwords :)


def crack_passwords(hints, pre_determined_corpus=False):
    matches = 0
    newPasswords = 0
    # print("Cracking passwords in " + hints + "...")
    # Start cracking with the given file of hints
    list_of_hash_to_pass = []
    with open(hints, "r", errors='ignore') as f:
        for line in f:
            # generate the list of possible passwords
            if not pre_determined_corpus:
                print("Generating list of possible passwords...")
                # You can uncomment any one of these to use those functions.
                # list_of_hash_to_pass = get_leet_speak()
                # list_of_hash_to_pass = get_common_words_concatenated()
                # list_of_hash_to_pass = get_random_permutations()
                # list_of_hash_to_pass = get_longest_words()
                # list_of_hash_to_pass = get_random_strings()
                # list_of_hash_to_pass = get_list_of_others(line.strip())

                # list_of_hash_to_pass.extend(number_endings(line.strip()))
            # Parse a pre-determined list of words
            else:
                print("Begin Reading In Pre-Determined Corpus")
                list_of_hash_to_pass.append((getHash(line.rstrip()), line.rstrip()))

            print("searching for correctly guessed passwords")
            # for each of the elements in the list
            for val in list_of_hash_to_pass:
                # if the password is not in the list of cracked passwords
                if val[1] not in cracked_passwords:
                    # if the hash is in the list of hashes, we found a new Password!
                    if val[0] in hashes:
                        print("     **** NEW Password Found ****: " + val[1])
                        cracked_passwords.append(val[1])
                        hashes[val[0]] = val[1]
                        newPasswords += 1
                        matches += 1
                # If we already found that password, notate it
                else:
                    print("Password Already Found: " + val[1])
                    hashes[val[0]] = val[1]
                    matches += 1
            if pre_determined_corpus:
                return matches, newPasswords
    return matches, newPasswords

# print the hashes with their corresponding passwords


def print_hashes():
    # Print the hash map to a file
    with open("cracked.txt", "w") as f:
        for key in hashes:
            f.write(key + ":" + hashes[key] + "\n")


# Print the cracked passwords to a file
def update_cracked_passwords():
    with open("Found_Passwords.txt", "w") as f:
        for password in cracked_passwords:
            f.write(password + "\n")


# Main function
if __name__ == "__main__":

    # Tests a single word that I have a hunch about
    # test_single_word("phanekham")

    # Crack the passwords in the large 65GB file:
    # large_file_hash()

    # get a list of all file names in a directory
    files = os.listdir("./wordLists")

    matches = 0
    newPasswords = 0

    # # # crack pre-determined corpus
    # tuple_ = crack_passwords(
    #     './wordLists/' + files[0], pre_determined_corpus=True)
    # # matches += tuple_[0]
    # # newPasswords += tuple_[1]

    # Uncomment this if you want to generate cracked.txt from the already found passwords
    # files = ['./miscLists/Found_Passwords.txt']

    for file_name in files:
      print("Cracking " + file_name + "...")
      tuple_ = crack_passwords(file_name)
      matches += tuple_[0]
      newPasswords += tuple_[1]

    # # Print the hashes with their corresponding passwords with their corresponding passwords to output file
    print_hashes()

    # # Update the list of cracked passwords
    update_cracked_passwords()
    # # Print to the user the stats of the cracking
    print("Password Bank holds " + str(len(cracked_passwords)) + " passwords")
    print("Found " + str(newPasswords) + " new passwords")
