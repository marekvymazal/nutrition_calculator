# Nutrition Calculator
Copyright (c) 2019 Marek Vymazal

### This program uses FoodData Central for its data
U.S. Department of Agriculture, Agricultural Research Service.  
FoodData Central, 2019. fdc.nal.usda.gov.

## Installation
`pip install .`

__for development__  
`pip install -e .`

__downloading nutrition data (optional)__  
For downloading ingredient nutrition data files (.json) you will need an API Key for FoodData Central obtained here:
* [FoodData Central API KEY](https://fdc.nal.usda.gov/api-key-signup.html)
Then you will need to paste the key into the config.csv file in the Documents/Nutrition folder that is generated when the program is run.

## Instructions
run `nutrition_calculator --help` in terminal to see help

### Download nutrition data for ingredients
`nutrition_calculator --codes`

This will download `.csv` files for ingredient ndb codes in the data/index.csv file
`TODO: create an override file which can retarget ingredient data to different products / brands`


## Directories
```
Nutrition/
    Data/
        ingredient.csv files go here
    Recipes/
        recipe.txt files go here
    Units/
        ingredient.txt files go here
```

### Data for ingredients
The nutrition calculator uses data from [USDA Food Composition Databases](https://ndb.nal.usda.gov/ndb/)

### Recipes files
__Example recipe file: oatmeal.txt__
```
1 cup oatmeal
1 tbsp maple syrup
1/3 cup blueberries
```

## Units files
Unit files hold special conversion information for the calculator.

`price=1.50/100`  
The above line tells the calculator that the item costs $1.50 per 100g

`default=42`  
The above line tells the calculator that the default unit is 42 grams
When no unit is detected it will refer to the default value.
This is useful for measures like 3 bananas or 1 tortilla, since there is no standard measure like 1 cup or 1 tsp it uses the ingredients default value for calculation. So in the above example 1 tortilla will mean 42g worth of tortilla nutrition.
