# -*- coding: utf-8 -*-
# base de l'api : 	'https://github.com/remaudcorentin-dev/python-marmiton', author='Corentin Remaud'

from bs4 import BeautifulSoup

import urllib.parse
import urllib.request

import re
import ssl


class RecipeNotFound(Exception):
	pass


class Marmiton(object):

	@staticmethod
	def search(query_dict):
		"""
		Search recipes parsing the returned html data.
		Options:
		'aqt': string of keywords separated by a white space  (query search)
		Optional options :
		'dt': "entree" | "platprincipal" | "accompagnement" | "amusegueule" | "sauce"  (plate type)
		'exp': 1 | 2 | 3  (plate expense 1: cheap, 3: expensive)
		'dif': 1 | 2 | 3 | 4  (recipe difficultie 1: easy, 4: advanced)
		'veg': 0 | 1  (vegetarien only: 1)
		'rct': 0 | 1  (without cook: 1)
		'sort': "markdesc" (rate) | "popularitydesc" (popularity) | "" (empty for relevance)
		"""
		base_url = "https://www.marmiton.org/recettes/recherche.aspx?"
		query_url = urllib.parse.urlencode(query_dict)
		url = base_url + query_url
		handler = urllib.request.HTTPSHandler(context=ssl._create_unverified_context())
		opener = urllib.request.build_opener(handler)
		response = opener.open(url)
		html_content = response.read()

		soup = BeautifulSoup(html_content, 'html.parser')

		search_data = []

		articles = soup.findAll("a", href=True)
		articles = [a for a in articles if a["href"].startswith("https://www.marmiton.org/recettes/recette_")]
		iterarticles = iter(articles)
		for article in iterarticles:
			data = {}
			try:
				data["name"] = article.find("h4").get_text().strip(' \t\n\r')
				data["url"] = article['href']
				try:
					data["rate"] = article.find("span").get_text().split("/")[0]
				except Exception as e0:
					pass
				try:
					data["image"] = article.find('img')['data-src']
				except Exception as e1:
					try:
						data["image"] = article.find('img')['src']
					except Exception as e1:
						pass
					pass
			except Exception as e2:
				pass
			if data:
				search_data.append(data)

		return search_data

	@staticmethod
	def _get_name(soup):
		return soup.find("h1").get_text().strip(' \t\n\r')

	@staticmethod
	def _get_ingredients(soup):
		# Extraire les valeurs des ingrédients
		ingredient_names = soup.find_all('span', class_='ingredient-name')
		ingredient_quantities = soup.find_all('span', class_='card-ingredient-quantity')

		# # Boucle pour récupérer et afficher tous les noms et quantités d'ingrédients
		# for ingredient_name, ingredient_quantity in zip(ingredient_names, ingredient_quantities):
		# 	produit = ingredient_name.get_text().strip(' \t\n\r').replace("\xa0", " ")
		# 	quantity = ingredient_quantity.get_text(strip=True)
		# 	# Ajouter un espace entre le nombre et le texte
		# 	quantity = re.sub(r'(\d)([^\d\s])', r'\1 \2', quantity)
		# 	print(f"{quantity} {produit}")

		ingredients = []
		for ingredient_name, ingredient_quantity in zip(ingredient_names, ingredient_quantities):
			produit = ingredient_name.get_text().strip(' \t\n\r').replace("\xa0", " ")
			quantity = ingredient_quantity.get_text(strip=True)
			# Ajouter un espace entre le nombre et le texte, en considérant le point comme numérique
			quantity = re.sub(r'(\d)([^\d\s.])', r'\1 \2', quantity)
			# Séparer la quantité et l'unité
			parts = quantity.split(' ', 1)
			quantite = parts[0]
			unite = parts[1] if len(parts) > 1 else ""  # L'unité est la valeur en texte contenue dans quantity
			ingredients.append({
				"quantite": quantite,
				"unite": unite,
				"nom_ingredient": produit
			})
		return ingredients
		
	@staticmethod
	def _get_author(soup):
		return soup.find("div", text="Note de l'auteur :").parent.parent.findAll("div")[0].findAll("div")[1].get_text()

	@staticmethod
	def _get_author_tip(soup):
		return soup.find("div", text="Note de l'auteur :").parent.parent.findAll("div")[3].find_all("div")[1].get_text().replace("\xa0", " ").replace("\r\n", " ").replace("  ", " ").replace("« ", "").replace(" »", "")

	@staticmethod
	def _get_steps(soup):
		return [step.parent.parent.find("p").get_text().strip(' \t\n\r') for step in soup.find_all("h3", text=re.compile("^Étape"))]

	@staticmethod
	def _get_images(soup):
		return [img.get("data-src") for img in soup.find_all("img", {"height": 150}) if img.get("data-src")]

	@staticmethod
	def _get_rate(soup):
		chemin_css = "html.no-js body.body-domuser-fr div#content.marmiton div.recipeV2-container div.mrtn-content div.recipe-header__title div.recipe-header__rating-container div.recipe-header__rating a.recipe-header__rating-stars span.recipe-header__rating-text"
		return soup.select(chemin_css)[0].get_text().split("/")[0]

	@staticmethod
	def _get_nb_comments(soup):
		return soup.find("h1").parent.next_sibling.find_all("span")[1].get_text().split(" ")[0]

	@staticmethod
	def _get_total_time__difficulty__budget(soup):
		svg_data = "M13.207 22.759a2.151 2.151 0 1 0 0 4.302 2.151 2.151 0 0 0 0-4.302z"
		return soup.find("path", {"d": svg_data}).parent.parent.parent.get_text().split("•")

	@classmethod
	def _get_total_time(cls, soup):
		return cls._get_total_time__difficulty__budget(soup)[0].replace("\xa0", " ")

	@classmethod
	def _get_difficulty(cls, soup):
		return cls._get_total_time__difficulty__budget(soup)[1]

	@classmethod
	def _get_budget(cls, soup):
		return cls._get_total_time__difficulty__budget(soup)[2]

	@staticmethod
	def _get_cook_time(soup):
		return soup.find_all(text=re.compile("Cuisson"))[0].parent.next_sibling.next_sibling.get_text()

	@staticmethod
	def _get_prep_time(soup):
		return soup.find_all(text=re.compile("Préparation"))[1].parent.next_sibling.next_sibling.get_text().replace("\xa0", " ")

	@staticmethod
	def _get_recipe_quantity(soup):
		servings_info = soup.find('div', class_='mrtn-recette_ingredients-counter')
		servings_nb = servings_info['data-servingsnb']
		servings_unit = servings_info['data-servingsunit']
		return f"{servings_nb} {servings_unit}"
	

	@classmethod
	def get(cls, url):
		"""
		'url' from 'search' method.
		 ex. "/recettes/recette_wraps-de-poulet-et-sauce-au-curry_337319.aspx"
		"""

		#base_url = "https://www.marmiton.org"
		#url = base_url + ("" if uri.startswith("/") else "/") + uri
		#url = uri
		try:
			handler = urllib.request.HTTPSHandler(context=ssl._create_unverified_context())
			opener = urllib.request.build_opener(handler)
			response = opener.open(url)
			html_content = response.read()
		except urllib.error.HTTPError as e:
			raise RecipeNotFound if e.code == 404 else e

		soup = BeautifulSoup(html_content, 'html.parser')

		elements = [
			{"name": "name", "default_value": ""},
			{"name": "ingredients", "default_value": []},
			{"name": "author", "default_value": "Anonyme"},
			{"name": "author_tip", "default_value": ""},
			{"name": "steps", "default_value": []},
			{"name": "images", "default_value": []},
			{"name": "rate", "default_value": ""},
			{"name": "difficulty", "default_value": ""},
			{"name": "budget", "default_value": ""},
			{"name": "cook_time", "default_value": ""},
			{"name": "prep_time", "default_value": ""},
			{"name": "total_time", "default_value": ""},
			{"name": "recipe_quantity", "default_value": ""},
			{"name": "nb_comments", "default_value": 0},
		]

		data = {"url": url}
		for element in elements:
			try:
				data[element["name"]] = getattr(cls, "_get_" + element["name"])(soup)
			except:
				data[element["name"]] = element["default_value"]

		return data

