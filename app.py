import certifi
import hashlib
import datetime
import jwt
import os
from dotenv import dotenv_values
from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
app = Flask(__name__)
ca = certifi.where()


config = dotenv_values('.env')
atlas_url = config['MONGODB_CLIENT']

client = MongoClient(atlas_url, tlsCAFile=ca)
db = client.project7

SECRET_KEY = config['SECRET_KEY']


#################################
## HTML 렌더링                 ##
#################################
@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    print(token_receive)

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.info.find_one({"id": payload['id']})
        return render_template('main.html', user_id=user_info["id"])
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


@app.route('/register')
def register():
    return render_template('register.html')


# 메인페이지에서 게시물 클릭 시 상세페이지로 이동
@app.get('/api/postings-detail/<int:post_id>')
def post_info(post_id):
    page_info = db.postings.find_one({'post_id': post_id}, {'_id': False})
    print(page_info)
    return render_template('detail.html', page=page_info)


#################################
##  로그인을 위한 API            ##
#################################

# [로그인 API]
# id, pw를 받아서 맞춰보고, 토큰을 만들어 발급합니다.
@app.route("/api/login", methods=["POST"])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    # 비밀번호를 암호화
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    result = db.info.find_one({'id': id_receive, 'pw': pw_hash})

    if result is not None:

        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        # 로그인이 얼마나 유지되는가

        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


#################################
##      회원가입 페이지 API     ##
#################################

# 회원가입 DB로 저(장)   여기에도 연습합니다
# 회원가입 DB로 저(장)   여기에도 연습합니다
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


#################################
##      메인 페이지 API        ##
#################################

# main 페이지 렌더링시 포스팅 정보 받아가는 API
@app.route("/api/postings", methods=["GET"])
def post_get():
    posting_list = list(db.postings.find({}, {'_id': False}))
    return jsonify({'postings': posting_list})


# 포스팅 할 때 고른 식당 정보를 가져오기 -> api/postings에 해당 데이터 활용
@app.route("/api/restaurant_list", methods=["GET"])
def rest_get():
    restaurant_list = list(db.restaurant_list.find({}, {'_id': False}))
    return jsonify({'restaurants': restaurant_list})


# 포스팅 내용 저장 API
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


# 메인 페이지에서 게시물 안에 "같이 먹기" 버튼 클릭했을 때, 참여자 명단 추가하기
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

    if len(participants) >= maxCount:
        return jsonify({'msg': '정원 초과이 초과되어 같이 먹을 수 없어요ㅠㅠ'})
    elif len(participants) < maxCount and user_receive not in participants:
        db.postings.update_one({'post_id': post_id_receive}, {
            '$push': {'count': user_receive}})
        print(db.postings.find_one(
            {'post_id': post_id_receive}, {'_id': False})['count'])
        return jsonify({'msg': '참가 완료!'})
    else:
        return jsonify({'msg': '이미 같이 먹기로 하였습니다!'})


#################################
##      상세 페이지 API        ##
#################################

# 상세 페이지 이동 관련

# 상세 페이지에서 식사 원정대 참여
# path variable 수정 완료
@app.post('/api/add/<int:post_id>')
def counting(post_id):
    page_info = db.postings.find_one({'post_id': post_id}, {'_id': False})

    params = request.get_json()
    member = params['give_user']
    print(member)

    participant_list = page_info['count']
    maxCount = int(page_info['maxCount'])

    # 배열에 member가 있다면 return
    for participant in participant_list:
        if participant == member:
            print(post_id, member)
            return jsonify({'result': 'fail', 'msg': '이미 식사에 참여하셨습니다'})

    # 없다면 배열에 member 추가 후 db업데이트
    if len(participant_list) < maxCount:
        participant_list.append(member)
        db.postings.update_one({'post_id': post_id}, {
                               '$set': {'count': participant_list}})
        print(page_info)
        return jsonify({'result': 'success', 'msg': '식사에 참여되었습니다.'})

    # 모든 if문에 안걸리면 정원초과과
    return jsonify({'result': 'fail', 'msg': '정원초과입니다.'})


# 식사 원정대 참여 취소
@app.post('/api/delete-comment/<int:post_id>')
def delete_comment(post_id):
    page_info = db.postings.find_one({'post_id': post_id}, {'_id': False})

    print('delete-comment')

    params = request.get_json()
    member = params['give_user']

    participant_list = page_info['count']
    print(participant_list)

    if member in participant_list:
        participant_list.remove(member)
        db.postings.update_one({'post_id': post_id}, {
                               '$set': {'count': participant_list}})

        return jsonify({'result': 'success', 'msg': '참여를 취소하셨습니다'})
    else:
        print('여기 오류남')
        return jsonify({'result': 'fail', 'msg': '식사에 참여하지 않은 상태입니다.'})


# 게시물 삭제
# member - jisoo로 고정
# path variable 수정 완료
@app.post('/api/delete-post/<int:post_id>')
def delete_post(post_id):
    params = request.get_json()
    member = params['give_user']

    page_info = db.postings.find_one({'post_id': post_id}, {'_id': False})

    participant_list = page_info['count']

    # 배열 0번째 인덱스 작성자와 member가 같다면 삭제, 아니면 삭제불가
    if participant_list[0] == member:
        db.postings.delete_one({'post_id': post_id})
        return jsonify({'result': 'success', 'msg': '삭제에 성공하셨습니다'})
    else:
        return jsonify({'result': 'fail', 'msg': '삭제권한이 없습니다'})


# 회원 유효성 검사
# 로그인 예제 파일 그대로 사용
# 토큰 인증시 회원 아이디만 반환하는 역할
@app.get('/api/validate')
def api_validate():
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)

        userinfo = db.info.find_one({'id': payload['id']}, {'_id': 0})
        return jsonify({'result': 'success', 'id': userinfo['id']})
    except jwt.ExpiredSignatureError:
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})


# 여기까지
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
