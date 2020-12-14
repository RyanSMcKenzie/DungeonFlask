from flask import Flask
from flask import request, jsonify
from firebase_admin import credentials, firestore, initialize_app

app = Flask(__name__)

cred = credentials.Certificate('DungeonDBKey.json')
default_app = initialize_app(cred)
db = firestore.client()
user_ref = db.collection('users')

@app.route('/')
def mainPage():
    return user_ref.where('username', '==', 'admin').get()[0].to_dict()

if __name__ == '__main__':
    # Run app
    app.run(host="0.0.0.0", port=5500, debug=True)