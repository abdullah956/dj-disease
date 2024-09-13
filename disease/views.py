from django.shortcuts import render
from .models import ProductImage
from django.core.files.storage import default_storage
import easyocr
from PIL import Image

reader = easyocr.Reader(['en'])

PRODUCT_INGREDIENTS = {
    'choco pops': {
        'Rice': '30%',
        'Sugar': '25%',
        'Cocoa powder': '12%',
        'Salt': '1%',
        'Barley malt extract': '5%',
        'Glucose syrup': '3%',
        'Flavouring': '1%',
        'Vitamins and minerals': 'Vitamin B12, Iron, Niacin, Riboflavin, Thiamin, Folic Acid (collectively less than 1%)'
    },
    'skippy': {
        'Roasted peanuts': '90%',
        'Sugar': '2%',
        'Palm oil': '5%',
        'Salt': '1%',
        'Hydrogenated vegetable oils (cottonseed, rapeseed, soybean)': '2%'
    },
    'cup cake': {
        'Flour': '30%',
        'Sugar': '25%',
        'Butter': '20%',
        'Eggs': '15%',
        'Milk': '5%',
        'Baking powder': '1%',
        'Salt': '0.5%',
        'Vanilla extract': '0.5%',
        'Frosting (optional: powdered sugar, butter, flavorings)': '3%'
    },
    'sue bee': {
        'Pure honey': '100%'
    }
}

def check_product(request):
    if request.method == 'POST' and request.FILES.get('product_image'):
        user = request.user
        product_name = request.POST.get('name')
        product_image = ProductImage(user=user, name=product_name,image=request.FILES['product_image'])
        product_image.save()
        #for name
        product_name_normalized = product_name.lower().replace(' ', '')
        ingredients = {key.replace(' ', '').lower(): value for key, value in PRODUCT_INGREDIENTS.items()}
        product_ingredients = ingredients.get(product_name_normalized, {})
        if product_ingredients:
            message = f"Warning: {product_name.title()} contains sugar."
            ingredient_message = "Major ingredients and percentages: " + ', '.join([f"{ingredient}: {percentage}" for ingredient, percentage in product_ingredients.items()])
        else:
            message = f"{product_name.title()} information not available."
            ingredient_message = "Ingredients information is not available."
        return render(request, 'disease/result.html', {'message': message, 'ingredients': ingredient_message})
        #for images
        image_path = default_storage.path(product_image.image.name)
        product_name = extract_product_name(image_path)
        product_name_formatted = product_name.title()
        ingredients = PRODUCT_INGREDIENTS.get(product_name_formatted, {})
        if ingredients:
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
    known_products = [ 'choco pops','skippy','cupcake','sue bee']
    extracted_prefix = extracted_text[:3]
    for product in known_products:
        if extracted_prefix == product[:3]:
            return product.capitalize()
    return 'Unknown Product'
