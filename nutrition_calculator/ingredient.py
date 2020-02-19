import os
import json
from fractions import Fraction

from bs4 import BeautifulSoup
import html5lib

from .data_object import DataObject

import pandas as pd

class Ingredient(DataObject):

    unit_names = ['cup','tbsp','tsp']
    unit_up = [1, 16, 3]
    unit_down = [1, .0625, 0.3333]

    # this list matches items in the data csv files and then uses the id as the attribute to set
    nutrient_list = {
        "Energy":{'id':'calories','unit':'kcal'},
        "Total lipid (fat)":{'id':'fat'},
        "Protein":{'id':'protein'},
        "Carbohydrate, by difference":{'id':'carbs'}
    }

    def __init__(self, amount, unit, name):

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

        #print (self.name)


        # get amount
        self.amount = float(sum(Fraction(s) for s in amount.split()))


        # get unit data
        found_unit = False

        if NC.debug:
            print('['+ str(self.amount) + '][' + self.unit + '][' + self.name + ']')

        unit_path = os.path.join(NC.local_units, name + '.txt')

        if not os.path.isfile(unit_path):
            raise ValueError('no unit found for ' + name + '\n  ' + unit_path)
            return

        if NC.debug:
            print("  " + unit_path)

        ing_unit_file = open(unit_path, 'r')
        for line in ing_unit_file:
            if 'price' in line:
                price, grams = line.strip().split('=')[1].split('/')
                self.price_per_gram = float(price) / float(grams)
                #print (price + " / " + gramses + " = " + str(self.price_per_gram) )

            if not found_unit:
                if 'default' in line:
                    val = line.strip().split('=')[1]
                    self.gpu = round(float(val),2)
                    fount_unit = True
                for x in range(len(self.unit_names)):
                    if self.unit_names[x] in line:
                        self.unit_values[x] = round(float(line.strip().split('=')[1]),2)
                        if self.unit in self.unit_names[x]:
                            fount_unit = True
                if self.unit in line:
                    val = line.strip().split('=')[1]
                    self.gpu = round(float(val),2)
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
        found = False
        try:
            # is 100g?
            if 'inputFoods' in data:
                for u in data['inputFoods']:
                    if u['unit'] == 'GM': # gram weight
                        if u['gramWeight'] == 100:
                            #print("  using 100 g")
                            pass
                        else:
                            #print("  gram weight is not 100g")
                            pass

                        found = True

        except:
            pass

        if not found:
            try:
                if data["servingSizeUnit"] == "ml":
                    #print("  using 100 ml?")
                    found = True
                elif data["servingSizeUnit"] == "g":
                    #print("  using 100 g")
                    found = True

            except KeyError:
                pass

        if not found:
            print("  COULD NOT FIND UNIT IN " + self.name)

        to_100g = 1

        if NC.debug:
            print("unit map")
            for key, value in unit_map.items():
                print('  ' + key + '=' + str(value))


        # get values
        # store values of 1g
        for nutrient in Ingredient.nutrient_list:
            #if 'unit' in Ingredient.nutrient_list[nutrient]:
            #    if unit != Ingredient.nutrient_list[nutrient]['unit']:
            #        continue
            if 'foodNutrients' in data:
                for item in data['foodNutrients']:
                    if nutrient == item['nutrient']['name']:
                        #print("  " + item['nutrient']['name'])

                        #print(Ingredient.nutrient_list[nutrient]['id'])

                        id = Ingredient.nutrient_list[nutrient]['id']
                        #print("  " + id)

                        val = item["amount"] * to_100g * 0.01 * self.grams
                        #val = float(items[unit_map['100g']]) * 0.01 * self.grams

                        val = round(val, 2)
                        #print('  ' + id + '=' + str(val) + "   (100g)=" + str(item["amount"]))
                        setattr(self, id, val)


        # calculate missing data
        if self.calories == 0:
            self.calories += self.fat * 9
            self.calories += self.carbs * 4
            self.calories += self.protein * 4

        return
