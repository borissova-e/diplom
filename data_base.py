import sqlalchemy as sq
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import psycopg2
from sqlalchemy_utils import IntRangeType


Base = declarative_base()


DSN = 'postgresql+psycopg2://vkinder:borisova@localhost:5432/vkinder'

engine = sq.create_engine(DSN)
Session = sessionmaker(bind=engine)



class User(Base):
    __tablename__ = 'user'

    id = sq.Column(sq.Integer, primary_key=True)
    vk_id = sq.Column(sq.Integer, unique=True)
    first_name = sq.Column(sq.String)
    second_name = sq.Column(sq.String)
    age = sq.Column(sq.String)
    range_age = sq.Column(IntRangeType)
    gender = sq.Column(sq.String)
    city = sq.Column(sq.JSON)
    dating_users = relationship('DatingUser')

class DatingUser(Base):
    __tablename__ = 'dating_user'

    id = sq.Column(sq.Integer, primary_key=True)
    vk_id = sq.Column(sq.Integer, unique=True)
    first_name = sq.Column(sq.String)
    second_name = sq.Column(sq.String)
    age = sq.Column(sq.String)
    id_User = sq.Column(sq.Integer, sq.ForeignKey('user.id'))
    black_list = sq.Column(sq.Boolean)
    users = relationship('User', back_populates='dating_users')
    photo = relationship('Photo')

class Photo(Base):
    __tablename__ = 'photos'

    id = sq.Column(sq.Integer, primary_key=True)
    link_photo = sq.Column(sq.String)
    count_likes = sq.Column(sq.Integer)
    id_DatingUser = sq.Column(sq.Integer, sq.ForeignKey('dating_user.id'))
    dating_users = relationship(DatingUser, back_populates='photo')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    Base.metadata.create_all(engine)


