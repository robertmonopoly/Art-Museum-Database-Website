import bcrypt

def hash_pw(password):
    # encoding user password
    bytes = password.encode('utf-8')
    # generating the salt
    salt = bcrypt.gensalt()
    # Hashing the password
    hash = bcrypt.hashpw(bytes, salt)
    print(hash)
    # print(result)
    return hash

def isValidPw(in_password,hash):
    db_pw_byte = hash[0].encode('utf-8')
   # print(hash[0], " pw")
    userBytes = in_password.encode('utf-8')
    # checking password (boolean)
    result = bcrypt.checkpw(userBytes, db_pw_byte)
    print("passed!")
    return result

# print("first admin: ",hash_pw("admin"), isValidPw("admin", hash_pw("admin")))
# print("first user: ", hash_pw("user"))
# print("second user pw: ",hash_pw("user1"))
# print("third user pw: ", hash_pw("user2"))
