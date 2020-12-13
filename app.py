from flask import Flask

app = Flask(__name__)

@app.route('/')
def mainPage():
    return "Hi there person"

if __name__ == '__main__':
    # Run app
    app.run(host="0.0.0.0", port=5500)