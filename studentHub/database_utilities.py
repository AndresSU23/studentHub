from dotenv import load_dotenv
load_dotenv()
import os
import certifi
import pymysql.cursors
import hashlib
from users import Student

'''
username: shrey
password: test101
'''

connection = pymysql.connect(host=os.getenv("PLANETSCALE_HOST"),
                             user=os.getenv("PLANETSCALE_USERNAME"),
                             password=os.getenv("PLANETSCALE_PASSWORD"),
                             database=os.getenv("PLANETSCALE_DATABASE"),
                             cursorclass=pymysql.cursors.DictCursor,

                             autocommit = True,
                             ssl_verify_identity = True,
                             ssl      = {
                             "ca": certifi.where()
                             })
cursor = connection.cursor()

userLogins = {}

def loginVerification(username, password):
    cursor.execute(f"select user_id from login where username = '{username}'")

    if(cursor.fetchall() != ()):
        hashedPass = hashlib.sha256(password.encode('utf-8')).hexdigest()
        password = "urmom"
        if passwordVerification(username, hashedPass):
            print("Invalid Password")
            return ['E','']
        
        print("Password Authenticated!")
        cursor.execute(f"select user_type, first_name from users where user_id = (select user_id from login where username = '{username}')")
        userType = cursor.fetchall()
        

        studentCreation(username)
        return [userType[0]["user_type"], userType[0]["first_name"]]

    else:
        return ['E','']

def passwordVerification(username, hashedPass):
    cursor.execute(f"select password_hash, hashed_salt from login where username = '{username}'")
    usrData = cursor.fetchall()
    storedPass, storedSalt = usrData[0]["password_hash"], usrData[0]["hashed_salt"]
    print("storedPass: ", storedPass)
    print("storedSalt", storedSalt)
    givenPass = hashlib.pbkdf2_hmac('sha256', hashedPass.encode('utf-8'), storedSalt.encode('utf-8'), 100000).hex()[:32]
    print("givenPass", givenPass)
    if(storedPass != givenPass):
        return 1
    else:
        return 0
    
def updatePassword(username, password):
    hashedPass = hashlib.sha256(password.encode('utf-8')).hexdigest()
    password = "urmum"
    salt = os.urandom(32)
    storedSalt = hashlib.sha256(salt).hexdigest()[:32]
    storedPass = hashlib.pbkdf2_hmac('sha256', hashedPass.encode('utf-8'), storedSalt.encode('utf-8'), 100000).hex()[:32]
    print("hashedpass: ", hashedPass)
    print("pass: ", storedPass)
    print("salt: ", storedSalt)
    cursor.execute(f"update login set password_hash = '{storedPass}', hashed_salt = '{storedSalt}' where username='{username}'") 

def studentCreation(username):
    cursor.execute(f'''select login.user_id, student_id, user_type, username, first_name, class, 
                   section from login, users, students where login.user_id=users.user_id and 
                   login.user_id=students.user_id and login.username = "{username}"''')
    userData = cursor.fetchall()
    student = Student(userData[0])
    userLogins[userData[0]['username']] = student


if __name__ == '__main__':
    pass
    #updatePassword("shrey","test111")
    #loginVerification("shrey", "asdfh")


    