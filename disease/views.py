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

PRODUCTS_WITH_SUGAR = [
    'Oreo', 'Hershey', 'Skittles', 'Starburst', 'Snickers', 'Butterfinger', 'Kurkure',
    'Cadbury Dairy Milk', 'Nestle KitKat', 'Mars', 'Twix', 'M&Ms', 'Reese\'s', 'Milky Way',
    'Snickers Almond', 'Bounty', 'Crunch', 'Ritter Sport', 'Toblerone', 'Lindt', 'Ferrero Rocher',
    'Ghirardelli', 'Jelly Belly', 'Haribo', 'Life Savers', 'Werther\'s Original', 'Nerds', 
    'KitKat Chunky', 'Peanut Butter Cups', 'Gummy Bears', 'Jolly Rancher', 'Smarties', 'Twizzlers',
    'Pop Rocks', 'Hershey\'s Kisses', 'Almond Joy', 'Cadbury Crunchie', 'Milka', 'York', 'Hershey\'s Syrup',
    'Kinder Bueno', 'Kinder Joy', 'Chupa Chups', 'Cheetos', 'Doritos', 'Lay\'s', 'Ruffles', 'Pringles',
    'Lays Stax', 'Munch', 'KitKat Senses', 'Cadbury 5 Star', 'Nestle Munch', 'Tango', 'Kool-Aid', 
    'Mirinda', 'Pepsi', 'Coca-Cola', 'Sprite', 'Fanta', '7 Up', 'Pakola', 'Mountain Dew', 
    'Shan', 'Nestle Fruita Vitals', 'Lux', 'Raro', 'Dairy Milk Silk', 'Dairy Milk Bubbly', 
    'Perk', 'KitKat Green Tea', 'Nestle Classic', 'Cadbury Dairy Milk Fruit & Nut', 'Cadbury Dairy Milk Roast Almond',
    'Jell-O', 'Airheads', 'Reese\'s Pieces', 'Bubblicious', 'Hubba Bubba', 'Bazooka', 'Double Bubble', 
    'Pez', 'Candy Corn', 'Kool-Aid Jammers', 'Otto', 'Raja', 'Willy Wonka', 'Chiclets', 'Big Red'
]

def check_product(request):
    if request.method == 'POST' and request.FILES['product_image']:
        product_image = ProductImage(image=request.FILES['product_image'])
        product_image.save()
        image_path = default_storage.path(product_image.image.name)
        product_name = extract_product_name(image_path)
        print(product_name)
        if product_name in PRODUCTS_WITH_SUGAR:
            message = f"Warning: {product_name} contains sugar."
        else:
            message = f"{product_name} might not contain sugar."
        return render(request, 'disease/result.html', {'message': message})
    return render(request, 'disease/upload.html')

def extract_product_name(image_path):
    image = Image.open(image_path)
    results = reader.readtext(image_path)
    extracted_text = ' '.join([result[1].lower() for result in results])
    print("extracted text:", extracted_text)
    known_products = [
    'oreo', 'hershey', 'skittles', 'starburst', 'snickers', 'butterfinger', 'kurkure',
    'cadbury dairy milk', 'nestle kitkat', 'mars', 'twix', 'm&ms', 'reese\'s', 'milky way',
    'snickers almond', 'bounty', 'crunch', 'ritter sport', 'toblerone', 'lindt', 'ferrero rocher',
    'ghirardelli', 'jelly belly', 'haribo', 'life savers', 'werther\'s original', 'nerds',
    'kitkat chunky', 'peanut butter cups', 'gummy bears', 'jolly rancher', 'smarties', 'twizzlers',
    'pop rocks', 'hershey\'s kisses', 'almond joy', 'cadbury crunchie', 'milka', 'york', 'hershey\'s syrup',
    'kinder bueno', 'kinder joy', 'chupa chups', 'cheetos', 'doritos', 'lays', 'ruffles', 'pringles',
    'lays stax', 'munch', 'kitkat senses', 'cadbury 5 star', 'nestle munch', 'tango', 'kool-aid',
    'mirinda', 'pepsi', 'coca-cola', 'sprite', 'fanta', '7 up', 'pakola', 'mountain dew',
    'shan', 'nestle fruita vitals', 'lux', 'raro', 'dairy milk silk', 'dairy milk bubbly',
    'perk', 'kitkat green tea', 'nestle classic', 'cadbury dairy milk fruit & nut', 'cadbury dairy milk roast almond',
    'jell-o', 'airheads', 'reese\'s pieces', 'bubblicious', 'hubba bubba', 'bazooka', 'double bubble',
    'pez', 'candy corn', 'kool-aid jammers', 'otto', 'raja', 'willy wonka', 'chiclets', 'big red'
    ]
    extracted_prefix = extracted_text[:3]
    for product in known_products:
        if extracted_prefix == product[:3]:
            return product.capitalize()
    return 'Unknown Product'
