from database import Session
from models import User

def verify_user(username, password):
    session = Session()
    try:
        user = session.query(User).filter(User.username == username, User.password == password).first()
        return user
    finally:
        session.close()
