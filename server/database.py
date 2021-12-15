from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, date as dtdate
from dateutil.tz import tzlocal

Base = declarative_base()

'''
Defining the tables for the database
'''
class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String(120), unique=True, index=True)
    password = Column(String(120))
    happiness = Column(Integer)
    total_happiness = Column(Integer)
    account_age = Column(Integer)

    def __init__(self, username=None, password=None, happiness=0, total_happiness=0, account_age=0):
        self.username = username
        self.password = password
        self.happiness = happiness
        self.total_happiness = total_happiness
        self.account_age = account_age

    def __repr__(self):
        return '<User id: %d username: %s password: %s happiness %d total happiness: %d account age: %d>' % (self.id, self.username, self.password, self.happiness, self.total_happiness, self.account_age)

class Song(Base):
    __tablename__ = 'songs'
    song_id = Column(Integer, primary_key=True)
    name = Column(String(120))
    artist = Column(String(120))
    length = Column(Integer)
    genre = Column(String(120))
    num_assigned = Column(Integer)
    happiness = Column(Integer, index=True)

    def __init__(self, name=None, artist=None, length=0, genre=None, num_assigned=0, happiness=0):
        self.name = name
        self.artist = artist
        self.length = length
        self.genre = genre
        self.num_assigned = num_assigned
        self.happiness = happiness

    def __repr__(self):
        return '<Song id: %d name: %s artist: %s length: %d genre: %s num_assigned: %d happiness: %d>' % (self.id, self.name, self.artist, self.length, self.genre, self.num_assigned, self.happiness)

class Quote(Base):
    __tablename__ = 'quote'
    quote_id = Column(Integer, primary_key=True)
    text = Column(String(240))
    author = Column(String(120))
    date = Column(Date)
    num_assigned = Column(Integer)
    happiness = Column(Integer, index=True)

    def __init__(self, text=None, author=None, date=None, num_assigned=0, happiness=0):
        self.text = text
        self.author = author
        if (date == None):
            date = dtdate.today()
        else:
            date = dtdate.fromisoformat(date)
        print(date)
        self.date = date
        self.num_assigned = num_assigned
        self.happiness = happiness
    
    def __repr__(self):
        return '<Quote id: %d text: %s author: %s date: %r num_assigned: %d happiness: %d>' % (self.id, self.text, self.author, self.date, self.num_assigned, self.happiness)

class SongUser(Base):
    __tablename__ = 'usersong'
    user_id = Column(Integer, primary_key=True)
    song_id = Column(Integer, index=True)

    def __init__(self, user_id=0, song_id=0):
        self.user_id = user_id
        self.song_id = song_id

    def __repr__(self):
        return '<SongUser user_id: %d song_id: %d>' % (self.user_id, self.song_id)

class QuoteUser(Base):
    __tablename__ = 'userquote'
    user_id = Column(Integer, primary_key=True)
    quote_id = Column(Integer, index=True)

    def __init__(self, user_id=0, quote_id=0):
        self.user_id = user_id
        self.quote_id = quote_id

    def __repr__(self):
        return '<QuoteUser user_id: %d quote_id: %d>' % (self.user_id, self.quote_id)
        
engine = create_engine('sqlite:///test.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base.query = db_session.query_property()
def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    #import models 
    Base.metadata.create_all(bind=engine)