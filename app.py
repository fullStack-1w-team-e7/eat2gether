import certifi as certifi
from flask import Flask, render_template, jsonify, request, session, redirect, url_for

app = Flask(__name__)

ca = certifi.where()
import certifi
from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.kmqoshg.mongodb.net/?retryWrites=true&w=majority',
                     tlsCAFile=ca)
db = client.project7

SECRETE_KEY = 'SPARTA'

import hashlib


# 로그인 API
# id, pw를 받아 맞춰보고, 토큰을 만들어 발급한다.

@app.route("/api/login/", methods=["POST"])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    doc = {
        'id': id_receive,
        'pw': pw_receive,
    }
    db.login.insert_one(doc)
    return jsonify({'msg': '로그인 완료!'})

    # pw를 암호화한다.
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    result = db.user.find_one({'id': id_receive, 'pw': pw_hash})
    print(result)



if __name__ == '__main__':
    app.run('0.0.0.0', port=12000, debug=True)
