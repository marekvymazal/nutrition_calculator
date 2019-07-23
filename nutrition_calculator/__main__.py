import sys
import os
import getopt
import shutil, errno

from pathlib import Path

from bs4 import BeautifulSoup
import html5lib

from .nutrition_calculator import NutritionCalculator

def main():
    """The main routine."""
    argv = sys.argv[1:]

    help_str = """
    -h,--help               Show help
    --recipe recipe_file    Calculates nutrition for specified recipe
    --code ndb_id           Gets nutrition data from usda database ndb code
    --debug                 Runs in debug mode (gives more output)

    Documents/Nutrition Calculator/
        recipes/
            store recipe .txt files here

        units/
            store unit overrides here

        data/
            store nutrition data here


    Recipe File Example:

    overnight_oats.txt

    1 cup oatmeal
    1 cup oat milk

    1/3 cup blueberries
    1 tbsp maple syrup

    nutrition_calculator --recipe overnight_oats

    add multiple recipes
    nutrition_calculator --recipe overnight_oats --recipe cashew_stirfry --recipe lentil_chili


    Recipe files can exist in Documents/Nutrition Calculator/recipes
    """

    print("Nutrition Calculator")
    print("Copyright 2019 Marek Vymazal")

    #print(os.getcwd())
    #print(Path.home())
    module_path = os.path.dirname(__file__)
    data_path = os.path.join(module_path,'data')

    run = True
    recipes = []

    nc = NutritionCalculator()
    nc.setup()

    try:
        opts, args = getopt.getopt(argv,"hir",["help","recipe=","code=","codes","debug"])

    except getopt.GetoptError:
        print(help_str)
        sys.exit(2)
        return

    for opt, arg in opts:
        if opt in ('--debug'):
            NutritionCalculator.debug = True

    for opt, arg in opts:

        print(opt, arg)

        if opt in ('-h', '--help'):
            print (help_str)
            sys.exit()
            return

        if opt in ('-r','--recipe'):
            print('Recipe ' + arg)
            recipes.append(arg)
            run = True

        if opt in ('--code'):
            code = arg
            nc.get_data_from_code( code )
            run = False

        if opt in ('--codes'):
            nc.get_data_from_codes( os.path.join( data_path, 'index.csv') )
            nc.get_data_from_codes( os.path.join( NutritionCalculator.local_documents, 'index.csv') )
            run = False

    # Execute
    if run:
        nc.execute()


if __name__ == "__main__":
    main()
