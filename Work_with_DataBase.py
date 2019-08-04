from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB
import json


# def auth_info_bd():
#     dbname = input('Введите имя БД, в которую хотите записать данные: ')
#     user = input('Введите пользователся БД: ')
#     password = input('Введите пароль пользователя БД: ')
#     auth_unfo = f'postgresql://{user}:{password}@localhost/{dbname}'
#     return auth_unfo

Base = declarative_base()
# engine = create_engine(auth_info_bd())
engine = create_engine('postgresql://admin@localhost/VKinder')
Session = sessionmaker(bind=engine)

def create_models(user):
    class VKinder(Base):
        __tablename__ = f'{user}'

        id = Column(Integer, primary_key=True)
        id_name = Column(Integer, nullable=False, unique=True)
        photos = Column(JSONB, server_default='[]', default=list, nullable=False)

session = Session()

def create_all():
    Base.metadata.create_all(engine)

def get_10_pretenders():
    with open('ten_pretenders.json', 'r') as out_info:
        ten_pretenders = json.load(out_info)
        return ten_pretenders

def add_pretender(**kwargs):
    pretender = VKinder(**kwargs)
    session.add(pretender)
    session.commit()

def add_all_pretenders():
    ten_pretenders = get_10_pretenders()
    for item in ten_pretenders:
        add_pretender(id_name=item['id'],
                   photos=item['photos'])