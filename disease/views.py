from django.shortcuts import render
from .models import ProductImage
from django.core.files.storage import default_storage
import pytesseract
import cv2  
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

PRODUCTS_WITH_SUGAR = ['Oreo', 'Hershey', 'Starburst', 'Snickers',  'Butterfinger']

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
    image = image.convert('L')
    image = image.filter(ImageFilter.SHARPEN)
    image = ImageEnhance.Contrast(image).enhance(2)
    image = ImageOps.autocontrast(image)
    width, height = image.size
    new_width = int(width * 1.5)
    new_height = int(height * 1.5)
    image = image.resize((new_width, new_height), Image.Resampling.BICUBIC)
    extracted_text = pytesseract.image_to_string(image, config='--psm 6')
    extracted_text = extracted_text.lower()
    print("extracted text ",extracted_text)
    known_products = ['oreo', 'hershey', 'starburst', 'snickers',  'butterfinger']
    for product in known_products:
        if product in extracted_text:
            return product.capitalize()
    return 'Unknown Product'
