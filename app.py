from flask import Flask, flash, redirect, render_template, request, session, abort
from flask import request, jsonify, url_for
from firebase_admin import credentials, firestore, initialize_app
import os

# LINK TO LIVE: https://dungeon-flask-nvxsto2xda-uc.a.run.app
app = Flask(__name__)
app.secret_key = os.urandom(12)
cred = credentials.ApplicationDefault()
default_app = initialize_app(cred)
db = firestore.client()
user_ref = db.collection('users')

@app.route('/')
def mainPage():
    if not session.get('logged_in'):
        return render_template('index.html')

    return render_template('user_page.html')


@app.route('/login', methods=['POST'])
def login():
    username = user_ref.where('username', 
        '==', request.form["username"]).get()
    if not username:
        flash('invalid username')

    elif request.form["password"] == username[0].get("password"):
        session['user'] = request.form["username"]
        session['logged_in'] = True

    else:
        flash('Wrong password')

    return redirect('/')

@app.route('/logout')
def logout():
    session['logged_in'] = False
    session.clear()
    return redirect('/')

@app.route('/register', methods=['POST'])
def register():
    if user_ref.where('username', '==', request.form["username"]).get():
        flash('Username already in use!')
        return redirect('/registration')

    elif request.form["password"] != request.form["password2"]:
        flash('Passwords do not match!')
        return redirect('/registration')

    elif " " in request.form["username"]:
        flash('Invalid character " " in username!')
        return redirect('/registration')
    else:
        user_ref.add({"username": request.form["username"], "password": request.form["password"]})
        return redirect('/')


@app.route('/registration')
def reg_page():
    return render_template('register.html')

@app.route('/character-sheet')
def char_sheet():
    return render_template('character-sheet.html')
    
@app.route('/test-session')
def sessionData():
    if 'user' not in session:
        return "No user"
    return session['user']

port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    # Run app
    app.run(host="0.0.0.0", port=port, debug=True)