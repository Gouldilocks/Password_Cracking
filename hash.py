import hashlib

with open("salt.txt", "r") as f:
  salt = f.read().strip()

list_of_characters = []
with open("list_of_characters.txt", "r") as f:
  for line in f:
    list_of_characters.append(line.strip())

# returns a set of all possibilities of a string with one extra character
def get_list_of_others(orig_password):
    list_of_others = []
    
    # Append the original password to the list
    list_of_others.append((getHash(orig_password),orig_password))

    # Append all possible character combos with the original word to the list
    for char in list_of_characters:
        list_of_others.append((getHash(orig_password + char),orig_password + char))

    for i in range(100):
      list_of_others.append((getHash(orig_password + str(i)),orig_password + str(i)))

    # return the list
    return list_of_others

# returns the hash of a string
def getHash(password):
    salted_password = (salt + password).encode('utf-8')
    hash_value = hashlib.sha256(salted_password).hexdigest()
    return hash_value



hashes = {}
hash_keys = set()
with open("hashes.txt", "r") as f:
  for line in f:
    pass_to_add = line.strip()
    hashes[pass_to_add] = '______'
    hash_keys.add(pass_to_add)

cracked_passwords = [] 
with open("rockyou.txt", "r", errors='ignore') as f:
  for line in f:
    list_of_hash_to_pass = get_list_of_others(line.strip())

    # strip new line character
    # password = line.strip()

    # find the hash of the password I want to check for
    # salted_password = (salt + password).encode('utf-8')
    # hash_value = hashlib.sha256(salted_password).hexdigest()

    # Check if the password is in hashes.txt
    # if hash_value in hash_keys and password not in cracked_passwords:
    # for each of the elements in the list
    for val in list_of_hash_to_pass:
      # if the password is not in the list of cracked passwords
      if val[1] not in cracked_passwords:
        # if the hash is in the list of hashes
        if val[0] in hashes:
          print("Password Found: " + val[1])
          cracked_passwords.append(val[1])
          hashes[val[0]] = val[1]

print("Found " + str(len(cracked_passwords)) + " passwords")


# Print the hash map to a file
with open("cracked.txt", "w") as f:
  for key in hashes:
    f.write(key + ":" + hashes[key] + "\n")
