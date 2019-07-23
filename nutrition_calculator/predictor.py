class Predictor:

    def __init__(self ):
        return

    def get_weight_from_calories( self, calories ):

        min_weight = ((calories / 1.65)/24) * 2.2
        max_weight = ((calories)/24) * 2.2
        return round(min_weight, 2), round(max_weight, 2)


    def get_calories_from_weight( self, weight ):

        min_calories = (weight/2.2) * 24
        target_calories = min_calories * 1.65

        return round(min_calories), round(target_calories)


    def get_water_from_weight( self, weight ):

        oz = weight * 0.5
        cups = round(oz * 0.125, 2)

        pints = round(cups / 2, 2)

        return pints


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
