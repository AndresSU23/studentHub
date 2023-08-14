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
def infoMenu(username):
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
                                               extra="He has a peanut allergy")
    else:
        return f"<html><body> <h1>You are not logged in <br><a href = '/login'>click here to log in</a></h1></body></html>" 


@app.route('/logout', methods = ["GET", "POST"]) 
def logout(username):
    del dbu.userLogins[username]
    return redirect(url_for('login'))

if __name__=='__main__':
   app.run(debug=True)