import csv
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from time import sleep

from models import db, Ingredient


options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", chrome_options=options)

page = driver.get('https://www.foodsafety.gov/keep-food-safe/foodkeeper-app')







# ingredients = soup.find_all('a', class_='f-safety-app-by-category-list-item')

# ingredient_list = []

# for a in ingredients:
# 	i = Ingredient(
# 		name=a.text,
# 		# category = rc(['Vegetable', 'Fruit', 'Grain', 'Protein', 'Dairy', 'Fat/Oil', 'Added Sugar', 'Beverage']),
# 		# exp_date = fake.future_date(),
# 		# img_url = fake.address(),
# 		# is_perishable = rc([True, False]),
# 		# priority = rc(['High', 'Medium', 'Low']),
# 		# storage_status = rc(['Freezer', 'Refrigerator', 'Pantry']),
# 		# storage_instructions = fake.email(),
# 		# usage_instructions = fake.country()
# 	)
# 	print(i.to_dict_no_lists())
# 	ingredient_list.append(i)

# 	return ingredient_list

# if __name__ == '__main__':
# 	with app.app_context():
# 		print('deleting ingredients data')
# 		Ingredient.query.delete()
# 		print('scraping ingredients from the website')
# 		ingredients = scrape_ingredients()
# 		print('adding ingredients to the database')
# 		db.session.add_all(ingredients)
# 		db.session.commit()
