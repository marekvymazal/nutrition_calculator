

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

        self.widths = [20, 10, 10, 10, 10, 10]


    def print_break(self):
        print ('-' * 70)


    def pretty_number(self, num, d ):
        if d == 0:
            return (str(int(num)))
        else:
            return "{:.{}f}".format(round(num, d), d)


    def print_header(self):
        index = 0
        self.header = ' ' * 70

        labels = [
            'Name',
            'Calories',
            'Carbs',
            'Fat',
            'Protien',
            'Price'
        ]

        for x in range(len(labels)):
            self.header = self.insert_string(self.header, index, labels[x])
            index += self.widths[x]

        print(self.header)


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

        print (self.print_str)


    def insert_string( self, _str, _index, _value ):
        end = _index + len(_value)
        _str = _str[:(_index)] + _value + _str[(end):]
        return _str
