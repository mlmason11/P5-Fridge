#!/usr/bin/env python3

from faker import Faker
from faker.providers.date_time import Provider as DatetimeProvider
from faker.providers.lorem import Provider as IpsumLoremProvider
from faker_food import FoodProvider
from random import choice as rc
from random import uniform as randunif
from random import randint

from app import app
from models import db, User, Ingredient, Recipe, RecipePost, UserIngredient, SavedRecipe, RecipeIngredient

fake = Faker()
fake.add_provider(FoodProvider)
fake.add_provider(DatetimeProvider)
fake.add_provider(IpsumLoremProvider)

def create_users(rows):
    users = []
    for _ in range(rows):
        user = User(
            username = fake.email(),
            password = fake.address(),
            first_name = fake.first_name(),
            last_name = fake.last_name(),
        )
        users.append(user)
    return users

def create_ingredients(rows):
    ingredients = []
    for _ in range(rows):
        ingredient = Ingredient(
            name = fake.ingredient(),
            category = rc(['Vegetable', 'Fruit', 'Grain', 'Protein', 'Dairy', 'Fat/Oil', 'Added Sugar', 'Beverage']),
            exp_date = fake.future_date(),
            img_url = fake.address(),
            is_perishable = rc([True, False]),
            priority = rc(['High', 'Medium', 'Low']),
            storage_status = rc(['Freezer', 'Refrigerator', 'Pantry']),
            storage_instructions = fake.email(),
            usage_instructions = fake.country()
        )
        ingredients.append(ingredient)
    return ingredients

def create_recipes(rows):
    recipes = []
    for _ in range(rows):
        recipe = Recipe(
            name = fake.dish(),
            description = fake.dish_description(),
            cuisine = fake.ethnic_category(),
            prep_time = randint(5, 60),
            cook_time = randint(5, 60),
            rating = round(randunif(0, 5), 2),
            exp_date = fake.future_date(),
            img_url = fake.address(),
            is_perishable = rc([True, False]),
            priority = rc(['High', 'Medium', 'Low']),
            storage_status = rc(['Freezer', 'Refrigerator', 'Pantry']),
            storage_instructions = fake.email(),
            usage_instructions = fake.country(),
            reheat_instructions = fake.company()
        )
        recipes.append(recipe)
    return recipes

# def create_user_follows(rows, users):
#     user_follows = []
#     for _ in range(rows):
#         follower = rc(users)
#         followee = rc(users)
#         uf = UserFollow(
#             follower_id = follower.id,
#             followee_id = followee.id
#         )
#         user_ingredients.append(uf)
#     return user_follows

def create_user_ingredients(rows, users, ingredients):
    user_ingredients = []
    for _ in range(rows):
        user = rc(users)
        ingredient = rc(ingredients)
        ui = UserIngredient(
            user_id = user.id,
            ingredient_id = ingredient.id,
            quantity = randint(0, 20)
        )
        user_ingredients.append(ui)
    return user_ingredients

def create_recipe_posts(rows, users, recipes):
    recipe_posts = []
    for _ in range(rows):
        user = rc(users)
        recipe = rc(recipes)
        rp = RecipePost(
            user_id=user.id,
            recipe_id=recipe.id
        )
        recipe_posts.append(rp)
    return recipe_posts

def create_saved_recipes(rows, users, recipes):
    saved_recipes = []
    for _ in range(rows):
        user = rc(users)
        recipe = rc(recipes)
        sr = SavedRecipe(
            user_id = user.id,
            recipe_id = recipe.id,
        )
        saved_recipes.append(sr)
    return saved_recipes

def create_recipe_ingredients(rows, recipes, ingredients):
    recipe_ingredients = []
    for _ in range(rows):
        recipe = rc(recipes)
        ingredient = rc(ingredients)
        ri = RecipeIngredient(
            recipe_id = recipe.id,
            ingredient_id = ingredient.id
        )
        recipe_ingredients.append(ri)
    return recipe_ingredients

if __name__ == '__main__':

    with app.app_context():
        print ('Clearing database ...')
        User.query.delete()
        Ingredient.query.delete()
        Recipe.query.delete()
        UserIngredient.query.delete()
        SavedRecipe.query.delete()
        RecipeIngredient.query.delete()

        print('Seeding users ...')
        users = create_users(10)
        db.session.add_all(users)
        db.session.commit()

        print('Seeding ingredients ...')
        ingredients = create_ingredients(15)
        db.session.add_all(ingredients)
        db.session.commit()

        print('Seeding recipes ...')
        recipes = create_recipes(5)
        db.session.add_all(recipes)
        db.session.commit()

        # print('Seeding user_follows ...')
        # user_follows = create_user_follows(20, users)
        # db.session.add_all(user_follows)
        # db.session.commit()

        print('Seeding user_ingredients ...')
        user_ingredients = create_user_ingredients(20, users, ingredients)
        db.session.add_all(user_ingredients)
        db.session.commit()

        print('Seeding saved_recipes ...')
        saved_recipes = create_saved_recipes(20, users, recipes)
        db.session.add_all(saved_recipes)
        db.session.commit()

        print('Seeding recipe_ingredients ...')
        recipe_ingredients = create_recipe_ingredients(20, recipes, ingredients)
        db.session.add_all(recipe_ingredients)
        db.session.commit()

        print('Done seeding !!!')
