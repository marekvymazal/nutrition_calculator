import os
from fractions import Fraction

from bs4 import BeautifulSoup
import html5lib

from .data_object import DataObject

class Ingredient(DataObject):

    unit_names = ['cup','tbsp','tsp']
    unit_up = [1, 16, 3]
    unit_down = [1, .0625, 0.3333]

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

        file_name = self.name + '.html'
        data_file = None

        for dirpath, dirnames, filenames in os.walk("raw"):
            for _filename in [f for f in filenames if f.endswith(".html")]:
                if _filename == file_name:
                    data_file = os.path.join(dirpath, file_name)

        html_file = open( data_file, encoding='utf-8', errors='replace', mode='r' )
        html_text = html_file.read()
        html_file.close()

        # make pretty html first
        soup = BeautifulSoup(html_text, 'html5lib')
        prettyHTML = soup.prettify()
        soup = BeautifulSoup(prettyHTML, 'html5lib')

        if soup == None and final_url == None:
            return False

        content = soup.find("fieldset", { "id" : "nutrition-info-container" })

        # Get serving
        serving = content.find("span", {"id" : "servingsize3"})
        #print ('Serving Size:' + serving.text.strip())

        # Get calories
        calories_set = content.find("span", {"id":"NUTRIENT_0"})
        self.calories = round(float(calories_set.text.strip())*.01*self.grams)

        carb_set = content.find("span", {"id":"NUTRIENT_1"})
        self.cal_carbs = round(float(carb_set.text.strip())*.01*self.grams)

        fat_set = content.find("span", {"id":"NUTRIENT_2"})
        self.cal_fat = round(float(fat_set.text.strip())*.01*self.grams)

        protien_set = content.find("span", {"id":"NUTRIENT_3"})
        self.cal_protien = round(float(protien_set.text.strip())*.01*self.grams)

        # Carbs
        carb_set = content.find("span", {"id":"NUTRIENT_4"})
        self.carbs = round(float(carb_set.text.strip())*.01*self.grams)


        # Fats
        fat_set = content.find("span", {"id":"NUTRIENT_14"})
        self.fat = round(float(fat_set.text.strip())*.01*self.grams)


        # Protiens
        protien_set = content.find("span", {"id":"NUTRIENT_77"})
        protien_units_set = content.find("span", {"id":"UNIT_NUTRIENT_77"})
        self.protien = round(float(protien_set.text.strip())*.01*self.grams)


        # Vitamins
        #print ("Vitamins")
        #vitamin_a_set = content.find("span", {"id":"NUTRIENT_100"})
        #vitamin_a_units_set = content.find("span", {"id":"UNIT_NUTRIENT_100"})

        #print ('  Vitamin A:' + vitamin_a_set.text.strip() + " " + vitamin_a_units_set.text.strip())

        # Minerals
