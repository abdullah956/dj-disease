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
    'Oreo': {'Sugar': '36%', 'Unbleached Flour': '30%', 'Palm and/or Canola Oil': '20%', 'Cocoa (Processed with Alkali)': '14%'},
    'Hershey': {'Sugar': '50%', 'Milk': '20%', 'Cocoa Butter': '15%', 'Chocolate': '10%', 'Milk Fat': '5%'},
    'Skittles': {'Sugar': '50%', 'Corn Syrup': '20%', 'Hydrogenated Palm Kernel Oil': '15%', 'Citric Acid': '10%'},
    'Lay\'s': {'Potatoes': '60%', 'Vegetable Oil': '30%', 'Salt': '10%'},
    'Doritos': {'Corn': '50%', 'Vegetable Oil': '30%', 'Cheese': '15%', 'Salt': '5%'},
    'Cheetos': {'Cornmeal': '60%', 'Vegetable Oil': '20%', 'Cheese Flavor': '15%', 'Salt': '5%'},
    'Pringles': {'Dehydrated Potato Flakes': '50%', 'Corn Starch': '30%', 'Vegetable Oil': '15%', 'Salt': '5%'},
    'Ritz': {'Wheat Flour': '60%', 'Vegetable Oil': '20%', 'Sugar': '15%', 'Salt': '5%'},
    'Goldfish': {'Wheat Flour': '60%', 'Cheddar Cheese': '20%', 'Vegetable Oil': '15%', 'Salt': '5%'},
    'Cheez-Its': {'Wheat Flour': '60%', 'Cheddar Cheese': '20%', 'Vegetable Oil': '15%', 'Salt': '5%'},
    'Combos': {'Pretzel': '50%', 'Cheese': '30%', 'Vegetable Oil': '15%', 'Salt': '5%'},
    'SunChips': {'Whole Grain Corn': '50%', 'Whole Grain Wheat': '30%', 'Vegetable Oil': '15%', 'Salt': '5%'},
    'Munchies': {'Cheese-flavored Snacks': '40%', 'Pretzels': '30%', 'Corn Chips': '20%', 'Vegetable Oil': '10%'},
    'Bugles': {'Corn Meal': '60%', 'Vegetable Oil': '20%', 'Salt': '10%', 'Cheese Flavor': '10%'},
    'Fritos': {'Corn': '70%', 'Vegetable Oil': '20%', 'Salt': '10%'},
    'Tostitos': {'Corn': '70%', 'Vegetable Oil': '20%', 'Salt': '10%'},
    'Cocoa Puffs': {'Corn Flour': '50%', 'Sugar': '30%', 'Cocoa': '15%', 'Salt': '5%'},
    'Cap\'n Crunch': {'Corn Flour': '50%', 'Sugar': '30%', 'Oat Flour': '15%', 'Salt': '5%'},
    'Pop-Tarts': {'Flour': '50%', 'Sugar': '30%', 'Corn Syrup': '15%', 'Vegetable Oil': '5%'},
    'Nutri-Grain': {'Whole Grain Oats': '50%', 'Corn Syrup': '25%', 'Sugar': '15%', 'Fruit Filling': '10%'},
    'Rice Krispies': {'Rice': '50%', 'Sugar': '30%', 'Salt': '10%', 'Malt Flavor': '10%'},
    'Special K': {'Rice': '40%', 'Sugar': '30%', 'Wheat': '20%', 'Salt': '10%'},
    'Cheerios': {'Whole Grain Oats': '60%', 'Corn Starch': '20%', 'Sugar': '15%', 'Salt': '5%'},
    'Froot Loops': {'Corn Flour': '50%', 'Sugar': '30%', 'Oat Flour': '15%', 'Salt': '5%'},
    'Lucky Charms': {'Corn Flour': '50%', 'Sugar': '30%', 'Oat Flour': '15%', 'Marshmallows': '5%'},
    'Oatmeal Creme Pies': {'Oat Flour': '50%', 'Sugar': '30%', 'Vegetable Oil': '15%', 'Cream Filling': '5%'},
    'Little Debbie': {'Sugar': '40%', 'Wheat Flour': '30%', 'Vegetable Oil': '20%', 'Chocolate': '10%'},
    'HoHos': {'Cake': '50%', 'Cream Filling': '30%', 'Chocolate Coating': '15%', 'Sugar': '5%'},
    'Swiss Rolls': {'Cake': '50%', 'Cream Filling': '30%', 'Chocolate Coating': '15%', 'Sugar': '5%'},
    'Hostess Cupcakes': {'Cake': '50%', 'Cream Filling': '30%', 'Chocolate Frosting': '15%', 'Sugar': '5%'},
    'Twinkies': {'Cake': '50%', 'Cream Filling': '30%', 'Vegetable Oil': '15%', 'Sugar': '5%'},
    'Ring Dings': {'Cake': '50%', 'Chocolate Coating': '30%', 'Cream Filling': '15%', 'Sugar': '5%'},
    'Moon Pies': {'Marshmallow': '40%', 'Graham Cracker': '30%', 'Chocolate Coating': '20%', 'Sugar': '10%'},
    'Gushers': {'Fruit Puree': '50%', 'Corn Syrup': '30%', 'Sugar': '15%', 'Gelatin': '5%'},
    'Fruit by the Foot': {'Fruit Puree': '50%', 'Corn Syrup': '30%', 'Sugar': '15%', 'Gelatin': '5%'},
    'Airheads': {'Sugar': '60%', 'Corn Syrup': '20%', 'Hydrogenated Palm Kernel Oil': '15%', 'Flavorings': '5%'},
    'Jolly Rancher': {'Sugar': '60%', 'Corn Syrup': '20%', 'Artificial Flavor': '15%', 'Colorings': '5%'},
    'Laffy Taffy': {'Sugar': '60%', 'Corn Syrup': '20%', 'Palm Oil': '15%', 'Flavorings': '5%'},
    'Smarties': {'Sugar': '60%', 'Dextrose': '20%', 'Citric Acid': '10%', 'Natural and Artificial Flavors': '10%'},
    'Nerds': {'Sugar': '60%', 'Dextrose': '20%', 'Artificial Flavors': '15%', 'Colorings': '5%'},
    'Starburst': {'Sugar': '50%', 'Corn Syrup': '20%', 'Hydrogenated Palm Kernel Oil': '15%', 'Fruit Juice': '15%'},
    'Twizzlers': {'Corn Syrup': '50%', 'Sugar': '30%', 'Wheat Flour': '15%', 'Palm Oil': '5%'},
    'Red Vines': {'Sugar': '60%', 'Corn Syrup': '20%', 'Wheat Flour': '15%', 'Red Dye': '5%'},
    'Haribo': {'Sugar': '50%', 'Glucose Syrup': '30%', 'Gelatin': '15%', 'Flavorings': '5%'},
    'Gummy Bears': {'Sugar': '50%', 'Glucose Syrup': '30%', 'Gelatin': '15%', 'Flavorings': '5%'},
    'Swedish Fish': {'Sugar': '60%', 'Corn Syrup': '20%', 'Artificial Flavors': '15%', 'Red Dye': '5%'},
    'Pez': {'Sugar': '60%', 'Corn Syrup': '20%', 'Flavorings': '15%', 'Colorings': '5%'},
    'Pocky': {'Wheat Flour': '50%', 'Sugar': '30%', 'Vegetable Oil': '15%', 'Chocolate': '5%'},
    'KitKat': {'Wheat Flour': '50%', 'Sugar': '30%', 'Vegetable Oil': '15%', 'Chocolate': '5%'},
    'Milky Way': {'Sugar': '50%', 'Milk Chocolate': '30%', 'Corn Syrup': '15%', 'Chocolate': '5%'},
    'Mars': {'Sugar': '50%', 'Milk Chocolate': '30%', 'Corn Syrup': '15%', 'Vegetable Oil': '5%'},
    'Snickers': {'Peanuts': '40%', 'Sugar': '30%', 'Milk Chocolate': '20%', 'Corn Syrup': '10%'},
    'Reese\'s': {'Peanut Butter': '40%', 'Milk Chocolate': '30%', 'Sugar': '25%', 'Salt': '5%'},
    'Butterfinger': {'Peanut Butter': '35%', 'Sugar': '30%', 'Corn Syrup': '25%', 'Chocolate': '10%'},
    'Almond Joy': {'Almonds': '30%', 'Milk Chocolate': '30%', 'Coconut': '30%', 'Sugar': '10%'},
    'Mounds': {'Coconut': '40%', 'Dark Chocolate': '30%', 'Sugar': '20%', 'Corn Syrup': '10%'},
    'Fanta': {'Carbonated Water': '90%', 'High Fructose Corn Syrup': '5%'},
    'abc': {'ok' : '10%'},
    }


def check_product(request):
    if request.method == 'POST' and request.FILES.get('product_image'):
        user = request.user
        product_name1 = request.POST.get('name')
        product_image = ProductImage(user=user, name=product_name1,image=request.FILES['product_image'])
        product_image.save()
        image_path = default_storage.path(product_image.image.name)
        
        print("product name from form",product_name1)
        product_name = extract_product_name(image_path)
        product_name_formatted = product_name.title()
        ingredients = PRODUCT_INGREDIENTS.get(product_name_formatted, {})
        print(ingredients)
        if product_name1 in PRODUCT_INGREDIENTS:
            message = f"Warning: {product_name1} contains sugar."
            return render(request, 'disease/result.html', {'message': message})
        elif ingredients:
            message = f"Warning: {product_name} contains sugar."
            ingredient_message = "Major ingredients and percentages: " + ', '.join([f"{ingredient}: {percentage}" for ingredient, percentage in ingredients.items()])
        else:
            message = f"{product_name} information not available."
            ingredient_message = "Ingredients information is not available."
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
