from bs4 import BeautifulSoup
import urllib.request

from bs4 import BeautifulSoup
import requests
import re

url = "https://www.marmiton.org/recettes/recette_veritable-fondue-savoyarde_34077.aspx"

# Effectuer une requête GET pour récupérer le contenu de la page
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extraire les valeurs des ingrédients
ingredient_names = soup.find_all('span', class_='ingredient-name')
ingredient_quantities = soup.find_all('span', class_='card-ingredient-quantity')

# Boucle pour récupérer et afficher tous les noms et quantités d'ingrédients
for ingredient_name, ingredient_quantity in zip(ingredient_names, ingredient_quantities):
    produit = ingredient_name.get_text().strip(' \t\n\r').replace("\xa0", " ")
    quantity = ingredient_quantity.get_text(strip=True)
    # Ajouter un espace entre le nombre et le texte
    quantity = re.sub(r'(\d)([^\d\s])', r'\1 \2', quantity)
    print(f"{quantity} {produit}")
