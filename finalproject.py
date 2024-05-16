#This code requires the libraries requests, pandas, and beautifulsoup4 to run


import re
import pandas as pd
from bs4 import BeautifulSoup
import requests

class Recipe:
    """
        This is a class that represents an e-recipe.

        attributes:
            name (str): The name of the recipe.
            ingredients (list): List of ingredients in the recipe.
            instructions (str): Instructions for the recipe.
            origin (str): Country of origin for the recipe.
            dietary_preferences (list): List of dietary preferences for the recipe.
            price_range (str): Price range of the recipe.
    """

    def __init__(self, name, ingredients, instructions, origin, dietary_preferences, price_range):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions
        self.origin = origin
        self.dietary_preferences = dietary_preferences
        self.price_range = price_range


    def display_of_details(self):
        """
            This will show the details of the recipe.
        """
        print("Recipe: {}".format(self.name))
        print("Ingredients: {}".format(', '.join(self.ingredients)))
        print("Instructions: {}".format(self.instructions))
        print("Origin: {}".format(self.origin))
        print("Dietary Preferences: {}".format(', '.join(self.dietary_preferences)))
        print("Price Range: {}".format(self.price_range))





def get_baking_recipes():
    """
    Web scrape baking recipes from the Tasty website.
    
    Returns:
        list: List of baking recipes.
    """
    url_link = 'https://tasty.co'
    response = requests.get(url_link)

    if response.status_code != 200:
        print("Failed to get the webpage.")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    recipe_cards = soup.find_all('div', class_='recipe-card')
    baking_keywords = re.compile(r'\bbake\b|\bbaking\b|\bbakes\b', re.IGNORECASE)

    recipes = []
    for recipe_card in recipe_cards:
        recipe_title = recipe_card.find('h3', class_='recipe-card__title').text
        recipe_description = recipe_card.find('p', class_='recipe-card__description').text

        if baking_keywords.search(recipe_title) or baking_keywords.search(recipe_description):
            recipes.append(Recipe(name=recipe_title, ingredients=[], instructions="", origin="", dietary_preferences=[], price_range=""))

    return recipes






def main():
    """
        This is the main function of the Recipe Book. Users can search for a recipe, save a recipe, apply filters, or exit.
    """
    recipes = get_baking_recipes() 
    recipes_dataframe = pd.DataFrame([{
        'name': recipe.name,
        'ingredients': recipe.ingredients,
        'instructions': recipe.instructions,
        'origin': recipe.origin,
        'dietary_preferences': recipe.dietary_preferences,
        'price_range': recipe.price_range
    } for recipe in recipes])

    print("Welcome to Ally's online Recipe Book!")
    while True:
        print("\n\tMenu:")
        print("1. Search for a recipe")
        print("2. Save a recipe to your recipe book")
        print("3. Filter recipe preferences")
        print("4. Exit")
        select = input("Enter your choice: ")
        if select == "1":
            search_query = input("Enter what you want to search: ")
            search_recipe(search_query, recipes_dataframe)
        elif select == "2":
            recipe_name = input("Enter the name of the recipe: ")
            save_recipe(recipe_name)
        elif select == "3":
            dietary_preference = input("Enter your dietary preference (leave blank for any): ")
            price_range = input("Enter your preferred price range (low, medium, high): ")
            country_of_origin = input("Enter the country of origin (leave blank for any): ")
            filtered_recipes = filter_recipes(dietary_preference, price_range, country_of_origin, recipes_dataframe)
            if filtered_recipes:
                print("Matching Recipes:")
                for recipe_name in filtered_recipes:
                    print(recipe_name)
            else:
                print("No recipes match your criteria.")
        elif select == "4":
            print("See you next time!")
            break
        else:
            print("Invalid choice. Please try again.")





def search_recipe(search_query, recipes_dataframe):
    """
        Search for recipes based on the search query.

        Args:
            search_query (str): The search query entered by the user.
            recipes_dataframe (dataframe): pandas dataframe containing recipe data.

        Returns:
            None
    """
    match = False
    print("Matching Recipes:")
    for index, recipe in recipes_dataframe.iterrows():
        if search_query.lower() in recipe['name'].lower():
            Recipe(**recipe).display_details()
            print()
            match = True
    
    if not match:
        print("No recipes found matching the search query.")




def filter_recipes(dietary_preference, price_range, country_origin, recipes_dataframe):
    """
        Filter recipes based on user preferences.

        args:
            dietary_preference (str): user's dietary preference.
            price_range (str): user's preferred price range.
            country_origin (str): user's preferred country of origin.
            recipes_dataframe (dataframe): pandas dataframe containing recipe data.

        returns:
            set: Set of recipe names matching the filtering criteria.
    """
    filtered_recipes = set()
    for index, recipe in recipes_dataframe.iterrows():
        if (not dietary_preference or dietary_preference in recipe['dietary_preferences']) and \
           (not price_range or price_range == recipe['price_range']) and \
           (not country_origin or country_origin == recipe['origin']):
            filtered_recipes.add(recipe['name'])
    return filtered_recipes





def save_recipe(recipe_name):
    """
        Save a recipe to the recipe book.

        args:
            recipe_name (str): The name of the recipe.

        returns:
            None
    """
    print("{} saved to your recipe book.".format(recipe_name))





if __name__ == "__main__":
    main()
