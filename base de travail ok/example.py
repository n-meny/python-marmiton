from api_marmiton import Marmiton


# Search :
query_options = {
  "aqt": "Fondue savoyarde",      # Query keywords - separated by a white space
  "dt": "platprincipal",      # Plate type : "entree", "platprincipal", "accompagnement", "amusegueule", "sauce" (optional)
  "exp": 2,                   # Plate price : 1 -> Cheap, 2 -> Medium, 3 -> Kind of expensive (optional)
  "dif": 2,                   # Recipe difficulty : 1 -> Very easy, 2 -> Easy, 3 -> Medium, 4 -> Advanced (optional)
  "veg": 0,                   # Vegetarien only : 0 -> False, 1 -> True (optional)
}
query_result = Marmiton.search(query_options)

# Get :
recipe = query_result[0]
print(recipe)
main_recipe_url = recipe['url']
print(main_recipe_url)
detailed_recipe = Marmiton.get(main_recipe_url)  # Get the details of the first returned recipe (most relevant in our case)

# Display result :
print("## %s\n" % detailed_recipe['name'])  # Name of the recipe
print("Recette par '%s'" % (detailed_recipe['author']))
print("Noté %s/5 par %s personnes." % (detailed_recipe['rate'], detailed_recipe['nb_comments']))
print("Temps de cuisson : %s / Temps de préparation : %s / Temps total : %s." % (detailed_recipe['cook_time'] if detailed_recipe['cook_time'] else 'N/A',detailed_recipe['prep_time'], detailed_recipe['total_time']))
print("Difficulté : '%s'" % detailed_recipe['difficulty'])
print("Budget : '%s'" % detailed_recipe['budget'])

print("\nRecette pour %s :\n" % detailed_recipe['recipe_quantity'])

for ingredient in detailed_recipe['ingredients']:  # List of ingredients
  print("ingrédient: %s quantité: %s unité: %s" % (ingredient['nom_ingredient'], ingredient['quantite'], ingredient['unite']))

print("")

for step in detailed_recipe['steps']:  # List of cooking steps
    print("# %s" % step)

if detailed_recipe['author_tip']:
	print("\nNote de l'auteur :\n%s" % detailed_recipe['author_tip'])
