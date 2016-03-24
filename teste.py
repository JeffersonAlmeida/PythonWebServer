class Bike:

    """
    A simple Bike Class
    """

    def __init__(self, name, brand, color):
        self.name = name
        self.brand = brand
        self.color = color

    brand  = 'DEFAULT'
    color = 'DEFAULT'

    def f(self):
        return 'hello world'


class Bikes:

    def __init__(self):
        self.truck = []

    def add(self, bike):
        self.truck.append(bike)

    def show(self):
        for bike in self.truck:
            print bike.name + ' ' + bike.brand + ' ' + bike.color



bag = Bikes()
bag.add(Bike('CALANGA', 'CALOI', 'AZUL'))
bag.add(Bike('CALANGA', 'CALOI', 'VERMELHA'))
bag.add(Bike('CALANGA', 'CALOI', 'BRANCA'))
bag.show()
