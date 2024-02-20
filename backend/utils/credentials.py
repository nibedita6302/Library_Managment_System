from bcrypt import hashpw, gensalt, checkpw
import re

def hash_password(plain_pw):
    salt = gensalt()
    return hashpw(plain_pw.encode('utf-8'),salt)

def check_password(plain_pw, hash_pw):
    return checkpw(plain_pw.encode('utf-8'),hash_pw)

def validate_email(email):
    if email.count('@')==1:
        front, back = email.split('@')
        front_pattern = re.compile(r'^[a-zA-Z0-9]+(?:[._][a-zA-Z0-9]+)*$')
        back_pattern = re.compile(r'^[a-zA-Z0-9]+[.][a-zA-Z]+$')
        # Explaination
        # Alpha numeric (1 or more) followed by '.' or '_' which is immediately
        # followed by Alpha numeric characters (1 or more)
        # No 2 special char occur together.
        if re.match(front_pattern, front) and re.match(back_pattern, back):
            return True
    return False

def validate_password(password):
    pattern = re.compile(r'^(?=.*[a-z])(?=.*[0-9])(?=.*[A-Z])(?=.*[^a-zA-Z0-9]).{8,}$')
    # Explanation 
    # (?=.*[a-z]) - atleast one lowercase letter
    # (?=.*[A-Z]) - atleast one uppercase letter
    # (?=.*\d) - atleast one digit
    # (?=.*[^a-zA-Z0-9]) - atleast one special character (not alphanumeric)
    # .{8,} - atleast 8 characters long
    return re.match(pattern, password) is not None


# Testing
# print(validate_email('hello1.2@hello.com'))
# print( validate_password('hello12@A') )