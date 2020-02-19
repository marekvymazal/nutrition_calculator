
import os
from pathlib import Path

from .recipe import Recipe
from .predictor import Predictor
from .data_object import DataObject

import pandas as pd
import requests
import json

from shutil import copyfile

class NutritionCalculator:

    module_data = None # path to modules data folder

    local_documents = None
    local_data = None # where per item csv files are stored
    local_recipes = None # where recipe files are stored
    local_items = None # where item files are stored

    api_key = None

    debug = False

    def __init__(self ):
        module_path = os.path.dirname(__file__)
        NutritionCalculator.module_data = os.path.join(module_path,'data')
        return


    def get_data_from_code( self, code, filename=None ):
        """
        Downloads csv data from NDB code
        """
        if NutritionCalculator.local_data == None:
            self.setup()

        if filename == None:
            # TODO: try get filename from code
            pass

        url = 'https://api.nal.usda.gov/fdc/v1/' + code
        params = {'api_key': NutritionCalculator.api_key}

        r = requests.get(url, params=params)

        if r.status_code == 200:
            data = json.loads(r.text)
            print(json.dumps(data, indent=4))

            if (filename == None):
                return

            f = open(os.path.join(NutritionCalculator.local_data, filename + ".json"), 'w', encoding='utf-8')
            json.dump(data, f, indent=4)
            f.close()


    def get_data_from_codes( self, code_file ):
        """
        Downloads all csv item/ingredient data from a list of NDB codes in code file
        """
        if not os.path.exists( code_file ):
            return

        data = open(code_file, encoding='utf-8', mode='r')
        for line in data:
            if line.startswith('#'):
                continue

            if line.strip() == '':
                continue

            print(line)

            items = line.split(',')

            code = items[0].strip()
            filename = items[1].strip()

            # TODO: get alt names and use them

            self.get_data_from_code(code, filename=filename)

        return


    def find_item( potential_names ):
        # cross reference data files for potential names using filename and alt names
        if potential_names == None:
            return None, None

        if len(potential_names) == 0:
            return None, None

        for root, subdirs, files in os.walk(NutritionCalculator.local_items):
            for f in files:
                if os.path.splitext(f)[1] != '.json':
                    continue

                n = os.path.splitext(f)[0]
                if n == potential_names[0]:
                    relpath = root[len(NutritionCalculator.local_items)+1:]
                    return n, relpath

        #print("Check alts")

        # if not found check alt names
        for root, subdirs, files in os.walk(NutritionCalculator.local_items):
            for f in files:
                if os.path.splitext(f)[1] != '.json':
                    continue

                #print(os.path.join(root, f))

                input_file = open(os.path.join(root, f), 'r')
                data = json.loads(input_file.read())
                input_file.close()

                n = os.path.splitext(f)[0]

                for alt in data['names']:
                    alt = alt.strip().lower().replace(' ', '_')
                    for potential_name in potential_names:
                        if potential_name == alt:
                            relpath = root[len(NutritionCalculator.local_items)+1:]
                            return n, relpath

        return None, None


    def get_code(self, item_file):
        if NutritionCalculator.debug:
            print(NutritionCalculator.local_items + item_file + '.json')

        input_file = open(os.path.join(NutritionCalculator.local_items, item_file + '.json'), 'r')
        data = json.loads(input_file.read())
        input_file.close()

        return data['code']


    def download_item( self, item_name ):
        file_name = item_name.lower().replace(' ', '_')

        # find unit file
        file_name, relpath = NutritionCalculator.find_item( [file_name] )
        print("  " + os.path.join(relpath, file_name))

        # get code
        code = self.get_code(os.path.join(relpath, file_name))
        print("  " + code)

        # download data from code
        url = 'https://api.nal.usda.gov/fdc/v1/' + code
        params = {'api_key': NutritionCalculator.api_key}

        r = requests.get(url, params=params)

        if r.status_code == 200:
            print("  received data")
            data = json.loads(r.text)
            #print(json.dumps(data, indent=4))

            if not os.path.exists(os.path.join(NutritionCalculator.local_data, relpath)):
                os.makedirs(os.path.join(NutritionCalculator.local_data, relpath))

            data_file = os.path.join(NutritionCalculator.local_data, relpath, file_name) + ".json"

            f = open(data_file, 'w', encoding='utf-8')
            json.dump(data, f, indent=4)
            f.close()

            print("  Saved data as: " + data_file)

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
        NutritionCalculator.local_items = os.path.join(NutritionCalculator.local_documents, "Items")

        folders = [
            NutritionCalculator.local_documents,
            NutritionCalculator.local_data,
            NutritionCalculator.local_recipes,
            NutritionCalculator.local_items
        ]

        for folder in folders:
            if not os.path.exists( folder ):
                os.makedirs( folder )
                print("Created directory :" + folder)

        # create config file
        config_path = os.path.join(NutritionCalculator.local_documents, "config.csv")
        if not os.path.exists(config_path):
            f = open(config_path, 'w+')
            f.write("VAR, VALUE\n")
            f.write("API_KEY, <YOUR KEY>")
            f.close()

            print("open " + config_path + " and enter API_KEY");
            print("go to https://fdc.nal.usda.gov/api-key-signup.html to obtain key")

            return False
        else:
            # load key
            data = open(config_path, encoding='utf-8', mode='r')
            for line in data:
                if not line.startswith('API_KEY'):
                    continue

                items = line.split(',')
                NutritionCalculator.api_key = items[1].strip()

                print("Found API_KEY=" + NutritionCalculator.api_key)

        # TODO: copy defaults from data directory?

    def sync( self ):

        # iterate through module files and transfer them to local directories
        files = []

        targets = [
            [os.path.join(NutritionCalculator.module_data, "items"), NutritionCalculator.local_items],
            [os.path.join(NutritionCalculator.module_data, "recipes"), NutritionCalculator.local_recipes],
            [os.path.join(NutritionCalculator.module_data, "data"), NutritionCalculator.local_data]
        ]

        for target in targets:
            for (dirpath, dirnames, filenames) in os.walk(target[0]):
                for filename in filenames:

                    src = os.path.join( dirpath, filename)

                    relpath = dirpath[len(target[0])+1:]
                    relpath = relpath.replace('_',' ').title()

                    target_folder = os.path.join( target[1], relpath)
                    if not os.path.exists( target_folder ):
                        os.makedirs( target_folder )

                    dst = os.path.join( target_folder, filename)

                    print( "  " + dst )

                    copyfile(src, dst)


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
