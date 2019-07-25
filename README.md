# Nutrition Calculator
Copyright (c) 2019 Marek Vymazal

## Installation
`pip install .`

__for development__
`pip install -e .`

__requirements__
For downloading ingredient nutrition data files (.csv) you will need:
* [Firefox](https://www.mozilla.org/en-US/firefox/new/)
* [Firefox Gecko driver](https://github.com/mozilla/geckodriver/releases/)
`TODO: download location / path to gecko`

## Instructions
run `nutrition_calculator` in terminal to see help

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
