from django.shortcuts import render, redirect
from .models import Product, Block, Manufacturer, ManufacturerUser, Retailer, RetailerUser
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import hashlib
from django.urls import reverse

def executer(request):
    Manufacturer.objects.all().delete()
    Retailer.objects.all().delete()
    Product.objects.all().delete()
    Block.objects.all().delete()
    ManufacturerUser.objects.all().delete()
    RetailerUser.objects.all().delete()
    User.objects.all().delete()
    return redirect("login")

def generate_hash(name,description):
    # Generate a hash for the product using SHA256
    hash_object = hashlib.sha256()
    hash_object.update(name.encode())
    hash_object.update(description.encode())
    # hash_object.update(product.manufacturer.encode())
    # hash_object.update(product.retailer.encode())
    # hash_object.update(product.identifier.encode())
    return hash_object.hexdigest()

def qrcode(request,data):
    return render(request,"qrcode.html",{"data":data})

@login_required
def add_product(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        retailer = request.POST['retailer']
        print(retailer,request.user)
        print(Retailer.objects.get(retailer_ID=retailer),request.user.manufactureruser.manufacturer)
        # manufacturer = Manufacturer.objects.get(manufacturer_ID=request.user)
        # print("hai",manufacturer)
        identifier = generate_hash(name,description)
        product = Product(name=name, description=description, manufacturer=request.user.manufactureruser.manufacturer , retailer=Retailer.objects.get(retailer_ID=retailer), identifier=identifier)
        product.save()

        try:
            current_block = Block.objects.latest('id')
        except Block.DoesNotExist:
            # If there are no blocks in the database, create a new default block
            current_block = Block(current_block='default')
            current_block.save()

        previous_block = current_block.current_block
        new_block = Block(previous_block=previous_block, current_block=identifier)
        new_block.save()

        return redirect(reverse('qrcode', kwargs={'data': identifier}))
    else:
        manufacturer = request.user.manufactureruser.manufacturer
        retailers = manufacturer.retailer_set.all()
        context = {'retailers': retailers}
        return render(request, 'add_product.html',context=context)


@login_required
def verify_product(request):
    if request.method == 'POST':
        identifier = request.POST.get('identifier')
        try:
            product = Product.objects.get(identifier=identifier)
            block = Block.objects.get(current_block=identifier, verified=False)
            block.verified = True
            product.verified = True
            product.save()
            block.save()
            return render(request, 'verified.html', {'product': product})
        except:
            return render(request, 'not_verified.html')
    else:
        return render(request, 'verify_product.html')


def signup_view(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        manufacturer_ID = request.POST.get('manufacturer_ID')
        # check if the manufacturer ID already exists
        if Manufacturer.objects.filter(manufacturer_ID=manufacturer_ID).exists():
            error_message = 'A manufacturer with that ID already exists'
        else:
            # create a new user
            user = User.objects.create_user(username=username, password=password)
            # create a new manufacturer and associate it with the user
            manufacturer = Manufacturer.objects.create(manufacturer_ID=manufacturer_ID)
            ManufacturerUser.objects.create(user=user, manufacturer=manufacturer)
            # authenticate the user and log them in
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('manufacturer_dashboard')

    return render(request, 'signup.html', {'error_message': error_message, "manufacturers": ManufacturerUser.objects.all()})


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect("signup")
        try:
            if request.user.manufactureruser:
                return redirect('manufacturer_dashboard')
        except:
            try:
                return redirect('retailer_dashboard')
            except:
                logout(request)
                return redirect("login")
        
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return redirect("signup")
            try:
                if user.manufactureruser:
                    return redirect('manufacturer_dashboard')
            except:
                if user.retaileruser:
                    return redirect('retailer_dashboard')
        else:
            error_message = 'Invalid login credentials'
    return render(request, 'login.html', {'error_message': error_message})

@login_required
def manufacturer_dashboard(request):
    if not request.user.manufactureruser:
        return redirect('logout')
    # Get the logged-in user's manufacturer object
    manufacturer = request.user.manufactureruser.manufacturer
    # Get all the retailers associated with the manufacturer
    # retailers = manufacturer.retailer_set.all()
    retailers = RetailerUser.objects.filter(retailer__manufacturer=manufacturer)
    products = Product.objects.filter(manufacturer=manufacturer)
    context = {'manufacturer': manufacturer, 'retailers': retailers, "products": products, "blocks": Block.objects.all()}
    return render(request, 'manufacturer_dashboard.html', context)

@login_required(login_url='/')
def create_retailer(request):
    user = request.user
    if user.manufactureruser:
        error_message = None

        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            retailer_ID = request.POST.get('retailer_ID')
            # check if the retailer ID already exists
            if Retailer.objects.filter(retailer_ID=retailer_ID).exists():
                error_message = 'A retailer with that ID already exists'
            else:
                # create a new user
                user = User.objects.create_user(username=username, password=password)
                # create a new retailer and associate it with the user
                retailer = Retailer.objects.create(retailer_ID=retailer_ID, manufacturer=ManufacturerUser.objects.get(user=request.user).manufacturer)
                RetailerUser.objects.create(user=user, retailer=retailer)
                return redirect('manufacturer_dashboard')

        return render(request, 'retailer_signup.html', {'error_message': error_message})
    else:
        return redirect('logout')

@login_required
def retailer_dashboard(request):
    # Get the logged-in user's retailer object
    retailer = request.user.retaileruser.retailer
    # Get the manufacturer associated with the retailer
    products = Product.objects.filter(retailer=retailer)
    manufacturer = retailer.manufacturer.manufactureruser
    context = {'retailer': retailer, 'manufacturer': manufacturer, "products": products}
    return render(request, 'retailer_dashboard.html', context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def consumer_dashboard(request):
    if request.method == 'POST':
        identifier = request.POST.get('identifier')
        try:
            product = Product.objects.get(identifier=identifier, verified=True)
            return render(request, 'verified.html', {'product': product})
        except:
            return render(request, 'not_verified.html')
    else:
        return render(request, 'consumer_dashboard.html')