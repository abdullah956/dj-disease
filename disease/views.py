from django.shortcuts import render
from .models import ProductImage
from django.core.files.storage import default_storage
import pytesseract
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


PRODUCTS_WITH_SUGAR = ['Oreo', 'Coke', 'Snickers', 'Sprite', 'KitKat']

def check_product(request):
    if request.method == 'POST' and request.FILES['product_image']:
        # Save the uploaded image to the database
        product_image = ProductImage(image=request.FILES['product_image'])
        product_image.save()

        # Get the path of the saved image
        image_path = default_storage.path(product_image.image.name)

        # Extract the product name using OCR
        product_name = extract_product_name(image_path)

        if product_name in PRODUCTS_WITH_SUGAR:
            message = f"Warning: {product_name} contains sugar."
        else:
            message = f"{product_name} might not contain sugar."

        return render(request, 'disease/result.html', {'message': message})

    return render(request, 'disease/upload.html')
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Make sure this path is correct

def extract_product_name(image_path):
    # Load the image using PIL
    image = Image.open(image_path)

    # Convert the image to grayscale
    image = image.convert('L')

    # Apply image filters to enhance the text
    image = image.filter(ImageFilter.SHARPEN)
    image = ImageEnhance.Contrast(image).enhance(2)

    # Use pytesseract to extract text from the image
    extracted_text = pytesseract.image_to_string(image)

    # Normalize the extracted text to find product names
    extracted_text = extracted_text.lower()

    # List of known products with sugar
    known_products = ['oreo', 'coke', 'snickers', 'sprite', 'kitkat']

    # Check if any known product name is in the extracted text
    for product in known_products:
        if product in extracted_text:
            return product.capitalize()

    # If no product is found, return "Unknown Product"
    return 'Unknown Product'
