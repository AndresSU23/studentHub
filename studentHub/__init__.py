from flask import Flask, render_template, redirect, request, url_for, session
import database_utilities as dbu
app = Flask(__name__)  

@app.route('/', methods =["GET", "POST"])
def home():
    return redirect(url_for('login'))

@app.route('/login', methods =["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
       username = request.form.get("username")
       password = request.form.get("password")
       if (username==None or password==None or username=='' or password==''):
           error = 'Invalid Input, Try Again'
       else:
           match (dbu.loginVerification(username, password)):
               case 0:
                   return redirect(url_for('studentHome', username=username))
               case -1:
                   error = 'Invalid Credentials, Try Again'
    return render_template("login.html",error = error)
 
@app.route('/studentHome/<username>', methods = ["GET", "POST"]) 
def studentHome(username):
    name = dbu.getUserFullNameByUsername(username=username)
    return render_template("studentHome.html",username=username, name=name)

@app.route('/studentHome/<username>/classesMenu', methods = ["GET", "POST"]) 
def classesMenu(username):
    return f"<html><body> <h1>Classes Menu from student {username}</h1></body></html>"

@app.route('/studentHome/<username>/gradesMenu', methods = ["GET", "POST"]) 
def gradesMenu(username):
    return f"<html><body> <h1>Grades Menu from student {username}</h1></body></html>"

@app.route('/studentHome/<username>/infoMenu', methods = ["GET", "POST"]) 
def infoMenu(username):
    return f"<html><body> <h1>Info Menu from student {username}</h1></body></html>"
if __name__=='__main__':
   app.run()