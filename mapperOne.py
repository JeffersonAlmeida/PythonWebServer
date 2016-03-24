from sqlalchemy import *

db = create_engine('sqlite:///mapper.db')

db.echo = True

metadata = MetaData(db)

users = Table ('users', metadata,

    Column('name', String(40)),
    Column('age', Integer)

)

class User(Base):
    __tablename__ = 'user'
    id = Column('user_id', Integer, primary_key=True)
    name = Column('user_name', String(50))


usermapper = mapper(User,users)

session = create_session()

fred = User()
fred.name = 'Fred'
fred.age = 37

session.save(fred)
session.flush()

selection = users.select()
collection = selection.execute()

for row in collection:
    print row.name, 'is', row.age, 'years old'
