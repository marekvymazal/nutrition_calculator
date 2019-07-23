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

            # get unit
            unit = None
            found_unit = False

            if len(words) == 1:
                found_unit = True

            if not found_unit:
                for unit_type in self.unit_types:
                    if words[0].startswith(unit_type):
                        unit = unit_type
                        fount_unit = True
                        words.pop(0)
                        break

            # get name
            name = words[0]
            if len(words) > 1:
                name = '_'.join(words)

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
            self.protien += ing.protien

            self.price += ing.price

            self.ingredients.append(ing)

        recipe_file.close()

        self.print()
        print('')
