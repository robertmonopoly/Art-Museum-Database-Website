import bcrypt

def hash_pw(password):
    # encoding user password
    bytes = password.encode('utf-8')
    # generating the salt
    salt = bcrypt.gensalt()
    # Hashing the password
    hash = bcrypt.hashpw(bytes, salt)
    print(hash)
    userBytes = password.encode('utf-8')
    # checking password (boolean)
    result = bcrypt.checkpw(userBytes, hash)
    # print(result)
    return result