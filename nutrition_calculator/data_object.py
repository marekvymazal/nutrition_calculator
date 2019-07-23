

class DataObject:

    header = ''

    def __init__(self, name):

        self.name = name
        if self.name == None:
            self.name = ''

        self.print_str = ' ' * 20

        self.calories = 0
        self.cal_carbs = 0
        self.cal_fat = 0
        self.cal_protien = 0

        self.carbs = 0
        self.fat = 0
        self.protien = 0

        self.price = 0

    def print_header(self):
        index = 0
        self.header = ' ' * 60

        self.header = self.insert_string(self.header, index, 'Name')
        index += 20

        self.header = self.insert_string(self.header, index, 'Calories')
        index += 10

        self.header = self.insert_string(self.header, index, 'Carbs')
        index += 10

        self.header = self.insert_string(self.header, index, 'Fat')
        index += 10

        self.header = self.insert_string(self.header, index, 'Protien')
        index += 20

        self.header = self.insert_string(self.header, index, 'Price')
        index += 10

        print(self.header)


    def print_break(self):
        print ('-' * 60)


    def print(self):
        index = 0
        self.print_str = ' ' * 60

        self.print_str = self.insert_string(self.print_str, index, str(self.name))
        index += 20

        self.print_str = self.insert_string(self.print_str, index, str(self.calories))
        index += 10

        self.print_str = self.insert_string(self.print_str, index, str(self.carbs))
        index += 10

        self.print_str = self.insert_string(self.print_str, index, str(self.fat))
        index += 10

        self.print_str = self.insert_string(self.print_str, index, str(self.protien))
        index += 20

        price_str = '{0:.2f}'.format(round(self.price, 2))
        self.print_str = self.insert_string(self.print_str, index, price_str)
        index += 10

        print (self.print_str)

    def insert_string( self, _str, _index, _value ):
        end = _index + len(_value)
        _str = _str[:(_index)] + _value + _str[(end):]
        return _str
