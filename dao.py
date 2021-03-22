import config

import psycopg2
from sqlalchemy import Table, Column, Integer, String, VARCHAR, Boolean, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData

engine = create_engine(config.DATABASE_URL, echo=False)
meta = MetaData()

students = Table('students', meta,
                 Column('id', Integer, primary_key=True),
                 Column('user_id', VARCHAR),
                 Column('st_group', String(10)),
                 Column('status', Boolean))

Session = sessionmaker(bind=engine)
session = Session()
conn = psycopg2.connect(config.DATABASE_URL, sslmode='require')
cur = conn.cursor()

def check_student(id_user):
    
    cur.execute(f"select user_id from students where user_id={id_user}::VARCHAR ")
    compare = cur.fetchone
    if str(id_user)==str(compare):
        return True
    else:
        return False


def add_student(id_user, in_group, in_status):
    if check_student(id_user):
        return cur.execute(f"update students set st_group=in_group where user_id={id_user}::VARCHAR")
    else:
        return cur.execute(f"insert into students (user_id, st_group, status) values (%s,%s,%s)",
                           (id_user, in_group, in_status))


def get_group(id_user):
    cur.execute(f"select st_group from students where user_id={id_user}::VARCHAR ")
    return cur.fetchone()
