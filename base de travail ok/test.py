from bs4 import BeautifulSoup
import urllib.request

from bs4 import BeautifulSoup
import requests
import re

url = "https://www.marmiton.org/recettes/recette_veritable-fondue-savoyarde_34077.aspx"

# Effectuer une requête GET pour récupérer le contenu de la page
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

#return [item.get_text().strip(' \t\n\r').replace("\xa0", " ") for item in soup.findAll("div", {"class": "MuiGrid-item"})]
chemin_css_intitule = "html.no-js body.body-domuser-fr div#content.marmiton div.recipeV2-container div.mrtn-content div.mrtn-recette_ingredients div.mrtn-recette_ingredients-content.no-show-more div.mrtn-recette_ingredients-items div.card-ingredient div.card-ingredient-content span.card-ingredient-link.af-to-obfuscate.af-to-obfuscate-83268 span.card-ingredient-title span.ingredient-name"
				# Extraire les valeurs des ingrédients
ingredient_names = soup.find_all('span', class_='ingredient-name')
# Boucle pour récupérer et afficher tous les noms d'ingrédients
for ingredient_name in ingredient_names:
    produit = ingredient_name.get_text().strip(' \t\n\r').replace("\xa0", " ")
    print(produit)


ingredient_quantities = soup.find_all('span', class_='card-ingredient-quantity')
		# Boucle pour récupérer et afficher toutes les quantités d'ingrédients
for ingredient_quantity, item in zip(ingredient_quantities, soup.select(chemin_css_intitule)):
    ingredient_quantity_text = ingredient_quantity.get_text(strip=True)
    # Ajouter un espace entre le nombre et le texte
    ingredient_quantity_text = re.sub(r'(\d)([^\d\s])', r'\1 \2', ingredient_quantity_text)
    produit = item.get_text().strip(' \t\n\r').replace("\xa0", " ")
   # print(f"{ingredient_quantity_text} {produit}")
    print(f"{ingredient_quantity_text} {produit}")
