from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

rest = Restaurant(name = "Pizza Palace")

session.add(rest)
session.commit()

item = MenuItem(
    name = "Pizza Calabreza",
    course = "entree",
    description = "Description",
    price = "25.00 R$",
    restaurant = rest
)

session.add(item)
session.commit()

restaurants = session.query(Restaurant).all()
menuItems = session.query(MenuItem).all()

for r in restaurants:
    print r.name, r.id

for mi in menuItems:
    print mi.name, mi.id, mi.restaurant_id

pccollection = session.query(MenuItem).filter_by(name = 'Pizza Calabreza')

for pc in pccollection:
    print pc.id, " > ", pc.name
    pc.name = "PIZZA CALABRESA ESPECIAL DA CASA"
    session.add(pc)
    session.commit()


#itemOne = session.query(MenuItem).filter_by(id = 1).one()
#session.delete(itemOne)
#session.commit()

print "new ones"
for mi in menuItems:
    print mi.name, mi.id
