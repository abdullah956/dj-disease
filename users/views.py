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
    'alpro': {
    'Water': '60-90%',
    'Almonds/Soybeans': '2-10%',
    'Sweeteners (e.g., Cane Sugar, Maltodextrin)': '0-10%',
    'Stabilizers (e.g., Gellan Gum, Guar Gum)': '0-1%',
    'Calcium Carbonate': '0-1%',
    'Flavors (e.g., Vanilla, Chocolate)': '0-1%',
    'Salt': '0-1%',
    'Vitamins (e.g., Vitamin D2, Vitamin B12)': '0-1%'
    },

    'grapefruit juice': {
    'Grapefruit': '100%'
    },
    'greek yogurt': {
    'Milk': '95%',
    'Live Active Cultures (e.g., Lactobacillus bulgaricus, Streptococcus thermophilus)': '4%',
    'Cream': '1%',
    'Pectin': '0.5%',
    'Citric Acid': '0.5%'
    },
    'quest': {
    'Protein Blend (Milk Protein Isolate, Whey Protein Isolate)': '30%',
    'Isomalto-oligosaccharides (IMO)': '25%',
    'Almonds': '15%',
    'Water': '10%',
    'Cocoa Powder': '8%',
    'Natural Flavors': '5%',
    'Vegetable Glycerin': '4%',
    'Salt': '2%',
    'Sucralose': '1%',
    'Steviol Glycosides (Stevia)': '1%'
    },
    'shortbread': {
    'Flour': '60%',
    'Butter': '30%',
    'Sugar': '10%',
    'Salt': '0.5%',
    'Vanilla Extract': '0.5%'
    },
    'smilac': {
    'Milk Powder': '60%',
    'Sugar': '25%',
    'Vegetable Oil': '10%',
    'Lactose': '3%',
    'Emulsifiers': '1%',
    'Flavorings': '0.5%',
    'Stabilizers': '0.5%'
    },
    'maggi': {
    'Wheat Flour': '60%',
    'Palm Oil': '15%',
    'Salt': '10%',
    'Spices': '5%',
    'Vegetable Extracts': '4%',
    'Monosodium Glutamate (MSG)': '3%',
    'Soy Sauce': '2%',
    'Sugar': '1%',
    'Flavors': '0.5%',
    'Coloring Agents': '0.5%'
    },
    'biscoff': {
    'Wheat Flour': '40%',
    'Sugar': '30%',
    'Vegetable Oil (Palm)': '20%',
    'Brown Sugar': '5%',
    'Sodium Bicarbonate': '2%',
    'Salt': '1%',
    'Cinnamon': '1%',
    'Cloves': '0.5%',
    'Nutmeg': '0.5%',
    },
    'digestive': {
    'Wheat Flour': '60%',
    'Sugar': '15%',
    'Vegetable Oil (Palm or Canola)': '12%',
    'Whole Wheat Flour': '10%',
    'Baking Powder': '2%',
    'Salt': '1%',
    'Malt Extract': '1%',
    },
    'haribo': {
    'Sugar': '50%',
    'Glucose Syrup': '30%',
    'Gelatin': '15%',
    'Citric Acid': '2%',
    'Natural and Artificial Flavors': '2%',
    'Coloring Agents': '1%',
    'Lactic Acid': '1%',
    'Palm Oil': '1%',
    },
    'guylian': {
    'Sugar': '50%',
    'Vegetable Oil (Palm or Coconut)': '25%',
    'Milk Powder': '15%',
    'Cocoa Mass': '10%',
    'Hazelnuts': '5%',
    'Cocoa Butter': '5%',
    'Emulsifier (Lecithin)': '0.5%',
    'Vanilla Extract': '0.5%',
    'Salt': '0.1%',
    },
    'toblerone': {
    'Sugar': '50%',
    'Milk Powder': '30%',
    'Cocoa Butter': '15%',
    'Cocoa Mass': '10%',
    'Honey': '5%',
    'Almonds': '3%',
    'Emulsifier (Lecithin)': '0.5%',
    'Vanilla Extract': '0.5%',
    },
    'cappuccino': {
    'Instant Coffee': '100%',
    },
    'pasta': {
    'Durum Wheat Semolina': '100%',
    },
    'blast 0 butter': {
    'Popped Corn': '100%',
    'Salt': 'Variable',
    'Oil (such as Canola or Coconut)': 'Variable',
    'Flavorings (such as Cheese or Spices)': 'Variable'
    },
    'popcorn': {
    'Popped Corn': '100%',
    'Salt': 'Variable',
    'Butter': 'Variable',
    'Oil (such as Canola or Coconut)': 'Variable',
    'Flavorings (such as Cheese or Caramel)': 'Variable'
    },
    'nutella': {
    'Sugar': '57%',
    'Palm Oil': '22%',
    'Hazelnuts': '13%',
    'Cocoa': '8%',
    'Skimmed Milk Powder': '6%',
    'Whey Powder': '4%',
    'Fat-Reduced Cocoa': '1%',
    'Emulsifier (Lecithin)': '0.4%',
    'Vanillin': '0.2%'
    },
    'bites': {
    'Whole Wheat Flour': '40%',
    'Sugar': '25%',
    'Vegetable Oil': '15%',
    'Corn Starch': '10%',
    'Salt': '5%',
    'Baking Powder': '3%',
    'Flavorings (Natural or Artificial)': '2%',
    'Preservatives (if any)': 'trace amounts'
    },
    'bugles': {
    'Corn Meal': '60%',
    'Vegetable Oil (Canola or Sunflower)': '20%',
    'Corn Starch': '10%',
    'Salt': '5%',
    'Sugar': '2%',
    'Leavening Agents (such as Baking Soda or Baking Powder)': '2%',
    'Flavorings (Natural or Artificial)': '1%'
    },
    'sun bites': {
    'Whole Grain Corn': '50%',
    'Whole Grain Rice': '25%',
    'Sunflower Oil': '10%',
    'Sugar': '8%',
    'Salt': '2%',
    'Corn Syrup': '2%',
    'Natural Flavors': '1%',
    'Vitamins and Minerals (varies)': 'trace amounts'
    },
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
    'gerber organic baby food': {
    'Organic Carrots': '100%',
    'Organic Water': 'as needed',
    'Organic Lemon Juice Concentrate': 'small amount',
    'Organic Ascorbic Acid (Vitamin C)': 'trace amount'
    },
    'four fruits': {
    'Organic Apples': '40%',
    'Organic Bananas': '30%',
    'Organic Pears': '20%',
    'Organic Peaches': '10%',
    'Organic Lemon Juice Concentrate': 'trace amount',
    'Organic Ascorbic Acid (Vitamin C)': 'trace amount'
    },
    'cheddar cheese': {
    'Milk': '90%',
    'Cheese Culture': '1%',
    'Rennet': '0.5%',
    'Salt': '1%',
    'Annatto (for coloring)': 'trace amount',
    'Calcium Chloride': '0.5%'
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
            message = f"{product_name.title()}"
            if any("sugar" in ingredient.lower() for ingredient in product_ingredients):
                ingredient_message = "These ingredients contain sugar: " + ', '.join([f"{ingredient}: {percentage}" for ingredient, percentage in product_ingredients.items()])
                ingredient_message1 = "These ingredients contain sugar (Not Safe to Consume)"
            else:
                ingredient_message = "Major ingredients and percentages: " + ', '.join([f"{ingredient}: {percentage}" for ingredient, percentage in product_ingredients.items()])
                ingredient_message1 = "These ingredients do not contain sugar (Safe to Consume)"
            return render(request, 'result.html', {'message': message, 'ingredients': ingredient_message, 'ingredients1' : ingredient_message1})
        else:
            message = f"{product_name.title()} information not available."
            ingredient_message = "Ingredient information is not available."
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
    known_products = [
    'alpro',
    'grapefruit juice',
    'greek yogurt',
    'quest',
    'shortbread',
    'smilac',
    'maggi',
    'biscoff',
    'digestive',
    'haribo',
    'guylian',
    'toblerone',
    'nescafe',
    'pasta',
    'blast 0 butter',
    'popcorn',
    'nutella',
    'bites',
    'bugles',
    'sun bites',
    'choco pops',
    'skippy',
    'cup cake',
    'gerber organic baby food',
    'four fruits',
    'cheddar cheese',
    'sue bee'
]
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