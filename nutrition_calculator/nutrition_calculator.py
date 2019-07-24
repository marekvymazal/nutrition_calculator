
import os
from pathlib import Path

from .web_html import WebHTML
from .recipe import Recipe
from .predictor import Predictor
from .data_object import DataObject

import pandas as pd

class NutritionCalculator:

    module_data = None # path to modules data folder

    local_documents = None
    local_data = None # where per item csv files are stored
    local_recipes = None # where recipe files are stored
    local_units = None # where unit file are stored

    debug = False

    def __init__(self ):
        module_path = os.path.dirname(__file__)
        NutritionCalculator.module_data = os.path.join(module_path,'data')
        return


    def get_data_from_url( self, url ):
        print( url )
        html = WebHTML.get_url( url )
        print(html)


    def get_data_from_code( self, code, filename=None ):
        """
        Downloads csv data from NDB code
        """
        if NutritionCalculator.local_data == None:
            self.setup()

        if filename == None:
            # TODO: try get filename from code
            pass

        url = "https://ndb.nal.usda.gov/ndb/foods/show/" + code + "?format=Full"
        #"https://ndb.nal.usda.gov/ndb/foods/show/08120?format=Full"
        #html = WebHTML.get_html( url )
        print(url)

        # get download link
        dl = "https://ndb.nal.usda.gov/ndb/foods/show/" + code + "?format=Full&reportfmt=csv&Qv=1"
        #/ndb/foods/show/45041356?format=Full&reportfmt=csv&Qv=1
        #"https://ndb.nal.usda.gov/ndb/foods/show/45041356?format=Full&reportfmt=csv&Qv=1"

        # download csv
        if NutritionCalculator.local_data != None:
            WebHTML.download_folder = NutritionCalculator.local_data

        if filename == None:
            html = WebHTML.get_html( dl, download=True, filename=code+'.csv' )
        else:
            html = WebHTML.get_html( dl, download=True, filename=filename+'.csv' )
        #print(html)


    def get_data_from_codes( self, code_file ):
        """
        Downloads all csv item/ingredient data from a list of NDB codes in code file
        """
        if not os.path.exists( code_file ):
            return

        #df = pd.read_csv(code_file, index_col=False, dtype={'NDB-code': str} )
        #for row in df.itertuples():
        #    print(row[1].strip(), row[2].strip() )
        #    self.get_data_from_code(row[1].strip(), filename=row[2].strip())

        data = open(code_file, encoding='utf-8', mode='r')
        for line in data:
            if line.startswith('NDB-code'):
                continue

            items = line.split(',')

            code = items[0].strip()
            filename = items[1].strip()

            # TODO: get alt names and use them

            self.get_data_from_code(code, filename=filename)

        return


    def process_recipes( self, recipes ):
        """
        Takes list of recipe files and calculates their values
        """
        data = DataObject('Total')

        for recipe in recipes:
            recipe_data = Recipe( os.path.join(NutritionCalculator.local_recipes, recipe ))
            data.calories += recipe_data.calories
            data.carbs += recipe_data.carbs
            data.fat += recipe_data.fat
            data.protein += recipe_data.protein
            data.price += recipe_data.price

        # print total
        if len(recipes) > 1:
            data.print_break()
            data.print_header()
            data.print()

        # predictor
        predictor = Predictor()
        min_weight, max_weight = predictor.get_weight_from_calories( data.calories )
        print (' ')
        print ('Min Weight: ' + str(min_weight))
        print ('Max Weight: ' + str(max_weight))

        min_calories, target_calories = predictor.get_calories_from_weight( 158 )
        print ( 'min calories: ' + str(min_calories) )
        print ('target_calories: ' + str(target_calories) )

        glass = predictor.get_water_from_weight( 158 )
        print ('pints: ' + str(glass) )


    def setup( self ):
        """
        Creates local directories and default files if they do not already exist
        """
        # get configuration files
        documents_path = os.path.join(Path.home(),"Documents")
        NutritionCalculator.local_documents = os.path.join(documents_path, "Nutrition")
        NutritionCalculator.local_data = os.path.join(NutritionCalculator.local_documents, "Data")
        NutritionCalculator.local_recipes = os.path.join(NutritionCalculator.local_documents, "Recipes")
        NutritionCalculator.local_units = os.path.join(NutritionCalculator.local_documents, "Units")

        folders = [
            NutritionCalculator.local_documents,
            NutritionCalculator.local_data,
            NutritionCalculator.local_recipes,
            NutritionCalculator.local_units
        ]

        for folder in folders:
            if not os.path.exists( folder ):
                os.makedirs( folder )
                print("Created directory :" + folder)

        # TODO: copy defaults from data directory?


    def execute( self ):
        """
        Calculates all recipes in recipe folder
        """
        files = []
        for (dirpath, dirnames, filenames) in os.walk(NutritionCalculator.local_recipes):
            for filename in filenames:
                if os.path.splitext(filename)[1] in ['.txt']:
                    files.append(os.path.join( dirpath, filename))

        for f in files:
            print(f)

        if len(files) > 0:
            self.process_recipes( files )
        else:
            print("No recipe files found in recipe folder")
            print("  recipe folder:" + NutritionCalculator.local_recipes)
