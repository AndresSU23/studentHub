import hashlib

password = "test101"

hashedpassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
print(hashedpassword)