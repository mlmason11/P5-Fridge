from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
# from string import ascii_lowercase, ascii_uppercase, digits, punctuation


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})


db = SQLAlchemy(metadata=metadata)


class User(db.Model):

	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String, nullable=False, unique=True)
	password = db.Column(db.String)
	first_name = db.Column(db.String, nullable=False)
	last_name = db.Column(db.String, nullable=False)

	# Relationships #

	# Other users that follow this user. Followers are of class User here.
	# follower_users = db.relationship('UserFollow', back_populates='followee')
	# followers = association_proxy('user_followers', 'followee')

	# Other users that this users is following. Followers are of class User here.
	# followee_users = db.relationship('UserFollow', back_populates='follower')
	# followees = association_proxy('user_followers', 'follower')

	# To denote all ingredients at the users disposal. Ingredients are of class Ingredient here.
	user_ingredients = db.relationship('UserIngredient', back_populates='user')
	ingredients = association_proxy('user_ingredients', 'ingredient')

	# To denote the recipes that the user has authored.
	# Posts are of class Recipe here.
	# recipe_posts = db.relationship('RecipePost', back_populates='user')
	# posts = association_proxy('recipe_posts', 'recipe')

	# To denote the possible recipes the user can make with the items at their disposal.
	# Recipes are of class Recipe here.
	recipes = db.relationship('Recipe', back_populates='author')

	# To allow users to save recipes for future reference.
	# Saves are of class Recipe here.
	saved_recipes = db.relationship('SavedRecipe', back_populates='user')
	saves = association_proxy('saved_recipes', 'recipe')

	# Serialization with lists
	def to_dict(self):
		return {
			'id': self.id,
			'username': self.username,
			'first_name': self.first_name,
			'last_name': self.last_name,
			'ingredients': [ingredient.to_dict_no_lists() for ingredient in self.ingredients],
			'recipes': [recipe.to_dict_no_lists() for recipe in self.recipes],
			'saves': [save.to_dict_no_lists() for save in self.saves]
		}

	# Serialization no lists
	def to_dict_no_lists(self):
		return {
			'id': self.id,
			'username': self.username,
			'first_name': self.first_name,
			'last_name': self.last_name
		}



class Ingredient(db.Model):

	__tablename__ = 'ingredients'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False, unique=True)
	category = db.Column(db.String)
	description = db.Column(db.String)
	fdc_id = db.Column(db.Integer)
	match_method = db.Column(db.String)
	img_url = db.Column(db.String)
	is_perishable = db.Column(db.Boolean)
	keeps_for = db.Column(db.String)
	storage_instructions = db.Column(db.String)
	usage_instructions = db.Column(db.String)

	# Relationships

	# To denote all ingredients at the users disposal.
	user_ingredients = db.relationship('UserIngredient', back_populates='ingredient')
	users = association_proxy('user_ingredients', 'user')

	# To obtain the list of all recipes that call for this ingredient for each ingredient.
	recipe_ingredients = db.relationship('RecipeIngredient', back_populates='ingredient')
	recipes = association_proxy('recipe_ingredients', 'recipe')

	# Serialization with lists
	def to_dict(self):
		return {
			'id': self.id,
			'name': self.name,
			'category': self.category,
			'description': self.description,
			'fdc_id': self.fdc_id,
			'match_method': self.match_method,
			'img_url': self.img_url,
			'is_perishable': self.is_perishable,
			'keeps_for': self.keeps_for,
			'storage_instructions': self.storage_instructions,
			'usage_instructions': self.usage_instructions,
			'users': [user.to_dict_no_lists() for user in self.users],
			'recipes': [recipe.to_dict_no_lists() for recipe in self.recipes]
		}

	# Serialization no lists
	def to_dict_no_lists(self):
		return {
			'id': self.id,
			'name': self.name,
			'category': self.category,
			'description': self.description,
			'fdc_id': self.fdc_id,
			'match_method': self.match_method,
			'img_url': self.img_url,
			'is_perishable': self.is_perishable,
			'keeps_for': self.keeps_for,
			'storage_instructions': self.storage_instructions,
			'usage_instructions': self.usage_instructions
		}


class Recipe(db.Model):

	__tablename__ = 'recipes'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False, unique=True)
	author_id = db.Column(db.String, db.ForeignKey('users.id'))
	description = db.Column(db.String)
	cuisine = db.Column(db.String)
	prep_time = db.Column(db.Integer)
	cook_time = db.Column(db.Integer)
	servings = db.Column(db.Integer)
	img_url = db.Column(db.String)
	keeps_for = db.Column(db.String)
	storage_instructions = db.Column(db.String)
	usage_instructions = db.Column(db.String)
	cook_instructions = db.Column(db.String)
	reheat_instructions = db.Column(db.String)
	ingredients_string = db.Column(db.String)
	rating = db.Column(db.Float, default=0)

	## Relationships ##

	# To denote the author of the recipe. The author is of class User.
	author = db.relationship('User', back_populates='recipes')

	# To denote the possible recipes the user can make with the items at their disposal. Yes.
	# user_recipes = db.relationship('UserRecipe', back_populates='recipe')
	# users = association_proxy('user_recipes', 'user')

	# To allow users to save recipes for future reference. Saves are of class User here.
	saved_recipes = db.relationship('SavedRecipe', back_populates='recipe')
	saves = association_proxy('saved_recipes', 'user')

	# To obtain the list of all ingredients in this recipe for each recipe. Yes.
	recipe_ingredients = db.relationship('RecipeIngredient', back_populates='recipe')

	# Serialization with lists
	def to_dict(self):
		return {
			'id': self.id,
			'name': self.name,
			'author_id': self.author_id,
			'description': self.description,
			'cuisine': self.cuisine,
			'prep_time': self.prep_time,
			'cook_time': self.cook_time,
			'img_url': self.img_url,
			'keeps_for': self.keeps_for,
			'storage_instructions': self.storage_instructions,
			'usage_instructions': self.usage_instructions,
			'cook_instructions': self.cook_instructions,
			'reheat_instructions': self.reheat_instructions,
			'ingredients_string': self.ingredients_string,
			'rating': self.rating,
			'saves': [save.to_dict_no_lists() for save in self.saves],
		}

	# Serialization no lists
	def to_dict_no_lists(self):
		return {
			'id': self.id,
			'name': self.name,
			'author_id': self.author_id,
			'description': self.description,
			'cuisine': self.cuisine,
			'prep_time': self.prep_time,
			'cook_time': self.cook_time,
			'img_url': self.img_url,
			'keeps_for': self.keeps_for,
			'storage_instructions': self.storage_instructions,
			'usage_instructions': self.usage_instructions,
			'cook_instructions': self.cook_instructions,
			'reheat_instructions': self.reheat_instructions,
			'rating': self.rating
		}


# User - Ingredient
# To denote all ingredients at each users disposal.
class UserIngredient(db.Model):

	__tablename__ = 'user_ingredients'

	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	quantity = db.Column(db.Integer)
	fdc_id = db.Column(db.Integer)
	data_type = db.Column(db.String)
	brand_owner = db.Column(db.String)
	brand_name = db.Column(db.String)
	ingredients = db.Column(db.String)
	food_category = db.Column(db.String)
	description = db.Column(db.String)
	package_weight = db.Column(db.String)
	serving_size_unit = db.Column(db.String)
	serving_size = db.Column(db.Float)
	img_url = db.Column(db.String)
	is_perishable = db.Column(db.Boolean)
	keeps_for = db.Column(db.String)
	storage_instructions = db.Column(db.String)
	usage_instructions = db.Column(db.String)
	priority = db.Column(db.String)
	storage_status = db.Column(db.String)

	user = db.relationship('User', back_populates='user_ingredients')

	# Serialization
	def to_dict(self):
		return {
			'id': self.id,
			'user_id': self.user_id,
			'fdc_id': self.fdc_id,
			'data_type': self.data_type,
			'brand_owner': self.brand_owner,
			'brand_name': self.brand_name,
			'ingredients': self.ingredients,
			'food_category': self.food_category,
			'description': self.description,
			'package_weight': self.package_weight,
			'serving_size_unit': self.serving_size_unit,
			'serving_size': self.serving_size,
			'img_url': self.img_url,
			'is_perishable': self.is_perishable,
			'keeps_for': self.keeps_for,
			'storage_instructions': self.storage_instructions,
			'quantity': self.quantity,
			'priority': self.priority,
			'storage_status': self.storage_status,
			'user': self.user.to_dict_no_lists()
		}


# User - Recipe
# To denote the recipes the users have at their disposal.
# class UserRecipe(db.Model):

# 	__tablename__ = 'user_recipes'

# 	id = db.Column(db.Integer, primary_key=True)
# 	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
# 	recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
# 	quantity = db.Column(db.Integer)
# 	priority = db.Column(db.String)
# 	storage_status = db.Column(db.String)

# 	user = db.relationship('User', back_populates='user_recipes')
# 	recipe = db.relationship('Recipe', back_populates='user_recipes')

# 	# Serialization
# 	def to_dict(self):
# 		return {
# 			'id': self.id,
# 			'user_id': self.user_id,
# 			'recipe_id': self.recipe_id,
# 			'quantity': self.quantity,
# 			'storage_status': self.storage_status,
# 			'user': self.user.to_dict_no_lists(),
# 			'recipe': self.recipe.to_dict_no_lists()
# 		}


# User - Recipe
# To allow users to save recipes for future reference.
class SavedRecipe(db.Model):

	__tablename__ = 'saved_recipes'

	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))

	user = db.relationship('User', back_populates='saved_recipes')
	recipe = db.relationship('Recipe', back_populates='saved_recipes')

	# Serialization
	def to_dict(self):
		return {
			'id': self.id,
			'user_id': self.user_id,
			'recipe_id': self.recipe_id,
			'rating': self.rating,
			'user': self.user.to_dict_no_lists(),
			'recipe': self.recipe.to_dict_no_lists()
		}


# Recipe - Ingredient
# To map all recipes in our database to their respective ingredients, and vice versa.
class RecipeIngredient(db.Model, SerializerMixin):

	__tablename__ = 'recipe_ingredients'

	id = db.Column(db.Integer, primary_key=True)
	recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
	fdc_id = db.Column(db.Integer)
	raw_string = db.Column(db.String)
	quantity = db.Column(db.Integer)
	unit = db.Column(db.String)
	product_size_modifier = db.Column(db.String)
	product = db.Column(db.String)
	preparation_notes = db.Column(db.String)
	usda_category = db.Column(db.String)
	usda_description = db.Column(db.String)
	match_method = db.Column(db.String)
	confidence = db.Column(db.Float)
	error = db.Column(db.String)

	recipe = db.relationship('Recipe', back_populates='recipe_ingredients')

	# Serialization
	def to_dict(self):
		return {
			'id': self.id,
			'recipe_id': self.recipe_id,
			'fdc_id': self.ingredient_id,
			'raw_string': self.raw_string,
			'quantity': self.quantity,
			'unit': self.unit,
			'product_size_modifier': self.product_size_modifier,
			'product': self.product,
			'preparation_notes': self.preparation_notes,
			'usda_category': self.usda_category,
			'usda_description': self.usda_description,
			'match_method': self.match_method,
			'confidence': self.confidence,
			'error': self.error,
			'recipe': self.recipe.to_dict_no_lists()
		}

	def to_dict_no_lists(self):
		return {
			'id': self.id,
			'recipe_id': self.recipe_id,
			'fdc_id': self.ingredient_id,
			'raw_string': self.raw_string,
			'quantity': self.quantity,
			'unit': self.unit,
			'product_size_modifier': self.product_size_modifier,
			'product': self.product,
			'preparation_notes': self.preparation_notes,
			'usda_category': self.usda_category,
			'usda_description': self.usda_description,
			'match_method': self.match_method,
			'confidence': self.confidence,
			'error': self.error,
		}
