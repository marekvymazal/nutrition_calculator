import os
import json
from fractions import Fraction

from .data_object import DataObject

import pandas as pd

class Ingredient(DataObject):

    unit_names = ['cup','tbsp','tsp']
    unit_up = [1, 16, 3]
    unit_down = [1, .0625, 0.3333]

    # this list matches items in the data csv files and then uses the id as the attribute to set
    nutrient_list = {
        "calories":"calories",
        "fat":"fat",
        "protein":"protein",
        "carbohydrates":"carbs"
    }

    def __init__(self, amount, unit, name, relpath=""):

        DataObject.__init__(self, name)

        from .nutrition_calculator import NutritionCalculator as NC

        self.amount = amount
        self.unit = unit
        if self.unit == None:
            self.unit = 'default'

        self.unit_values = [None, None, None]

        self.gpu = 0.0
        self.grams = 0.0

        self.price_per_gram = 0.0

        self.amount = amount


        # get unit data
        found_unit = False

        if NC.debug:
            print('['+ str(self.amount) + '][' + self.unit + '][' + self.name + ']')

        unit_path = os.path.join(NC.local_items, relpath, name + '.json')

        if not os.path.isfile(unit_path):
            raise ValueError('no unit found for ' + name + '\n  ' + unit_path)
            return

        if NC.debug:
            print("  " + unit_path)

        ing_unit_file = open(unit_path, 'r')
        data = json.loads(ing_unit_file.read())
        ing_unit_file.close()

        self.price_per_gram = float(data['cost']['price']) / float(data['cost']['grams'])

        if not found_unit:
            if 'default' in data['units']:
                self.gpu = round(float(data['units']['default']), 2)
                found_unit = True

            for x in range(len(self.unit_names)):
                if self.unit_names[x] in data['units']:
                    self.unit_values[x] = round(float(data['units'][self.unit_names[x]]), 2)
                    if self.unit in self.unit_names[x]:
                        found_unit = True

            if self.unit in data['units']:
                self.gpu = round(float(data['units'][self.unit]), 2)
                found_unit = True

        # set unit values if possible
        process_units = None
        for x in range(len(self.unit_values)):
            if self.unit_values[x] != None:
                process_units = x

        if process_units != None:
            # process upstream
            while process_units > 0:
                self.unit_values[process_units-1] = self.unit_values[process_units] * self.unit_up[process_units]
                process_units -= 1

            # process downstream
            process_units = 0
            while process_units < len(self.unit_values)-1:
                self.unit_values[process_units+1] = round(self.unit_values[process_units] * self.unit_down[process_units+1],2)
                process_units += 1

            # get unit value key from unit
            if self.unit in self.unit_names:
                index = self.unit_names.index(self.unit)
                self.gpu = round(self.unit_values[index],2)

            if NC.debug:
                for i in range(len(self.unit_values)):
                    print ( '    ' + self.unit_names[i] + ' = ' + str(self.unit_values[i]))

        ing_unit_file.close()

        self.grams = self.amount * self.gpu
        self.price = round(self.price_per_gram * self.grams, 2)

        if NC.debug:
            print('  price:          ' + str(self.price))
            print('  grams per unit: ' + str(self.gpu))
            print('  amount:         ' + str(self.amount))
            print('  grams:          ' + str(self.grams))
            print('  price per gram: ' + str(self.price_per_gram))

        self.process_item()


    def process_item(self):

        from .nutrition_calculator import NutritionCalculator as NC

        file_name = self.name + '.json'
        data_file = None

        for dirpath, dirnames, filenames in os.walk(NC.local_data):
            for _filename in [f for f in filenames if f.endswith('.json')]:
                #print(_filename)
                if _filename == file_name:
                    data_file = os.path.join(dirpath, file_name)

        if NC.debug:
            print(data_file)

        if data_file == None:
            raise ValueError("could not find data file for " + self.name )

        unit_map = {}

        # load json
        f = open(data_file, encoding='utf-8', errors='replace', mode='r')
        text = f.read()
        data = json.loads(text)
        f.close()

        # get units
        to_100g = 1

        if data['servingSize'] != 100:
            to_100g = 100 / data['servingSize']

            if NC.debug:
                print( "  to 100g:" + str(to_100g) )

        if NC.debug:
            print("unit map")
            for key, value in unit_map.items():
                print('  ' + key + '=' + str(value))


        # get values
        if 'nutrientsPerServing' in data:
            for nutrient in Ingredient.nutrient_list:
                if nutrient in data['nutrientsPerServing']:
                    val = (data['nutrientsPerServing'][nutrient]["value"] * to_100g) * 0.01 * self.grams
                    val = round(val, 2)
                    setattr(self, Ingredient.nutrient_list[nutrient], val)


        # calculate missing data
        if self.calories == 0:
            self.calories += self.fat * 9
            self.calories += self.carbs * 4
            self.calories += self.protein * 4

        return
