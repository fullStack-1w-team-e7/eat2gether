
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://tibbetrabbit:galois1811@cluster0.5tpcr40.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

import hashlib

@app.route('/')
def home():
    return render_template('main.html')


@app.route("/api/postings", methods=["POST"])
def post():
    restaurant_receive = request.form['restaurant_give']
    message_receive = request.form['message_give']
    date_receive = request.form['date_give']
    time_receive = request.form['time_give']
    meetingPlace_receive = request.form['meetingPlace_give']
    payment_receive = request.form['payment_give']
    maxCount_receive = request.form['maxcount_give']
    count_receive = request.form['count_give']

    restaurant_db = db.restaurant_list.find_one(
        {'restaurant': restaurant_receive})
    address = restaurant_db['address']
    url = restaurant_db['link']
    img = restaurant_db['img']

    post_list = list(db.postings.find({}, {'_id': False}))
    post_id = len(post_list) + 1

    doc = {
        'post_id': post_id,
        'restaurant': restaurant_receive,
        'address': address,
        'url': url,
        'img': img,
        'message': message_receive,
        'date': date_receive,
        'time': time_receive,
        'meetingPlace': meetingPlace_receive,
        'payment': payment_receive,
        'maxCount': maxCount_receive,
        'count': [count_receive]
    }
    db.postings.insert_one(doc)

    return jsonify({'msg': '저장 완료!'})


@app.route("/api/postings", methods=["GET"])
def post_get():
    posting_list = list(db.postings.find({}, {'_id': False}))
    return jsonify({'postings': posting_list})


@app.route("/api/restaurant_list", methods=["GET"])
def rest_get():
    restaurant_list = list(db.restaurant_list.find({}, {'_id': False}))
    return jsonify({'restaurants': restaurant_list})


@app.route("/api/postings/add", methods=["POST"])
def add_count():

    post_id_receive = int(request.form['post_id_give'])
    print('post_id:', post_id_receive, type(post_id_receive))
    user_receive = request.form['count_give']
    post = db.postings.find_one(
        {'post_id': post_id_receive}, {'_id': False})
    participants = post['count']
    maxCount = int(post['maxCount'])

    # db에서 count 배열을 가져와 현재 참여하기를 누른 유저의 id 값이 있는지 확인 후, 없으면 배열에 추가하고, 있으면 "이미 참여하셨습니다." 메세지 전송

    if len(participants) < maxCount:
        for participant in participants:
            if user_receive != participant:
                db.postings.update_one({'post_id': post_id_receive}, {
                    '$push': {'count': user_receive}})
                print(db.postings.find_one(
                    {'post_id': post_id_receive}, {'_id': False})['count'])
                return jsonify({'msg': '참가 완료!'})
            else:
                return jsonify({'msg': '이미 같이 먹기로 하였습니다!'})
    else:
        return jsonify({'msg': '정원 초과이 초과되어 같이 먹을 수 없어요ㅠㅠ'})


#회원가입 api
@app.route('/api/register', methods=["POST"])
def info_post():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    doc = {
        'id': id_receive,
        'pw': pw_hash
        }
    db.info.insert_one(doc)

    return jsonify({'msg': '가입 완료!'})

#중복확인 api
@app.route('/api/register', methods=["GET"])
def double_check():
    info_list = list(db.info.find({}, {'_id': False}))
    return jsonify({'inf': info_list})


#회원가입 창 (커밋 잘되나)
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/detail_test')
def open_details():
    return render_template('detail_test.html')



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
