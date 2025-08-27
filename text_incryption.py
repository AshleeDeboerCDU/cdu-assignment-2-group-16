import string
import os

# show where files are to make sure it works
print(f"Looking for files in: {os.path.dirname(os.path.abspath(__file__))}")

# encrypts one letter based on shifts
def encrypt_letter(c, s1, s2):
    if c.islower():
        # first half of lowercase
        if c in 'abcdefghijklm':
            shift = s1 * s2  # multiply shifts
            pos = string.ascii_lowercase.find(c)
            new_pos = (pos + shift) % 26
            return string.ascii_lowercase[new_pos]
        else:
            # second half lowercase
            shift = s1 + s2
            pos = string.ascii_lowercase.find(c)
            new_pos = (pos - shift) % 26
            return string.ascii_lowercase[new_pos]
    elif c.isupper():
        # first half uppercase
        if c in 'ABCDEFGHIJKLM':
            pos = string.ascii_uppercase.find(c)
            new_pos = (pos - s1) % 26
            return string.ascii_uppercase[new_pos]
        else:
            # second half uppercase
            shift = s2 * s2  # square shift2
            pos = string.ascii_uppercase.find(c)
            new_pos = (pos + shift) % 26
            return string.ascii_uppercase[new_pos]
    return c  # keep non-letters same

# decrypts one letter, reverses the encrypt
def decrypt_letter(c, s1, s2):
    temp = c  # temp var for letter
    if temp.islower():
        if temp in 'abcdefghijklm':
            shift = s1 * s2
            pos = string.ascii_lowercase.find(temp)
            new_pos = (pos - shift) % 26
            return string.ascii_lowercase[new_pos]
        else:
            shift = s1 + s2
            pos = string.ascii_lowercase.find(temp)
            new_pos = (pos + shift) % 26
            return string.ascii_lowercase[new_pos]
    elif temp.isupper():
        if temp in 'ABCDEFGHIJKLM':
            pos = string.ascii_uppercase.find(temp)
            new_pos = (pos + s1) % 26
            return string.ascii_uppercase[new_pos]
        else:
            shift = s2 * s2
            pos = string.ascii_uppercase.find(temp)
            new_pos = (pos - shift) % 26
            return string.ascii_uppercase[new_pos]
    return temp

# reads raw_text.txt and makes encrypted_text.txt
def do_encrypt(s1, s2):
    try:
        # use absolute path cuz relative didnt work
        script_dir = os.path.dirname(os.path.abspath(__file__))
        f = open(os.path.join(script_dir, 'raw_text.txt'), 'r')
        text = f.read()
        f.close()
        encrypted = ''
        for c in text:
            encrypted += encrypt_letter(c, s1, s2)  # encrypt each letter
        f = open(os.path.join(script_dir, 'encrypted_text.txt'), 'w')
        f.write(encrypted)
        f.close()
        print("Encryption Completed! Verifying encrypted_text.txt")
    except:
        print("Encryption failed!, check if raw_text.txt is there")

# reads encrypted_text.txt and makes decrypted_text.txt
def do_decrypt(s1, s2):
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        f = open(os.path.join(script_dir, 'encrypted_text.txt'), 'r')
        text = f.read()
        f.close()
        decrypted = ''
        for c in text:
            decrypted += decrypt_letter(c, s1, s2)
        f = open(os.path.join(script_dir, 'decrypted_text.txt'), 'w')
        f.write(decrypted)
        f.close()
        print("Decryption completed! Verifying decrypted_text.txt")
    except:
        print("Decryption failed! maybe encrypted_text.txt missing?")

# checks if decrypted file is same as original
def check_files():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        f1 = open(os.path.join(script_dir, 'raw_text.txt'), 'r')
        f2 = open(os.path.join(script_dir, 'decrypted_text.txt'), 'r')
        orig = f1.read()
        dec = f2.read()
        f1.close()
        f2.close()
        if orig == dec:
            print("Files match!!")
        else:
            print("Files are different!")
    except:
        print("cant check, file is missing!")

# main stuff
try:
    s1 = int(input("Please enter shift 1 number: "))
    s2 = int(input("Please enter shift 2 number: "))
    do_encrypt(s1, s2)  # do encrypt
    do_decrypt(s1, s2)  # do decrypt
    check_files()       # check files
except:
    print("please use numbers for shifts!!")