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

    --debug                 Runs in debug mode (gives more output)

    recipe <recipe_name>    Calculates nutrition for specified recipe

    download <item_name> ...   Downloads item data, finds item json file in Nutrition/Items and uses "code" value to find data.
                               Downloads it to Nutrition/Data

    download all                 Downloads all items with codes

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

    run = True
    recipes = []

    nc = NutritionCalculator()
    nc.setup()

    # enable debug?
    if '--debug' in argv:
        NutritionCalculator.debug = True
        del argv[argv.index('--debug')]
        print(argv)

    # show help?
    if any(arg in ['-h','--help'] for arg in argv):
        print (help_str)
        sys.exit()
        return

    # download
    if 'download' == argv[0]:

        if 'all' == argv[1]:
            # download all
            nc.download_all()
        else:
            index = argv.index('download')
            items = argv[index+1:]
            for item in items:
                print("trying to download: " + item)
                nc.download_item(item)

        return

    # sync
    if 'sync' == argv[0]:
        nc.sync()
        return

    # validate
    if 'validate' == argv[0]:
        nc.validate()
        return

    # new
    if 'new' == argv[0]:
        index = argv.index('new')
        _type = argv[index+1]
        _name = argv[index+2]

        nc.add_new(_type, _name)

        return

    # calculate recipes
    if 'recipe' == argv[0]:
        for x in range(1,len(argv)):
            if NutritionCalculator.debug:
                print('append recipe ' + argv[x])
            recipes.append(argv[x])

        run = True

    # Execute
    if run:
        if len(recipes) > 0:
            nc.process_recipes(recipes)
        else:
            nc.execute()


if __name__ == "__main__":
    main()
