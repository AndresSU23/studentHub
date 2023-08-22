from flask import Flask, render_template, redirect, request, url_for, session

import database_utilities as dbu
app = Flask(__name__)  


@app.route('/', methods =["GET", "POST"])
def home():
    return redirect(url_for('login'))

@app.route('/login', methods =["GET", "POST"])
def login():
    global username
    error = None
    if request.method == "POST":
       username = request.form.get("username")
       password = request.form.get("password")
       if (username==None or password==None or username=='' or password==''):
           error = 'Invalid Input, Try Again'
       else:
           user_type, first_name = dbu.loginVerification(username, password)  #user_type, first_name
           match (user_type):
               case 'S':
                   print(dbu.userLogins[username].user_type)
                   return redirect(url_for('studentHome', username=username))
               case 'E':
                   error = 'Invalid Credentials, Try Again'
    return render_template("login.html",error = error)
 
@app.route('/studentHome/<username>', methods = ["GET", "POST"]) 
def studentHome(username):
    if username in dbu.userLogins:
        name = dbu.userLogins[username].first_name
        return render_template("studentHome.html",username=username, name=name)
    else:
        return f"<html><body> <h1>You are not logged in <br><a href = '/login'>click here to log in</a></h1></body></html>" 

@app.route('/studentHome/<username>/classesMenu', methods = ["GET", "POST"]) 
def classesMenu(username):
    return f"<html><body> <h1>Classes Menu from student {username}</h1></body></html>"

@app.route('/studentHome/<username>/gradesMenu', methods = ["GET", "POST"]) 
def gradesMenu(username):
    return f"<html><body> <h1>Grades Menu from student {username}</h1></body></html>"

@app.route('/studentHome/<username>/infoMenu', methods = ["GET", "POST"]) 
def infoMenu(username, error = None):
    if username in dbu.userLogins:
        test = request.form.get("extra")
        print(test)
        return render_template("userInfo.html",username=username, 
                                               firstName=dbu.userLogins[username].first_name,
                                               middleName="ANdres",
                                               lastName="Hu Nous",
                                               birthDate="02/18/20030",
                                               bloodType="-A",
                                               email="sanchez@gmail.com",
                                               number="3264 684 565",
                                               address="Cra70 no 22 75",
                                               extra="He has a peanut allergy",
                                               error = error)
    else:
        return f"<html><body> <h1>You are not logged in <br><a href = '/login'>click here to log in</a></h1></body></html>" 


@app.route('/logout', methods = ["GET", "POST"]) 
def logout(username):
    del dbu.userLogins[username]
    return redirect(url_for('login'))

@app.route('/loadNameInfo', methods = ["GET", "POST"]) 
def loadNameInfo(username, firstName, middleName, lastName):
    error = dbu.dataNameValidation(firstName, middleName, lastName)
    if (error == None):
        dbu.userLogins[username]['first_name'] = firstName
        #Repeat with middleName
        #Repeat with LastName
        dbu.updateUserFirstName(username, firstName)
        dbu.updateUserMiddleName(username, middleName)
        dbu.updateUserLastName(username, lastName)
    return redirect(url_for('/studentHome/<username>/infoMenu', username=username, error = error))
    
@app.route('/loadEmailInfo', methods = ["GET", "POST"]) 
def loadEmailInfo(username, email):
    error = dbu.dataEmailValidation(email)
    if (error == None):
        #Alter the Email value in login user with username
        dbu.updateUserEmail(username, email)
    return redirect(url_for('/studentHome/<username>/infoMenu', username=username, error = error))

@app.route('/loadNumberInfo', methods = ["GET", "POST"]) 
def loadNumberInfo(username, number):
    error = dbu.dataNumberValidation(number)
    if (error == None):
        #Alter the number value in login user with username
        dbu.updateUserNumber(username, number)
    return redirect(url_for('/studentHome/<username>/infoMenu', username=username, error = error))

@app.route('/loadAddressInfo', methods = ["GET", "POST"]) 
def loadAddressInfo(username, address):
    error = dbu.dataAddressValidation(address)
    if (error == None):
        #Alter the address value in login user with username
        dbu.updateUserAddress(username, address)
    return redirect(url_for('/studentHome/<username>/infoMenu', username=username, error = error))

@app.route('/loadExtraInfo', methods = ["GET", "POST"]) 
def loadExtraInfo(username, extra):
    error = dbu.dataExtraValidation(extra)
    if (error == None):
        #Alter the extra value in login user with username
        dbu.updateUserExtraInfo(username, extra)
    return redirect(url_for('/studentHome/<username>/infoMenu', username=username, error = error))

if __name__=='__main__':
   app.run(debug=True)