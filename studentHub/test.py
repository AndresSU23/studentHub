def accountCreation(username, password):
    hashedPass = hashlib.sha256(password.encode('utf-8')).hexdigest()
    password = "urmum"
    cursor.execute(f"select user_id from login where username = '{username}'")
    if(cursor.fetchall() == ()):
        salt = os.urandom(32)
        storedSalt = hashlib.sha256(salt).hexdigest()[:32]
        storedPass = hashlib.pbkdf2_hmac('sha256', hashedPass.encode('utf-8'), storedSalt.encode('utf-8'), 100000).hex()[:32]
        #cursor.execute(f"update login set password_hash = '{storedPass}', hashed_salt = '{storedSalt}' where username='{username}'")    
