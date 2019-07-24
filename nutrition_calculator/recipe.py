'''
TODO:
    Title support / format
    Recipe XML
    Data to array template
    Debug/Clean print
    Spreadsheet output
    Data accuracy

NOTES
    Raw folder contains details of ingredients per 100g
    Unit folder containers details of what unit translates to grams
    Recipes folder contains all recipes
'''
from bs4 import BeautifulSoup
import html5lib
import os

from .data_object import DataObject
from .ingredient import Ingredient
from .predictor import Predictor


class Recipe(DataObject):

    unit_types = [
        'cup',
        'tbsp',
        'tsp',
        'clove',
        'bulb',
        'can',
        'container']

    def __init__(self, recipe_file ):

        DataObject.__init__(self, 'TOTAL')

        from .nutrition_calculator import NutritionCalculator as NC

        if NC.debug:
            print("initialize:" + recipe_file)

        self.ingredients = []

        self.print_header()

        recipe_file = open(recipe_file)
        for line in recipe_file:

            # break line into words
            words = line.strip().split()
            if len(words) == 0: # if no words, skip
                break

            # get amount
            amount = words[0]
            words.pop(0)

            # find unit
            unit = None
            if len(words) > 1:
                for unit_type in self.unit_types:
                    if words[0] in [unit_type, str(unit_type + 's')]:
                        unit = unit_type
                        words.pop(0)
                        break

            # get potential ingredient names
            potential_names = []

            name = '_'.join(words).lower()
            potential_names.append(name)


            if words[-1][-1] == 's':
                # remove 's'
                words[-1] = words[-1][:-1]
                name = '_'.join(words).lower()
                potential_names.append(name)
            else:
                # add 's'
                words[-1] = words[-1]+'s'
                name = '_'.join(words).lower()
                potential_names.append(name)

            name = self.find_ingredient( potential_names )
            if name == None:
                raise ValueError('could not find ingredient data for: ' + line)

            if unit == None:
                # ingredient is unit (example 1 banana, 3 vegan sausages)
                # unit == any of potential names
                pass

            if NC.debug:
                # print info
                info_str = ''
                if amount != None:
                    info_str += '[' + str(amount) + ']'
                if unit != None:
                    info_str += '[' + str(unit) + ']'
                if name != None:
                    info_str += '[' + str(name) + ']'

                print (info_str)

            # process ingredient
            ing = Ingredient(amount, unit, name)
            ing.print()

            self.calories += ing.calories
            self.carbs += ing.carbs
            self.fat += ing.fat
            self.protein += ing.protein

            self.price += ing.price

            self.ingredients.append(ing)

        recipe_file.close()

        self.print()
        print('')


    def find_ingredient( self, potential_names ):
        # cross reference data files for potential names using filename and alt names

        from .nutrition_calculator import NutritionCalculator as NC

        code_file = os.path.join( NC.module_data, 'index.csv')
        #nc.get_data_from_codes( os.path.join( NutritionCalculator.local_documents, 'index.csv') )

        data = open(code_file, encoding='utf-8', mode='r')
        for line in data:
            if line.startswith('NDB-code'):
                continue

            items = line.split(',')

            code = items[0].strip()
            filename = items[1].strip()

            if filename in potential_names:
                return filename

            for item in items[2:]:
                item = item.strip().replace(' ','_')
                if item in potential_names:
                    return filename

        data.close()
