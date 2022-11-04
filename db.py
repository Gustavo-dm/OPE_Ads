from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging

engine = create_engine('sqlite:///arquesys.db', echo=True,
                       connect_args={"check_same_thread": False})

Session = sessionmaker(bind=engine)
session = Session()

db = SQLAlchemy()


handler = logging.FileHandler('app.log')
handler.setLevel(logging.DEBUG)

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').addHandler(handler)
