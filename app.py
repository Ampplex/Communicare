from flask import Flask, render_template, request, redirect
from flask_mail import Mail, Message
import pyrebase
import pyttsx3
import threading
from datetime import date
import requests
from datetime import datetime
from random import randint
import json

config = {
  "apiKey": "AIzaSyA4BBE51ZH3f-VKdapqUOY2F-QgwTlZIcY",
  "authDomain": "communicare-45870.firebaseapp.com",
  "databaseURL": "https://communicare-45870-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "communicare-45870",
  "storageBucket": "communicare-45870.appspot.com",
  "messagingSenderId": "73972180735",
  "appId": "1:73972180735:web:6d5ea9d2c209fbd3470eca",
  "measurementId": "G-0GZSL9LQK0"
};

firebase = pyrebase.initialize_app(config)
database = firebase.database()
storage = firebase.storage()

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'team.amplex@gmail.com'
app.config['MAIL_PASSWORD'] = 'iyfmqibihwffqvjn'
mail = Mail(app)

def Server_Assistant(audio):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(audio)
    engine.runAndWait()


def Cryptography_Encrypt(text):
    alpha = {'a': 2073, 'b': 2076, 'c': 2079, 'd': 2082, 'e': 2085, 'f': 2088,
             'g': 2091, 'h': 2094, 'i': 2097, 'j': 2100, 'k': 2103, 'l': 2106, 'm': 2109, 'n': 2112, 'o': 2115, 'p': 2118, 'q': 2121, 'r': 2124, 's': 2127, 't': 2130, 'u': 2133, 'v': 2136, 'w': 2139, 'x': 2142, 'y': 2145, 'z': 2148, ' ': 2151,
             '1': 234, '2': 89, '3': 45, '4': 1095,
             '5': 77, '6': 12, '7': 61, '8': 55, '9': 23, '0': 22,
             '`': 1288, '~`': 226096, '!': 33, '@': 44, '#': 59, '$': 66, '%': 7754, '^': 88, '&': 99, '*': 401, '(': 402, ')': 403, '-': 404, '_': '405', '=': 406, '+': 407, '[': 408, ']': 409, '{': 410, '}': 411, '\\': 412, '|': 413, ';': 414, ':': 415, "'": 416, '"': 417, ',': 418, '.': 419, '/': 420, '?': 422, 'A': 630, 'B': 632, 'C': 634, 'D': 636, 'E': '638', 'F': 640, 'G': 642, 'H': 644, 'I': 646, 'J': 648, 'K': 650, 'L': 652, 'M': 654, 'N': 656, 'O': 658, 'P': 660, 'Q': 662, 'R': 664, 'S': 666, 'T': 668, 'U': 670, 'V': 672, 'W': 674, 'X': 676, 'Y': 678, 'Z': 680}

    encryptedTxt = ""

    for i in text:
        encryptedTxt += ' '
        encryptedTxt += str(alpha[i])

    return encryptedTxt


def Cryptography_Decrypt(encryptedTxt):

    alpha_num = {'2073': 'a', '2076': 'b', '2079': 'c',
                 '2082': 'd', '2085': 'e', '2088': 'f', '2091': 'g', '2094': 'h', '2097': 'i', '2100': 'j', '2103': 'k', '2106': 'l', '2109': 'm', '2112': 'n', '2115': 'o', '2118': 'p', '2121': 'q', '2124': 'r', '2127': 's', '2130': 't', '2133': 'u', '2136': 'v', '2139': 'w', '2142': 'x', '2145': 'y', '2148': 'z', '2151': ' ', '234': '1', '89': '2', '45': '3',
                 '1095': '4', '77': '5', '12': '6', '61': '7', '55': '8', '23': '9', '22': '0', '1288': '`', '226096': '~', '33': '!', '44': '@', '59': '#', '66': '$', '7754': '%', '88': '^', '99': '&', '401': '*', '402': '(', '403': ')', '404': '-', '405': '_', '406': '=', '407': '+', '408': '[', '409': ']', '410': '{', '411': '}', '412': '\\', '413': '|', '414': ';', '415': ':', '416': "'", '417': '"', '418': ',', '419': '.', '420': '/', '422': '?', '630': 'A', '632': 'B', '634': 'C', '636': 'D', '638': 'E', '640': 'F', '642': 'G', '644': 'H', '646': 'I', '648': 'J', '650': 'K', '652': 'L', '654': 'M', '656': 'N', '658': 'O', '660': 'P', '662': 'Q', '664': 'R', '666': 'S', '668': 'T', '670': 'U', '672': 'V', '674': 'W', '676': 'X', '678': 'Y', '680': 'Z'}

    decryptedTxt = ""

    encryptedLst = encryptedTxt.split()

    for i in encryptedLst:
        decryptedTxt += alpha_num[i]

    return decryptedTxt


@app.route('/')
@app.route('/home')
def Home():
    return "Hello World!"

@app.route('/Login/<string:email>/<string:password>', methods=['GET'])
def Login(email, password):

    # if request.url == f"http://ampplex-backened.herokuapp.com/Login/<string:email>/<string:password>":
    #     return redirect("https://ampplex-backened.herokuapp.com/Login/<string:email>/<string:password>")

    try:

        db_val = database.child("User").get().val()

        password = Cryptography_Decrypt(password)

        for i in db_val:
            if db_val[i]["Email"] == email and Cryptography_Decrypt(db_val[i]["password"]) == password:
                # If user's email and password is correct then returning the status success and user id
                response = {
                    "status": "success",
                    "user_id": i,
                    "UserName": db_val[i]["UserName"]
                }
                return json.dumps(response)
    except:
        # If user's email or password is incorrect then returning the response error
        response = {
            "status": "error",
        }
    return json.dumps(response)

@app.route('/SignUp/<string:username>/<string:email>/<string:password>', methods=['GET'])
def SignUp(username, email, password):
    # if request.url == "http://ampplex-backened.herokuapp.com/SignUp/<string:username>/<string:email>/<string:password>":
    #     return redirect('https://ampplex-backened.herokuapp.com/SignUp/<string:username>/<string:email>/<string:password>')

    password_len = password.split(' ')

    if len(password_len) >= 8:

        data = {"UserName": username, "Email": email,
                "password": password, "Follower": 0, "Bio": ""}
        database.child("User").push(data)

        # msg = Message("Congratulations! you have successfully became a part of Ampplex family",
        #               sender="team.amplex@gmail.com", recipients=[email])
        # msg.body = f"Hi, {username} Thanks for downloading our app. We would love to hear your feedback! \n https://play.google.com/store/apps/details?id=com.ankeshkumar.Ampplex"
        # mail.send(msg)

        return "success"

    else:
        return "error"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4567)