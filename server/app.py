from flask import Flask, jsonify, request
from flask_cors import CORS

from database import init_db, db_session, engine, User, Song, Quote, SongUser, QuoteUser
import sqlalchemy
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import date as dtdate

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

eng = sqlalchemy.create_engine('sqlite:///test.db', convert_unicode=True, isolation_level='REPEATABLE READ')
Session = scoped_session(sessionmaker(bind=engine))
s = Session()

#########################################################
##                      Users                          ##
#########################################################

@app.route('/api/users/add', methods=['POST'])
def add_user():
    post_data = request.get_json()
    to_add = User(post_data.get('username'), post_data.get('password'), post_data.get('happiness'), post_data.get('happiness'), 1)
    db_session.add(to_add)
    
    #get a song

    rs = s.execute('select * from songs where happiness >= :happiness', {'happiness': post_data.get('happiness')}).fetchone()
    uid = to_add.user_id
    sid = rs[0]
    num_assigned = rs[5]
    db_session.query(Song).filter(Song.song_id==sid).update({'num_assigned': num_assigned + 1})
    to_add_junction = SongUser(uid, sid)
    print('assigning user %s song: %d' % (post_data.get('username'), sid))
    db_session.add(to_add_junction)

    #get a quote
    rs = s.execute('select * from quote where happiness >= :happiness', {'happiness': post_data.get('happiness')}).fetchone()
    uid = to_add.user_id
    qid = rs[0]
    num_assigned = rs[4]
    db_session.query(Quote).filter(Quote.quote_id==qid).update({'num_assigned': num_assigned + 1})
    to_add_junction = QuoteUser(uid, qid)
    print('assigning user %s quote: %d' % (post_data.get('username'), qid))
    db_session.add(to_add_junction)

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

#########################################################
##                      Songs                          ##
#########################################################

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
    payload = request.get_json()
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

@app.route('/api/songuser', methods=['POST'])
def get_songusers():
    payload = request.get_json()
    # get song id from name
    rs = s.execute('select song_id from songs where name = :name', {'name': payload.get('name')}).fetchone()
    sid = rs[0]

    # get all user id's with this song id
    rs = s.execute('select u.username, u.happiness from users u where u.user_id in (select us.user_id from usersong us where us.song_id = :song_id)', {'song_id': sid})
    arr = []
    for row in rs:
        d = dict(row.items())
        arr.append(d)
    return jsonify({
        'status': 'success',
        'songusers': arr
    })
#########################################################
##                     Quotes                          ##
#########################################################
#TODO fix methods
@app.route('/api/quotes', methods=['GET'])
def get_quotes():
    # print(db_session.query(Quote).first())
    # rs = db_session.query(Quote).all()
    rs = db_session.execute('select * from quote')
    print(rs)
    arr = []
    for row in rs:
        d = dict(row.items())
        arr.append(d)
    return jsonify({
        'status': 'success',
        'quotes': arr
    })

@app.route('/api/quotes/add', methods=['POST'])
def add_quote():
    post_data = request.get_json()
    to_add = Quote(post_data.get('quote'), post_data.get('author'), post_data.get('date'), 0, post_data.get('happiness'))
    db_session.add(to_add)
    db_session.commit()
    print('added quote %s' % (post_data.get('quote')))
    return jsonify({
        'status': 'success'
    })

@app.route('/api/quotes/delete', methods=['POST'])
def delete_quote():
    payload = request.get_json()
    target_quote = payload.get('quote')
    print(payload)
    print('deleting quote %s' % (target_quote))
    db_session.query(Quote).filter(Quote.text==target_quote).delete()
    db_session.commit()
    return jsonify({
        'status': 'success'
    })

@app.route('/api/quotes/update', methods=['POST'])
def update_quote():
    payload = request.get_json()
    target_quote = payload.get('quote')
    print('update quote')
    return jsonify({
        'status': 'success'
    })

@app.route('/api/quoteuser', methods=['POST'])
def get_quoteusers():
    payload = request.get_json()
    # get quote id from quote
    rs = s.execute('select quote_id from quote where text = :quote', {'quote': payload.get('quote')}).fetchone()
    qid = rs[0]

    # get all user id's with this quote id
    rs = s.execute('select u.username, u.happiness from users u where u.user_id in (select uq.user_id from userquote uq where uq.quote_id = :quote_id)', {'quote_id': qid})
    arr = []
    for row in rs:
        d = dict(row.items())
        arr.append(d)
    return jsonify({
        'status': 'success',
        'quoteusers': arr
    })

#########################################################

# clear kill [me] switch
@app.route('/api/clear', methods=['POST'])
def clear():
    print('clearing all tables')
    db_session.query(Song).delete()
    db_session.query(User).delete()
    db_session.query(Quote).delete()
    db_session.query(SongUser).delete()
    db_session.query(QuoteUser).delete()
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
