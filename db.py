from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import logging
from config import Config


logger = logging.getLogger(__name__)

Base = declarative_base()
engine = create_engine(Config.DATABASE_URL)

Session = sessionmaker(bind=engine)


@contextmanager
def get_session():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


class Item_line(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    user_id = Column(String)   
    timestamp = Column(String)
    item_id = Column(String)


    def __str__(self):
       return f"user_id={self.user_id}, timestamp={self.timestamp}, item_id={self.item_id}"


if not database_exists(Config.DATABASE_URL):
    create_database(engine.url)
    Base.metadata.create_all(engine)
else:
    Base.metadata.create_all(engine)


def new_item(user_id, timestamp, item_id):
    with get_session() as session:
        session.add(Item_line(user_id=user_id, timestamp=timestamp, item_id=item_id))
        session.commit()


