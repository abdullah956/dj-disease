# from django.shortcuts import render
# from .models import ProductImage
# from django.core.files.storage import default_storage
# import pytesseract
# import cv2  
# import numpy as np
# from PIL import Image, ImageEnhance, ImageFilter, ImageOps
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# PRODUCTS_WITH_SUGAR = ['Oreo', 'Hershey', 'Starburst', 'Snickers',  'Butterfinger']

# def check_product(request):
#     if request.method == 'POST' and request.FILES['product_image']:
#         product_image = ProductImage(image=request.FILES['product_image'])
#         product_image.save()
#         image_path = default_storage.path(product_image.image.name)
#         product_name = extract_product_name(image_path)
#         print(product_name)
#         if product_name in PRODUCTS_WITH_SUGAR:
#             message = f"Warning: {product_name} contains sugar."
#         else:
#             message = f"{product_name} might not contain sugar."
#         return render(request, 'disease/result.html', {'message': message})
#     return render(request, 'disease/upload.html')

# def extract_product_name(image_path):
#     image = Image.open(image_path)
#     image = image.convert('L')
#     image = image.filter(ImageFilter.SHARPEN)
#     image = ImageEnhance.Contrast(image).enhance(2)
#     image = ImageOps.autocontrast(image)
#     width, height = image.size
#     new_width = int(width * 1.5)
#     new_height = int(height * 1.5)
#     image = image.resize((new_width, new_height), Image.Resampling.BICUBIC)
#     extracted_text = pytesseract.image_to_string(image, config='--psm 6')
#     extracted_text = extracted_text.lower()
#     print("extracted text ",extracted_text)
#     known_products = ['oreo', 'hershey', 'starburst', 'snickers',  'butterfinger']
#     for product in known_products:
#         if product in extracted_text:
#             return product.capitalize()
#     return 'Unknown Product'

from django.shortcuts import render
from .models import ProductImage
from django.core.files.storage import default_storage
import easyocr
from PIL import Image

reader = easyocr.Reader(['en'])

PRODUCT_INGREDIENTS = {
    'Oreo': ['Sugar', 'Unbleached Flour', 'Palm and/or Canola Oil', 'Cocoa (Processed with Alkali)'],
    'Hershey': ['Sugar', 'Milk', 'Cocoa Butter', 'Chocolate', 'Milk Fat'],
    'Skittles': ['Sugar', 'Corn Syrup', 'Hydrogenated Palm Kernel Oil', 'Citric Acid'],
    'Lay\'s': ['Potatoes', 'Vegetable Oil', 'Salt'],
    'Doritos': ['Corn', 'Vegetable Oil', 'Cheese', 'Salt'],
    'Cheetos': ['Cornmeal', 'Vegetable Oil', 'Cheese Flavor', 'Salt'],
    'Pringles': ['Dehydrated Potato Flakes', 'Corn Starch', 'Vegetable Oil', 'Salt'],
    'Ritz': ['Wheat Flour', 'Vegetable Oil', 'Sugar', 'Salt'],
    'Goldfish': ['Wheat Flour', 'Cheddar Cheese', 'Vegetable Oil', 'Salt'],
    'Cheez-Its': ['Wheat Flour', 'Cheddar Cheese', 'Vegetable Oil', 'Salt'],
    'Combos': ['Pretzel', 'Cheese', 'Vegetable Oil', 'Salt'],
    'SunChips': ['Whole Grain Corn', 'Whole Grain Wheat', 'Vegetable Oil', 'Salt'],
    'Munchies': ['Cheese-flavored Snacks', 'Pretzels', 'Corn Chips', 'Vegetable Oil'],
    'Bugles': ['Corn Meal', 'Vegetable Oil', 'Salt', 'Cheese Flavor'],
    'Fritos': ['Corn', 'Vegetable Oil', 'Salt'],
    'Tostitos': ['Corn', 'Vegetable Oil', 'Salt'],
    'Cocoa Puffs': ['Corn Flour', 'Sugar', 'Cocoa', 'Salt'],
    'Cap\'n Crunch': ['Corn Flour', 'Sugar', 'Oat Flour', 'Salt'],
    'Pop-Tarts': ['Flour', 'Sugar', 'Corn Syrup', 'Vegetable Oil'],
    'Nutri-Grain': ['Whole Grain Oats', 'Corn Syrup', 'Sugar', 'Fruit Filling'],
    'Rice Krispies': ['Rice', 'Sugar', 'Salt', 'Malt Flavor'],
    'Special K': ['Rice', 'Sugar', 'Wheat', 'Salt'],
    'Cheerios': ['Whole Grain Oats', 'Corn Starch', 'Sugar', 'Salt'],
    'Froot Loops': ['Corn Flour', 'Sugar', 'Oat Flour', 'Salt'],
    'Lucky Charms': ['Corn Flour', 'Sugar', 'Oat Flour', 'Marshmallows'],
    'Oatmeal Creme Pies': ['Oat Flour', 'Sugar', 'Vegetable Oil', 'Cream Filling'],
    'Little Debbie': ['Sugar', 'Wheat Flour', 'Vegetable Oil', 'Chocolate'],
    'HoHos': ['Cake', 'Cream Filling', 'Chocolate Coating', 'Sugar'],
    'Swiss Rolls': ['Cake', 'Cream Filling', 'Chocolate Coating', 'Sugar'],
    'Hostess Cupcakes': ['Cake', 'Cream Filling', 'Chocolate Frosting', 'Sugar'],
    'Twinkies': ['Cake', 'Cream Filling', 'Vegetable Oil', 'Sugar'],
    'Ring Dings': ['Cake', 'Chocolate Coating', 'Cream Filling', 'Sugar'],
    'Moon Pies': ['Marshmallow', 'Graham Cracker', 'Chocolate Coating', 'Sugar'],
    'Gushers': ['Fruit Puree', 'Corn Syrup', 'Sugar', 'Gelatin'],
    'Fruit by the Foot': ['Fruit Puree', 'Corn Syrup', 'Sugar', 'Gelatin'],
    'Airheads': ['Sugar', 'Corn Syrup', 'Hydrogenated Palm Kernel Oil', 'Flavorings'],
    'Jolly Rancher': ['Sugar', 'Corn Syrup', 'Artificial Flavor', 'Colorings'],
    'Laffy Taffy': ['Sugar', 'Corn Syrup', 'Palm Oil', 'Flavorings'],
    'Smarties': ['Sugar', 'Dextrose', 'Citric Acid', 'Natural and Artificial Flavors'],
    'Nerds': ['Sugar', 'Dextrose', 'Artificial Flavors', 'Colorings'],
    'Starburst': ['Sugar', 'Corn Syrup', 'Hydrogenated Palm Kernel Oil', 'Fruit Juice'],
    'Skittles': ['Sugar', 'Corn Syrup', 'Hydrogenated Palm Kernel Oil', 'Fruit Juice'],
    'Twizzlers': ['Corn Syrup', 'Sugar', 'Wheat Flour', 'Palm Oil'],
    'Red Vines': ['Sugar', 'Corn Syrup', 'Wheat Flour', 'Red Dye'],
    'Haribo': ['Sugar', 'Glucose Syrup', 'Gelatin', 'Flavorings'],
    'Gummy Bears': ['Sugar', 'Glucose Syrup', 'Gelatin', 'Flavorings'],
    'Swedish Fish': ['Sugar', 'Corn Syrup', 'Artificial Flavors', 'Red Dye'],
    'Pez': ['Sugar', 'Corn Syrup', 'Flavorings', 'Colorings'],
    'Pocky': ['Wheat Flour', 'Sugar', 'Vegetable Oil', 'Chocolate'],
    'KitKat': ['Wheat Flour', 'Sugar', 'Vegetable Oil', 'Chocolate'],
    'Milky Way': ['Sugar', 'Milk Chocolate', 'Corn Syrup', 'Chocolate'],
    'Mars': ['Sugar', 'Milk Chocolate', 'Corn Syrup', 'Vegetable Oil'],
    'Snickers': ['Peanuts', 'Sugar', 'Milk Chocolate', 'Corn Syrup'],
    'Reese\'s': ['Peanut Butter', 'Milk Chocolate', 'Sugar', 'Salt'],
    'Butterfinger': ['Peanut Butter', 'Sugar', 'Corn Syrup', 'Chocolate'],
    'Almond Joy': ['Almonds', 'Milk Chocolate', 'Coconut', 'Sugar'],
    'Mounds': ['Coconut', 'Dark Chocolate', 'Sugar', 'Corn Syrup'],
    'Fanta': ['Carbonated Water', 'High Fructose Corn Syrup', 'Natural Flavors', 'Citric Acid', 'Sodium Benzoate', 'Coloring'],
}

def check_product(request):
    if request.method == 'POST' and request.FILES['product_image']:
        product_image = ProductImage(image=request.FILES['product_image'])
        product_image.save()
        image_path = default_storage.path(product_image.image.name)
        product_name = extract_product_name(image_path)
        print(product_name)
        product_name_formatted = product_name.title()
    
        ingredients = PRODUCT_INGREDIENTS.get(product_name_formatted, 'Ingredients not available')
        
        if product_name in PRODUCT_INGREDIENTS:
            message = f"Warning: {product_name} contains sugar."
        else:
            message = f"{product_name} might not contain sugar."
        
        ingredient_message = f"Major ingredients: {', '.join(ingredients) if isinstance(ingredients, list) else ingredients}"
        
        return render(request, 'disease/result.html', {'message': message, 'ingredients': ingredient_message})
    
    return render(request, 'disease/upload.html')


def extract_product_name(image_path):
    image = Image.open(image_path)
    results = reader.readtext(image_path)
    extracted_text = ' '.join([result[1].lower() for result in results])
    print("extracted text:", extracted_text)
    known_products = [
    'oreo','fanta', 'hershey', 'skittles', 'lay\'s', 'doritos', 'cheetos', 'pringles', 'ritz',
    'goldfish', 'cheez-its', 'combos', 'sunchips', 'munchies', 'bugles', 'fritos', 
    'tostitos', 'cocoa puffs', 'cap\'n crunch', 'pop-tarts', 'nutri-grain', 'rice krispies', 
    'special k', 'cheerios', 'froot loops', 'lucky charms', 'oatmeal creme pies', 'little debbie',
    'hohos', 'swiss rolls', 'hostess cupcakes', 'twinkies', 'ring dings', 'moon pies', 'gushers',
    'fruit by the foot', 'airheads', 'jolly rancher', 'laffy taffy', 'smarties', 'nerds', 'starburst',
    'twizzlers', 'red vines', 'haribo', 'gummy bears', 'swedish fish', 'pez', 'pocky', 'kitkat',
    'milky way', 'mars', 'snickers', 'reese\'s', 'butterfinger', 'almond joy', 'mounds'
    ]
    extracted_prefix = extracted_text[:3]
    for product in known_products:
        if extracted_prefix == product[:3]:
            return product.capitalize()
    return 'Unknown Product'
