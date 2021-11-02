from flask import Flask, jsonify, request
from flask_cors import CORS

from database import init_db, db_session, engine, User, Song, Quote, SongUser, QuoteUser
import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

BOOKS = [
    {
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'read': True
    },
    {
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J. K. Rowling',
        'read': False
    },
    {
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'read': True
    }
]

init_db()

eng = sqlalchemy.create_engine('sqlite:///test.db', convert_unicode=True)
Session = scoped_session(sessionmaker(bind=engine))
s = Session()

@app.route('/api/users/add', methods=['POST'])
def add_user():
    post_data = request.get_json()
    to_add = User(post_data.get('username'), post_data.get('password'), post_data.get('happiness'), post_data.get('happiness'), 1)
    db_session.add(to_add)
    db_session.commit()
    #con.execute('insert into user(username, password, happiness, total_happiness, account_age) values(%s, %s, %d, %d, %d)' % (post_data.get('username'), post_data.get('password'), post_data.get('happiness'), post_data.get('happiness'), 1))
    print('added user %s' % (post_data.get('username')))
    return jsonify({
        'status': 'success'
    })

@app.route('/api/users', methods=['GET'])
def get_users():
    rs = s.execute('select * from users')
    arr = []
    for row in rs:
        print(row)
        d = dict(row.items())
        average = 0
        avg_happiness_rs = s.execute('select avg(happiness) from users')
        for elem in avg_happiness_rs:
            average = elem[0]
            print(elem[0])
        d['total_avg'] = average
        d['average_happiness'] = d['total_happiness'] // d['account_age']
        arr.append(d)
    return jsonify({
        'status': 'success',
        'users': arr
    })

@app.route('/api/users/delete', methods=['POST'])
def delete_user():
    payload = request.get_json()
    target_user = payload.get('username')
    db_session.query(User).filter(User.username==target_user).delete()
    db_session.commit()
    return jsonify({
        'status': 'success'
    })

@app.route('/api/users/update', methods=['POST'])
def update_user():
    payload = request.get_json()
    target_user = payload.get('username')
    rs = s.execute('select account_age from users where username="%s"' % (target_user))
    age = 1
    for row in rs:
        age = int(row[0])
    print('update user')
    db_session.query(User).filter(User.username==target_user).update({"password": payload.get('password'), 'happiness': payload.get('happiness'), 'total_happiness': (payload.get('happiness') * age)})
    db_session.commit()
    return jsonify({
        'status': 'success'
    })


@app.route('/api/songs', methods=['GET'])
def get_songs():
    rs = s.execute('select * from songs')
    arr = []
    for row in rs:
        d = dict(row.items())
        arr.append(d)
    return jsonify({
        'status': 'success',
        'songs': arr
    })

@app.route('/api/songs/add', methods=['POST'])
def add_song():
    post_data = request.get_json()
    to_add = Song(post_data.get('name'), post_data.get('artist'), post_data.get('length'), post_data.get('genre'), 0, post_data.get('happiness'))
    db_session.add(to_add)
    db_session.commit()
    print('added song %s' % (post_data.get('name')))
    return jsonify({
        'status': 'success'
    })

@app.route('/api/songs/delete', methods=['POST'])
def delete_song():
    payload = get_json()
    target_song_name = payload.get('name')
    target_song_artist = payload.get('artist')
    db_session.query(Song).filter(Song.name==target_song_name).filter(Song.artist==target_song_artist).delete()
    db_session.commit()
    return jsonify({
        'status': 'success'
    })

@app.route('/api/songs/update', methods=['POST'])
def update_song():
    payload = request.get_json()
    target_song_name = payload.get('name')
    target_song_artist = payload.get('artist')
    print('update song')
    db_session.query(Song).filter(Song.name==target_song_name).filter(Song.artist==target_song_artist).update({"length": payload.get('length'), 'genre': payload.get('genre'), 'happiness': payload.get('happiness'), 'num_assigned': payload.get('num_assigned')})
    db_session.commit()
    return jsonify({
        'status': 'success'
    })

@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        BOOKS.append({
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book added!'
    else:
        response_object['books'] = BOOKS
    return jsonify(response_object)

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


if __name__ == '__main__':
    app.run()
