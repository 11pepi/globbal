'''
ORM base stuff
'''
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from functools import wraps
import os

Base = declarative_base()
DBURL = os.environ["DATABASE_URL"]
#DBURL = "sqlite:///primary.db"
_engine = None

def engine():
    '''
    get an Engine
    '''
    if not _engine:
        return create_engine(DBURL)
    else:
        return _engine

def session():
    '''
    get a session
    '''
    return sessionmaker(bind=engine())()

def transaction():
    '''
    starts a new transaction and returns it's session
    '''
    return session().begin().session

def create_all_tables():
    '''
    initializes all tables
    '''
    Base.metadata.create_all(engine())

def db_transaction(fn):
    '''
    safe transaction
    '''
    @wraps(fn)
    def wrapper(*args, **kwargs):
        with session() as s:
            try:
                with s.begin():
                    return fn(*args, session=s, **kwargs)
            except Exception as e:
                #print(f"[DB Error] {type(e).__name__}: {e}")
                s.rollback()
                raise e
    return wrapper
