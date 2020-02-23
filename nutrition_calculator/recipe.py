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
import os
import json

from .data_object import DataObject
from .ingredient import Ingredient
from .predictor import Predictor

from fractions import Fraction

class Recipe(DataObject):

    unit_types = [
        'cup',
        'tbsp',
        'tsp',
        'clove',
        'bulb',
        'can',
        'container',
        'block',
        'package']

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
            amount, words = self.get_amount( words )

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

            if NC.debug:
                print("  potential_names")
                for pn in potential_names:
                    print("    " + pn)

            name, relpath = NC.find_item( potential_names )

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
            ing = Ingredient(amount, unit, name, relpath=relpath)
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


    def get_amount( self, words):

        amount = 0
        x = 0
        while x < len(words):
            try:
                val = float(words[x])
                amount += val
                words.pop(x)
                continue
            except Exception as e:
                pass

            if '/' in words[x]:
                vals = words[x].split('/')
                if len(vals) == 2:
                    try:
                        amount += float( vals[0] ) / float( vals[1] )
                        words.pop(x)
                        continue
                    except:
                        pass

            x += 1

        return amount, words
