from dotenv import load_dotenv
load_dotenv()
import os
import certifi
import pymysql.cursors
from users import Student

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
    cursor.execute(f"select user_type, first_name from users where user_id = (select user_id from login where username = '{username}')")
    userType = cursor.fetchall()
    
    try:
        studentCreation(username)
        return [userType[0]["user_type"], userType[0]["first_name"]]
    except(IndexError):
        return ['E','']


def studentCreation(username):
    cursor.execute(f'''select login.user_id, student_id, user_type, username, first_name, class, 
                   section from login, users, students where login.user_id=users.user_id and 
                   login.user_id=students.user_id and login.username = "{username}"''')
    userData = cursor.fetchall()
    student = Student(userData[0])
    userLogins[userData[0]['username']] = student

def getStudent(username):
    return userLogins[username]

def getUserFullNameByUsername(username):
    return "Michael"

if __name__ == '__main__':
    loginVerification("shrey", "asdfh")


    