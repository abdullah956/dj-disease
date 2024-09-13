from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views import View
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth import logout
from disease.models import ProductImage
from django.core.files.storage import default_storage
from PIL import Image
from .models import Contact
from django.contrib import messages
import easyocr

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

def index_view(request):
    return render(request, 'index.html')

def about_view(request):
    return render(request, 'about.html')

def emergency_view(request):
    return render(request, 'emergency-care.html')

def avoid_view(request):
    return render(request, 'foods-to-avoid.html')

def info_view(request):
    return render(request, 'info.html')

def symptoms_view(request):
    return render(request, 'symptoms.html')


def triggers_view(request):
    return render(request, 'triggers.html')

class UserRegisterView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        return render(request, 'register.html', {'form': form})

class UserLoginView(View):
    def get(self, request):
        form = UserLoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('home') 
        return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def user_images(request):
    images = ProductImage.objects.filter(user=request.user)
    return render(request, 'scanned.html', {'images': images})



def selfcare_view(request):
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
        return render(request, 'result.html', {'message': message, 'ingredients': ingredient_message})
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
        return render(request, 'result.html', {'message': message, 'ingredients': ingredient_message})
    return render(request, 'selfcare.html')



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


def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f"Name: {name}, Phone: {phone}, Email: {email}, Message: {message}")
        contact = Contact(name=name, phone=phone, email=email, message=message)
        contact.save()

        messages.success(request, 'Your message has been sent successfully!')

        return redirect('home')

    return render(request, 'index.html')