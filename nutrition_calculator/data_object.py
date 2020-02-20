

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
        self.cal_protein = 0

        self.carbs = 0
        self.fat = 0
        self.protein = 0

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

        self.header = self.insert_string(self.header, index, 'Protein')
        index += 10

        self.header = self.insert_string(self.header, index, 'Price')
        index += 10

        print(self.header)


    def print_break(self):
        print ('-' * 60)

    def pretty_number(self, num, d ):
        if d == 0:
            return (str(int(num)))
        else:
            return "{:.{}f}".format(round(num, d), d)

    def print(self):
        index = 0
        self.print_str = ' ' * 70

        values = [
            [self.name, None, '', '', False, 20],
            [self.calories, 0, '', '', True, 10],
            [self.carbs, 1, '', 'g', True, 10],
            [self.fat, 1, '', 'g', True, 10],
            [self.protein, 1, '', 'g', True, 10],
            [self.price, 2, '$', '', True, 10]
        ]

        for val in values:
            index += val[5]

            vs = str(val[0])
            if val[1] != None:
                vs = self.pretty_number( val[0], val[1] )

            vs = val[2] + vs + val[3]

            padding = 0
            if val[4]:
                padding = -(len(vs)+2)
            else:
                padding = val[5] * -1

            self.print_str = self.insert_string(self.print_str, index+padding, vs)


        #index += 10

        #price_str = '{0:.2f}'.format(round(self.price, 2))
        #self.print_str = self.insert_string(self.print_str, index, price_str)
        #index += 10

        print (self.print_str)

    def insert_string( self, _str, _index, _value ):
        end = _index + len(_value)
        _str = _str[:(_index)] + _value + _str[(end):]
        return _str
