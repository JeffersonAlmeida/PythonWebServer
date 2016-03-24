from sqlalchemy import *

db = create_engine('sqlite:///tutorial.db')
db.echo = True # Try changing this to True and see what happens

metadata = MetaData(db)

users = Table ('users', metadata,

    Column('user_id', Integer, primary_key=True),
    Column('name', String(40)),
    Column('age', Integer),
    Column('password', String)

)

users.create()

insert = users.insert()
insert.execute( name='Mary', age=30, password='secret' )
insert.execute(

    { 'name' : 'John', 'age': 42 },
    { 'name' : 'Susan', 'age': 57 },
    { 'name' : 'Carl', 'age': 42 }

)

selection = users.select()
collection = selection.execute()

for row in collection:
    print row.name, 'is', row.age, 'years old'
