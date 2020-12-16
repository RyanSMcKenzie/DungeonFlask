from flask import Flask, flash, redirect, render_template, request, session, abort
from flask import request, jsonify, url_for
from firebase_admin import credentials, firestore, initialize_app
import os

app = Flask(__name__)
app.secret_key = os.urandom(12)
#cred = credentials.Certificate('DungeonDBKey.json')
#default_app = initialize_app(cred)
cred = credentials.ApplicationDefault()
default_app = initialize_app(cred)
db = firestore.client()
user_ref = db.collection('users')

@app.route('/')
def mainPage():
    if not session.get('logged_in'):
        return render_template('index.html')

    return f"Hi {session['user']}"


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
    return redirect('/')

port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    # Run app
    app.run(host="0.0.0.0", port=port)