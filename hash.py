import hashlib

# Import the list of passwords I've already cracked
cracked_passwords = [] 
with open("Found_Passwords.txt", "r") as f:
  for line in f:
    cracked_passwords.append(line.strip())

# Get the salt from the file
with open("salt.txt", "r") as f:
  salt = f.read().strip()

# Get the list of special characters to add to a password
list_of_characters = []
with open("list_of_characters.txt", "r") as f:
  for line in f:
    list_of_characters.append(line.strip())

# Function which returns a list of passwords with the original password + a number. Ex: password -> password22, up to 99
def number_endings(password):
  list_of_others = []
  for i in range(100):
    list_of_others.append((getHash(password + str(i)),password + str(i)))
  return list_of_others

def capitalize_first_letter(string):
  if len(string) > 0:
    return string[0].upper() + string[1:]
  else:
    return string.upper()

# returns a set of all possibilities of a string with one extra character
def get_list_of_others(orig_password):
    list_of_others = []
    
    # Append the original password to the list
    list_of_others.append((getHash(orig_password),orig_password))

    # Append a first-capitalized version of the original password to the list
    # list_of_others.append((getHash(capitalize_first_letter(orig_password)),capitalize_first_letter(orig_password)))

    # Append all possible character combos with the original word to the list
    for first_char in list_of_characters:
      list_of_others.append((getHash(orig_password + first_char),orig_password + first_char))
      for second_char in list_of_characters:
        list_of_others.append((getHash(orig_password + first_char + second_char),orig_password + first_char + second_char))
        for third_char in list_of_characters:
          list_of_others.append((getHash(orig_password + first_char + second_char + third_char),orig_password + first_char + second_char + third_char))

    # return the list
    return list_of_others

# returns the hash of a string
def getHash(password):
    salted_password = (salt + password).encode('utf-8')
    hash_value = hashlib.sha256(salted_password).hexdigest()
    return hash_value


# Get the list of hashed passwords from the file
hashes = {}
hash_keys = set()
with open("hashes.txt", "r") as f:
  for line in f:
    pass_to_add = line.strip()
    hashes[pass_to_add] = '______'
    hash_keys.add(pass_to_add)



# Crack the passwords :)
def crack_passwords(hints):
  matches = 0
  newPasswords = 0
  print("Cracking passwords in " + hints + "...")
  # Start cracking with the given file of hints
  with open(hints, "r", errors='ignore') as f:
    for line in f:
      # get the list of possible passwords
      list_of_hash_to_pass = get_list_of_others(line.strip())
      # list_of_hash_to_pass.extend(number_endings(line.strip())) 
      # for each of the elements in the list
      for val in list_of_hash_to_pass:
        # if the password is not in the list of cracked passwords
        if val[1] not in cracked_passwords:
          # if the hash is in the list of hashes, we found a new Password!
          if val[0] in hashes:
            print("**** NEW Password Found ****: " + val[1])
            cracked_passwords.append(val[1])
            hashes[val[0]] = val[1]
            newPasswords += 1
            matches += 1
        # If we already found that password, notate it
        else:
          print("Password Already Found: " + val[1])
          matches += 1
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
  # The names of the files to use as hints
  files = \
  [
   'rockyoupt1.txt', 
   'rockyoupt2.txt',
  #  'phpbb.txt', 
  #  'hotmail.txt', 
  #  'myspace.txt', 
  #  'my_hints.txt', 
  #  'john.txt',
   ]

  matches = 0
  newPasswords = 0
  # Crack the passwords
  for file_name in files:
    tuple_ = crack_passwords(file_name)
    matches += tuple_[0] 
    newPasswords += tuple_[1]

  # Print the hashes with their corresponding passwords with their corresponding passwords to output file
  print_hashes()

  # Update the list of cracked passwords
  update_cracked_passwords()
  # Print to the user the stats of the cracking
  print("Password Bank holds " + str(len(cracked_passwords)) + " passwords")
  print("Found " + str(newPasswords) + " new passwords")