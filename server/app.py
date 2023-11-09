#!/usr/bin/env python3
import json
import parse_ingredient

from flask import Flask, jsonify, request, session, make_response
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS

from models import db, User, Ingredient, Recipe, UserIngredient, SavedRecipe, RecipeIngredient

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)

migrate = Migrate(app, db)

db.init_app(app)

bcrypt = Bcrypt(app)


# HELPER METHODS #

def logged_in_user():
    return User.query.filter(User.id == session.get('user_id')).first()

def authorize():
    if not logged_in_user():
        return {'message': "No logged in user"}, 401


## ----- HOME PAGE ----- ##

@app.route("/")
def index():
    return "<h1>HOME PAGE</h1>"


## ----- USER CREATION, DELETION, LOGIN, & SESSION ----- ##

# USER SIGNUP #
@app.post('/users')
def create_user():
    try:
        data = request.json
        password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        new_user = User(
            username=data['username'],
            password=password_hash,
            first_name=data['first_name'],
            last_name=data['last_name']
        )
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.id
        return make_response( jsonify( new_user.to_dict() ), 201 )
    except Exception as e:
        return make_response( jsonify({ 'error': str(e) }), 406 )

# SESSION LOGIN #
@app.post('/login')
def login():
    data = request.json
    user = User.query.filter(User.username == data['username']).first()

    if user and bcrypt.check_password_hash(user.password, data['password']):
        session['user_id'] = user.id
        return make_response(jsonify(user.to_dict()), 202)
    else:
        return make_response( jsonify({ 'error': "Username and Password don't match any accounts" }), 401 )

# LOGOUT #
@app.delete('/logout')
def logout():
    session.pop('user_id')
    return make_response( jsonify({}), 204 )

# CHECK SESSION #
@app.get('/check_session')
def check_session():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        return make_response( jsonify( user.to_dict() ), 200 )
    else:
        return make_response( jsonify({}), 401 )

# DELETE ACCOUNT #
# @app.delete('/delete_account')
# def delete_account():
#     if logged_in_user():
#         user = logged_in_user()

#         for uf in user.user_followers:
#             db.session.delete(uf)

#         for uf in user.user_followees:
#             db.session.delete(uf)

#         for ui in user.user_ingredients:
#             db.session.delete(ui)

#         for rp in user.recipe_posts:
#              db.session.delete(rp)

#         for ur in user.user_recipes:
#             db.session.delete(ur)

#         for sr in user.saved_recipes:
#             db.session.delete(sr)

#         db.session.delete(user)
#         db.session.commit()
#         session.pop('user_id')
#         return make_response( jsonify({}), 204 )
#     else:
#         return make_response( jsonify({ 'error': 'User not found' }), 404 )


## ----- USER ROUTES ----- ##

# GET ALL USERS #
@app.get('/users')
def get_users_all():
    try:
        users = User.query.all()
        users_list = [user.to_dict() for user in users]
        return make_response( jsonify( users_list ), 200 )
    except AttributeError:
        return make_response( jsonify({ 'error': '404 users not found' }), 404 )

# GET USER BY ID #
@app.get('/users/<int:id>')
def get_user_by_id(id:int):
    try:
        user = User.query.filter(User.id == id).first()
        return make_response( jsonify( user.to_dict() ), 200 )
    except AttributeError:
        return make_response( jsonify({ 'error': f'404 user-{id} not found' }), 404 )


## ----- INGREDIENT ROUTES ----- ##

# GET ALL INGRREDIENTS
@app.get('/ingredients')
def get_ingredients_all():
    try:
        ingredients = Ingredient.query.all()
        ingredients_list = [ingredient.to_dict() for ingredient in ingredients]
        return make_response( jsonify( ingredients_list ), 200 )
    except AttributeError:
        return make_response( jsonify({ 'error': '404 ingredients not found' }), 404 )

# GET INGREDIENT BY ID #
@app.get('/ingredients/<int:id>')
def get_ingredient_by_id(id:int):
    try:
        ingredient = Ingredient.query.filter(Ingredient.id == id).first()
        return make_response( jsonify( ingredient.to_dict() ), 200 )
    except AttributeError:
        return make_response( jsonify({ 'error': f'404 ingredient-{id} not found' }), 404 )


## ----- RECIPE ROUTES ----- ##

# GET ALL RECIPES
@app.get('/recipes')
def get_recipes_all():
    # try:
    recipes = Recipe.query.all()
    recipes_list = [recipe.to_dict() for recipe in recipes]
    return make_response( jsonify( recipes_list ), 200 )
    # except AttributeError:
    #     return make_response( jsonify({ 'error': '404 recipes not found' }), 404 )

# GET RECIPE BY ID #
@app.get('/recipes/<int:id>')
def get_recipe_by_id(id:int):
    try:
        recipe = Recipe.query.filter(Recipe.id == id).first()
        return make_response( jsonify( recipe.to_dict() ), 200 )
    except AttributeError:
        return make_response( jsonify({ 'error': f'404 recipe-{id} not found' }), 404 )

# POST A RECIPE #
@app.post('/recipes')
def submit_recipe():
    try:
        recipe_data = request.json
        new_recipe = Recipe(**recipe_data)
        db.session.add(new_recipe)
        session['most_recent_recipe_id'] = new_recipe.id
        db.session.commit()
        return make_response( jsonify( new_recipe.to_dict() ), 201 )
    except Exception as e:
       return make_response ( jsonify({ 'error': str(e) }), 406 )


# ## ----- USER_FOLLOWS ROUTES ----- ##

# # GET ALL USER_FOLLOWS #
# @app.get('/user_follows')
# def get_user_follows_all():
#     try:
#         user_follows = UserFollow.query.all()
#         user_follows_list = [user_follow.to_dict() for user_follow in user_follows]
#         return make_response( jsonify( user_follows_list ), 200 )
#     except AttributeError:
#         return make_response( jsonify({ 'error': '404 user_follows not found' }), 404 )

# # GET USER_FOLLOW BY FOLLOWER_ID AND FOLLOWEE_ID #
# @app.get('/user_follows/<int:follower_id>/<int:followee_id>')
# def get_user_follow_by_follower_followee_id(follower_id:int, followee_id):
#     try:
#         user_follow = UserFollow.query.filter(UserFollow.follower_id == follower_id and UserFollow.followee_id == followee_id).first()
#         return make_response( jsonify( user_follow.to_dict() ), 200 )
#     except AttributeError:
#         return make_response ( jsonify({ 'error': f'404 user_follow-{follower_id}-{followee_id} not found' }), 404 )

# # FOLLOW ANOTHER USER #
# @app.post('/user_follows')
# def follow_user():
# 	try:
# 		user_follow_data = request.json
# 		new_user_follow = UserFollow(
#             follower_id=user_follow_data['follower_id'],
#             followee_id=user_follow_data['followee_id']
#         )
# 		db.session.add(new_user_follow)
# 		db.session.commit()
# 		return make_response( jsonify( new_user_follow.to_dict() ), 201 )
# 	except Exception as e:
# 		return make_response ( jsonify({ 'error': str(e) }), 406 )

# # UNFOLLOW ANOTHER USER #
# @app.delete('/user_follows/<int:follower_id>/<int:followee_id>')
# def unfollow_user(follower_id:int, followee_id:int):
# 	try:
# 		user_follow = UserFollow.query.filter(follower_id=follower_id, followee_id=followee_id).first()
# 		db.session.delete(user_follow)
# 		db.session.commit()
# 		return make_response( jsonify({}), 204 )
# 	except Exception as e:
# 		return make_response ( jsonify({ 'error': str(e) }), 406 )


## ----- USER_INGREDIENT ROUTES ----- ##

# GET ALL USER_INGREDIENTS #
@app.get('/user_ingredients')
def get_user_ingredients_all():
    try:
        user_ingredients = UserIngredient.query.all()
        user_ingredients_list = [user_ingredient.to_dict() for user_ingredient in user_ingredients]
        return make_response(jsonify(user_ingredients_list), 200)
    except AttributeError:
        return make_response( jsonify({ 'error': '404 user_ingredients not found' }), 404 )

# GET USER_INGREDIENT BY ID #
@app.get('/user_ingredients/<int:id>')
def get_user_ingredient_by_id(id:int):
    try:
        user_ingredient = UserIngredient.query.filter(UserIngredient.id == id).first()
        return make_response( jsonify( user_ingredient.to_dict() ), 200) 
    except AttributeError:
        return make_response( jsonify({ 'error': f'404 user-{id} not found' }), 404 )


## ----- USER_RECIPE ROUTES ----- ##

# GET ALL USER_RECIPES #
# @app.get('/user_recipes')
# def get_user_recipes_all():
#     try:
#         user_recipes = UserRecipe.query.all()
#         user_recipes_list = [user_recipe.to_dict() for user_recipe in user_recipes]
#         return make_response( jsonify( user_recipes_list ), 200 )
#     except AttributeError:
#         return make_response( jsonify({ 'error': '404 user_recipes not found' }), 404 )

# # GET USER_RECIPE BY ID #
# @app.get('/user_recipes/<int:id>')
# def get_user_recipe_by_id(id:int):
#     try:
#         user_recipe = UserRecipe.query.filter(UserRecipe.id == id).first()
#         return make_response( jsonify( user_recipe.to_dict() ), 200 )
#     except AttributeError:
#         return make_response( jsonify({ 'error': f'404 user_recipe-{id} not found' }), 404 )


## ----- SAVED_RECIPES ROUTES ----- ##

# GET ALL SAVED_RECIPES #
@app.get('/saved_recipes')
def get_saved_recipes_all():
    try:
        saved_recipes = SavedRecipe.query.all()
        saved_recipes_list = [saved_recipe.to_dict() for saved_recipe in saved_recipes]
        return make_response( jsonify( saved_recipes_list ), 200 )
    except AttributeError:
        return make_response( jsonify({ 'error': '404 saved_recipes not found' }), 404 )

# GET SAVED_RECIPE BY ID #
@app.get('/saved_recipes/<int:id>')
def get_saved_recipe_by_id(id:int):
    try:
        saved_recipe = SavedRecipe.query.filter(SavedRecipe.id == id).first()
        return make_response( jsonify( saved_recipe.to_dict() ), 200 )
    except AttributeError:
        return make_response( jsonify({ 'error': f'404 user_recipe-{id} not found' }), 404 )

# GET SAVED_RECIPE BY USER_ID AND RECIPE_ID #
@app.get('/saved_recipes/<int:user_id>/<int:recipe_id>')
def get_saved_recipe_by_user_recipe_id(user_id:int, recipe_id:int):
    try:
        saved_recipe = SavedRecipe.query.filter(SavedRecipe.user_id == user_id and SavedRecipe.recipe_id == recipe_id).first()
        return make_response( jsonify( saved_recipe.to_dict() ), 200 )
    except AttributeError:
        return make_response( jsonify({ 'error': f'404 saved_recipe-{id} not found' }), 404 )

# SAVE A RECIPE #
@app.post('/saved_recipes')
def save_recipe():
	try:
		recipe_data = request.json
		new_saved_recipe = SavedRecipe(
            user_id=session.get('user_id'),
            recipe_id=recipe_data['id']
        )
		db.session.add(new_saved_recipe)
		db.session.commit()
		return make_response( jsonify( new_saved_recipe.to_dict() ), 201 )
	except Exception as e:
		return make_response( jsonify({ 'error': str(e) }), 406 )

# USAVE A RECIPE #
@app.delete('/saved_recipes/<int:user_id>/<int:recipe_id>')
def unsave_recipe(user_id:int, recipe_id:int):
	try:
		saved_recipe = SavedRecipe.query.filter(SavedRecipe.user_id == user_id and SavedRecipe.recipe_id == recipe_id).first()
		db.session.delete(saved_recipe)
		db.session.commit()
		return make_response( jsonify({}), 204 )
	except Exception as e:
		return make_response ( jsonify({ 'error': str(e) }), 406 )


## ----- RECIPE_INGREDIENTS ROUTES ----- ##

# GET ALL RECIPE_INGREDIENTS #
@app.get('/recipe_ingredients')
def get_recipe_ingredients_all():
    try:
        recipe_ingredients = RecipeIngredient.query.all()
        recipe_ingredients_list = [recipe_ingredient.to_dict() for recipe_ingredient in recipe_ingredients]
        return make_response(jsonify(recipe_ingredients_list), 200)
    except AttributeError:
        return make_response( jsonify({ 'error': '404 recipe_ingredients not found' }), 404 )

# GET RECIPE_INGREDIENT BY ID #
@app.get('/recipe_ingredients/<int:id>')
def get_recipe_ingredient_by_id(id:int):
    try:
        recipe_ingredient = RecipeIngredient.query.filter(RecipeIngredient.id == id).first()
        return make_response( jsonify( recipe_ingredient.to_dict() ), 200 )
    except AttributeError:
        return make_response( jsonify({ 'error': f'404 recipe_ingredient-{id} not found' }), 404 )

@app.post('/recipe_ingredients')
def add_recipe_ingredient():
    try:
        data = request.json
        raw_ingredients_string = data['ingredients_string']
        raw_ingredients_list = raw_ingredients_string.split(', ')
        ingredient_dict_list = []
        for ingredient in raw_ingredients_list:
            ingr = parse_ingredient.parse(ingredient)
            ingredient_dict = json.dumps(ingr.as_dict())
            i = Ingredient.query.filter(Ingredient.fdc_id == ingredient_dict['ingedientParsed']['usdaInfo']['fdcId'])
            new_recipe_ingredient = RecipeIngredient(
                recipe_id=session.get('most_recent_recipe_id'),
                ingredient_id=i.id,
                raw_string=ingredient_dict['ingredientRaw'],
                quantity=ingredient_dict['ingedientParsed']['quantity'],
                unit=ingredient_dict['ingedientParsed']['unit'],
                product_size_modifier=ingredient_dict['ingedientParsed']['product_size_modifier'],
                product=ingredient_dict['ingedientParsed']['product'],
                preparation_notes=ingredient_dict['ingedientParsed']['preparationNotes'],
                confidence=ingredient_dict['confidence']
            )
            ingredient_dict_list.append(new_recipe_ingredient)
            db.session.add(new_recipe_ingredient)
        db.session.commit()
        return make_response([ri.to_dict for ri in ingredient_dict_list], 201)
    except AttributeError:
        pass


## ----- RUN MAIN ----- ##

if __name__ == "__main__":
    app.run(port=5555, debug=True)