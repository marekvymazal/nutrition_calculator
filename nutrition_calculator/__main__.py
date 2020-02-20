import sys
import os
import getopt
import shutil, errno

from pathlib import Path

from .nutrition_calculator import NutritionCalculator

def main():
    """The main routine."""
    argv = sys.argv[1:]

    help_str = """

    COMMANDS

    -h,--help               Show help
    --recipe <recipe_name>    Calculates nutrition for specified recipe
    --code ndb_id           Downloads nutrition data from usda database ndb code
    --codes                 Downloads all nutrition data using food codes in data/index.csv and Documents/Nutrition/index.csv
    --debug                 Runs in debug mode (gives more output)
    download <item_name>    Downloads item data, finds item json file in Nutrition/Items and uses "code" value to find data.
                            Downloads it to Nutrition/Data
    sync                    Copies all data, recipes, items to your local Nutrition folder

    validate                Scans all files and reports any errors

    new recipe "Recipe name"     Creates a new recipe file from template
    new item "Item Name"         Creates a new item file from template
    new data "Item Name"         Creates a new data file from template


    HOW TO USE

    Documents/Nutrition/
        Recipes/
            store recipe .txt files here

        Items/
            store item information here

        Data/
            store item nutrition data here


    Recipe File Example:

        overnight_oats.txt

            1 cup oatmeal
            1 cup oat milk
            1/3 cup blueberries
            1 tbsp maple syrup

    Get nutrition information of overnight_oats.txt recipe

        nutrition_calculator --recipe overnight_oats

    add multiple recipes

        nutrition_calculator --recipe overnight_oats --recipe cashew_stirfry --recipe lentil_chili

    Recipe files exist in Documents/Nutrition/Recipes
    """

    print("""
    Nutrition Calculator
    Copyright 2020 Marek Vymazal

    This program uses FoodData Central for its data
    U.S. Department of Agriculture, Agricultural Research Service.
    FoodData Central, 2019. fdc.nal.usda.gov.
    """)

    #print(os.getcwd())
    #print(Path.home())
    #module_path = os.path.dirname(__file__)
    #data_path = os.path.join(module_path,'data')

    run = True
    recipes = []

    nc = NutritionCalculator()
    nc.setup()

    try:
        opts, args = getopt.getopt(argv,"hirf:",["help","recipe=","code=","filename=","codes","debug","download","sync","validate", 'new'])

    except getopt.GetoptError:
        print(help_str)
        sys.exit(2)
        return

    for opt, arg in opts:
        if opt in ['--debug']:
            NutritionCalculator.debug = True

    filename = None
    for opt, arg in opts:
        if opt in ['-f', '--filename']:
            filename = arg

    # download
    if 'download' in argv:
        index = argv.index('download')
        items = argv[index+1:]
        for item in items:
            print("trying to download: " + item)
            nc.download_item(item)

        return

    # sync
    if 'sync' in argv:
        nc.sync()
        return

    # validate
    if 'validate' in argv:
        nc.validate()
        return

    # new
    if 'new' in argv:
        index = argv.index('new')
        _type = argv[index+1]
        _name = argv[index+2]

        nc.add_new(_type, _name)

        return


    for opt, arg in opts:

        if NutritionCalculator.debug:
            print(opt, arg)

        if opt in ['-h', '--help']:
            print (help_str)
            sys.exit()
            return

        if opt in ['-r','--recipe']:
            if NutritionCalculator.debug:
                print('append recipe ' + arg)
            recipes.append(arg)
            run = True

        """
        if opt in ['--code']:
            code = arg
            nc.get_data_from_code( code, filename=filename )
            run = False

        if opt in ['--codes']:
            nc.get_data_from_codes( os.path.join( NutritionCalculator.module_data, 'index.csv') )
            nc.get_data_from_codes( os.path.join( NutritionCalculator.local_documents, 'index.csv') )
            run = False
        """

    # Execute
    if run:
        if len(recipes) > 0:
            nc.process_recipes(recipes)
        else:
            nc.execute()


if __name__ == "__main__":
    main()
