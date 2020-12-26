from flask import Flask, flash, redirect, render_template, request, session, abort
from flask import request, jsonify, url_for
from firebase_admin import credentials, firestore, initialize_app
from static.py.login_req import login_required
import os

# LINK TO LIVE: https://dungeon-flask-nvxsto2xda-uc.a.run.app
app = Flask(__name__)
app.secret_key = os.urandom(12)
cred = credentials.ApplicationDefault()
default_app = initialize_app(cred)
db = firestore.client()
user_ref = db.collection('users')
sheet_ref = db.collection('Sheet')

@app.route('/')
def mainPage():
    if not session.get('logged_in'):
        return render_template('index.html')

    sheets = sheet_ref.where("userID", "==", session['userID']).stream()
    sheets = [(sheet.id, sheet.get('char_name')) if sheet.get('char_name') != "" else (sheet.id, "**Unnamed**") for sheet in sheets]
    data = {"user_sheets": sheets}
    return render_template('user_page.html', data=data)


@app.route('/login', methods=['POST'])
def login():
    username = user_ref.where('username', 
        '==', request.form["username"]).get()
    if not username:
        flash('invalid username')

    elif request.form["password"] == username[0].get("password"):
        session['user'] = request.form["username"]
        session['logged_in'] = True
        session['userID'] = user_ref.where("username", "==", session['user']).get()[0].id

    else:
        flash('Wrong password')

    return redirect('/')

@app.route('/logout')
@login_required
def logout():
    session['logged_in'] = False
    session.clear()
    return redirect('/')

@app.route('/register', methods=['POST'])
def register():
    if request.form.get("bots"):
        return redirect('/')
        
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

@app.route('/new-character')
@login_required
def new_char():
    new_sheet = sheet_ref.document()
    template = sheet_ref.document(u'9JxW3AAKWMaUoSrWAHeI').get().to_dict()
    data = template
    data["sheetID"] = new_sheet.get().id
    
    return render_template('character-sheet.html', data=data)

@app.route('/character-sheet', methods=['POST'])
@login_required
def char_sheet():
    data = sheet_ref.document(request.form["sheetID"]).get().to_dict()
    data["sheetID"] = sheet_ref.document(request.form["sheetID"]).get().id
    return render_template('character-sheet.html', data=data)

@app.route('/save-character', methods=['POST'])
@login_required
def char_save():
    current_user_id = session['userID']

    data = request.form.to_dict()
    
    data['userID'] = current_user_id
    if 'equips' not in data:
        data['equipment'] = ""
    else:
        data['equipment'] = data['equips']
        del data['equips']
    sheet_ID = data["sheetID"]
    del data["sheetID"]
    sheet_ref.document(sheet_ID).set(data)
    data["sheetID"] = sheet_ID
    return render_template('/character-sheet.html', data=data)

@app.route('/delete-character', methods=['POST'])
@login_required
def delChar():
    to_del = sheet_ref.document(request.form["sheet"]).delete()
    return redirect('/')
    
@app.route('/test-session')
def sessionData():
    if 'user' not in session:
        return ("No user")
    return (session['user'])

@app.route('/test-login-requirement')
@login_required
def testLogReq():
    return "Logged in"

port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    # Run app
    app.run(host="0.0.0.0", port=port, debug=True)