import os
import sys
import json
import re

def convert_usda_data( data ):

    from .nutrition_calculator import NutritionCalculator as NC

    # load template
    template_file = os.path.join(NC.module_templates, 'data.json')
    input_file = open(template_file, 'r')
    converted = json.loads(input_file.read())
    input_file.close()

    # add data
    print("\n\nRAW" + '='*70)
    print(json.dumps(data, indent=4))

    print("\n\nCONVERTED" + '='*70)

    to_serving = 1

    # name
    if 'description' in data:
        converted['description'] = data['description']
        print(converted['description'])

    # transfer item codes
    if 'ndbNumber' in data:
        converted["ndbNumber"] = data['ndbNumber']
        print("ndbNumber: " + str(converted['ndbNumber']))

    if 'fdcId' in data:
        converted["fdcId"] = data['fdcId']
        print("fdcId: " + str(converted['fdcId']))

    if 'gtinUpc' in data:
        converted['gtinUpc'] = data['gtinUpc']
        print("gtinUpc: " + str(converted['gtinUpc']))

    # transfer serving size
    if 'servingSize' in data and 'servingSizeUnit' in data:
        converted['servingSize'] = data['servingSize']
        converted['servingSizeUnit'] = data['servingSizeUnit']
        print("\nservingSize: " + str(converted['servingSize']) + " " + converted['servingSizeUnit'])

        if data['servingSize'] != 100:
            to_serving = float(data['servingSize'] / 100)

    else:
        # force 100g?
        converted['servingSize'] = 100

    if 'householdServingFullText' in data:
        converted['servingText'] = data['householdServingFullText']
        print(converted['servingText'])

    # transfer nutrient label
    nutrients = [
        "fat",
        "saturatedFat",
        "transFat",
        "cholesterol",
        "sodium",
        "carbohydrates",
        "fiber",
        "sugars",
        "protein",
        "calcium",
        "iron",
        "potassium",
        "calories"
    ]

    if 'labelNutrients' in data:
        print("\nLabel")
        for nutrient in data['labelNutrients']:
            if nutrient in converted['nutrientsPerServing']:
                converted['nutrientsPerServing'][nutrient]['value'] = data['labelNutrients'][nutrient]['value']
                print("  " + nutrient + ": " + str(data['labelNutrients'][nutrient]['value']))
            else:
                print("NEED TO ADD NUTRIENT TO TEMPLATE " + nutrient)
                sys.quit()

    # extra nutrients (based on 100ml or 100g so values need to be scaled to match serving size)
    if "foodNutrients" in data:

        print("\nMore nutrients")
        nutrient_label_translation = [
            ["calcium", "Calcium, Ca"],
            ["iron", "Iron, Fe"],
            ["vitaminA", "Vitamin A, IU"],
            ["vitaminD", "Vitamin D (D2 + D3), International Units"],
            ["vitaminC", "Vitamin C, total ascorbic acid"],
            ["cholesterol", "Cholesterol"],

            ["fat","Total lipid (fat)"],

            ["saturatedFat", "Fatty acids, total saturated"],
                ["4:0","4:0"],
                ["6:0","6:0"],
                ["8:0","8:0"],
                ["10:0","10:0"],
                ["12:0","12:0"],
                ["14:0","14:0"],
                ["15:0","15:0"],
                ["16:0","16:0"],
                ["17:0","17:0"],
                ["18:0","18:0"],
                ["20:0","20:0"],
                ["22:0","22:0"],
                ["24:0","24:0"],

            ["monosaturatedFat", "Fatty acids, total monounsaturated"],
                ["14:1","14:1"],
                ["15:1","15:1"],
                ["16:1","16:1"],
                ["16:1 c","16:1 c"],
                ["17:1","17:1"],
                ["18:1","18:1"],
                ["18:1 c","18:1 c"],
                ["20:1","20:1"],
                ["22:1","22:1"],
                ["22:1 c","22:1 c"],
                ["24:1 c","24:1 c"],

            ["polyunsaturatedFat","Fatty acids, total polyunsaturated"],
                ["18:2","18:2"],
                ["18:2 n-6 c,c","18:2 n-6 c,c"],
                ["18:2 CLAs","18:2 CLAs"],
                ["18:3","18:3"],
                ["18:3 n-3 c,c,c (ALA)","18:3 n-3 c,c,c (ALA)"],
                ["18:3 n-6 c,c,c","18:3 n-6 c,c,c"],
                ["18:3i","18:3i"],
                ["18:4","18:4"],
                ["20:2 n-6 c,c","20:2 n-6 c,c"],
                ["20:3","20:3"],
                ["20:3 n-3","20:3 n-3"],
                ["20:3 n-6","20:3 n-6"],
                ["20:4","20:4"],
                ["20:5 n-3 (EPA)","20:5 n-3 (EPA)"],
                ["22:4","22:4"],
                ["22:5 n-3 (DPA)","22:5 n-3 (DPA)"],
                ["22:6 n-3 (DHA)","22:6 n-3 (DHA)"],

            ["transFat","Fatty acids, total trans"],
                ["Fatty acids, total trans-monoenoic","Fatty acids, total trans-monoenoic"],
                ["16:1 t","16:1 t"],
                ["18:1 t","18:1 t"],
                ["22:1 t","22:1 t"],
                ["18:2 t not further defined","18:2 t not further defined"],
                ["Fatty acids, total trans-polyenoic","Fatty acids, total trans-polyenoic"],

            ["protein", "Protein"],

            ["carbohydrates", "Carbohydrate, by difference"],
            ["carbohydrates", "Carbohydrates"],

            ["calories", "Energy", "kcal"],
            ["fiber", "Fiber, total dietary"],
            ["fiberSoluble","Fiber, soluble"],
            ["potassium","Potassium, K"],
            ["sodium","Sodium, Na"],

            ["aminoAcids","Amino acids"],
            ["alcohol","Alcohol, ethyl"],
            ["caffeine","Caffeine"],
            ["theobromine","Theobromine"],


            ["vitaminD","Vitamin D (D2 + D3)"],
            ["vitaminK","Vitamin K (phylloquinone)"],
            ["lipids","Lipids"],


            ["sugars","Sugars, total including NLEA"],

            ["water","Water"],
            ["ash","Ash"],

            ["sucrose","Sucrose"],
            ["glucose","Glucose (dextrose)"],
            ["fructose","Fructose"],
            ["lactose","Lactose"],
            ["maltose","Maltose"],
            ["galactose","Galactose"],
            ["starch","Starch"],
            ["minerals","Minerals"],

            ["magnesium","Magnesium, Mg"],
            ["phosphorus","Phosphorus, P"],

            ["zinc","Zinc, Zn"],
            ["copper","Copper, Cu"],
            ["manganese","Manganese, Mn"],
            ["selenium","Selenium, Se"],
            ["vitaminsAndOther","Vitamins and Other Components"],

            ["thiamin","Thiamin"],
            ["riboflavin","Riboflavin"],
            ["niacin","Niacin"],
            ["pantothenicAcid","Pantothenic acid"],
            ["vitaminB6","Vitamin B-6"],
            ["folateTotal","Folate, total"],
            ["folicAcid","Folic acid"],
            ["folateFood","Folate, food"],
            ["folateDFE","Folate, DFE"],
            ["choline","Choline, total"],
            ["betaine","Betaine"],
            ["vitaminB12","Vitamin B-12"],
            ["vitaminB12Added","Vitamin B-12, added"],
            ["vitaminA","Vitamin A, RAE"],
            ["retinol","Retinol"],
            ["caroteneBeta","Carotene, beta"],
            ["caroteneAlpha","Carotene, alpha"],
            ["cryptoxanthinBeta","Cryptoxanthin, beta"],
            ["lycopene","Lycopene"],
            ["lutein_zeaxanthin","Lutein + zeaxanthin"],
            ["vitaminE","Vitamin E (alpha-tocopherol)"],
            ["vitaminEAdded","Vitamin E, added"],
            ["tocopherolBeta","Tocopherol, beta"],
            ["tocopherolGamma","Tocopherol, gamma"],
            ["tocopherolDelta","Tocopherol, delta"],
            ["tocotrienolAlpha","Tocotrienol, alpha"],
            ["tocotrienolBeta","Tocotrienol, beta"],
            ["tocotrienolGamma","Tocotrienol, gamma"],
            ["tocotrienolDelta","Tocotrienol, delta"],

            ["fluoride","Fluoride, F"],
            ["tryptophan","Tryptophan"],
            ["threonine","Threonine"],
            ["isoleucine","Isoleucine"],
            ["leucine","Leucine"],
            ["lysine","Lysine"],
            ["methionine","Methionine"],
            ["cystine","Cystine"],
            ["phenylalanine","Phenylalanine"],
            ["tyrosine","Tyrosine"],
            ["valine","Valine"],
            ["arginine","Arginine"],
            ["histidine","Histidine"],
            ["alanine","Alanine"],
            ["asparticAcid","Aspartic acid"],
            ["glutamicAcid","Glutamic acid"],
            ["glycine","Glycine"],
            ["proline","Proline"],
            ["serine","Serine"]
        ]

        for nutrient in data['foodNutrients']:
            found = False
            for t in nutrient_label_translation:
                if t[1] == nutrient['nutrient']['name']:

                    if len(t) > 2 and nutrient['nutrient']['unitName'] != t[2]:
                        continue

                    if not 'amount' in nutrient:
                        continue

                    if nutrient['amount'] == 0:
                        found = True
                        continue

                    try:
                        #print(nutrient['nutrient']['name'])
                        # identified
                        converted['nutrientsPerServing'][t[0]] = {}
                        converted['nutrientsPerServing'][t[0]]["value"] = round((nutrient['amount'] * to_serving),3)
                        converted['nutrientsPerServing'][t[0]]["unit"] = nutrient['nutrient']['unitName']
                        print("  " + t[0] + ": " + str(converted['nutrientsPerServing'][t[0]]['value']))
                        found = True
                    except Exception as e:
                        print(str(e))
                        print(json.dumps(nutrient, indent=4))
                        sys.exit()

            if not found:
                amount = None
                if 'amount' in nutrient:
                    amount = nutrient['amount']
                if amount != None:
                    print("Could not find: " + str(nutrient['nutrient']['name']) + " " + str(amount) + " " + nutrient['nutrient']['unitName'])

    """
    "foodNutrients": [
        {
            "type": "FoodNutrient",
            "id": 3672385,
            "nutrient": {
                "id": 1087,
                "number": "301",
                "name": "Calcium, Ca",
    """

    if 'ingredients' in data:

        print("\nIngredients")
        converted['ingredients'] = []

        ingredients = re.split(r',(?!(?:[^(]*\([^)]*\))*[^()]*\))', data['ingredients'])
        for ingredient in ingredients:
            print("  " + ingredient.strip())
            converted['ingredients'].append(ingredient.strip())

    print("")

    return converted
