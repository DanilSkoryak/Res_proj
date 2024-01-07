from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import Client, Product, Salesman, Sales, Registered_Users
from datetime import datetime
from django.contrib.auth.hashers import check_password, make_password
# Create your views here.
import uuid

def index(request):
    # check cookie
    user_token = request.COOKIES.get('user_token')
    if user_token:
        return render(request, 'index.html')
    return redirect('login')

def login(request):
    user_token = request.COOKIES.get('user_token') 

    if user_token:
        return redirect('index')

    if request.method == 'POST':
        email = request.POST.get('email').lower() 
        password = request.POST.get('password')

        # this part is used for already exist user, but user has no COOKIE yet
        try: 
            user = Registered_Users.objects.get(email=email)

            if check_password(password, user.password):
                user_token = str(uuid.uuid4())
                user.user_token = user_token
                user.save()

                response = redirect('index')
                response.set_cookie('user_token', user_token)
                return response
            else:
                return redirect('login')

        except Registered_Users.DoesNotExist:
            hashed_password = make_password(password)
            user_token = str(uuid.uuid4())
            
            # check already exist user with this email
            if not Registered_Users.objects.filter(email=email).exists():
                new_user = Registered_Users(email=email, password=hashed_password, user_token=user_token)
                new_user.save()

                response = redirect('index')
                response.set_cookie('user_token', user_token)
                return response
            else:
                return redirect('login')

    return render(request, 'login.html')


def show_clients(request):
    data = Client.objects.all()
    return render(request, 'clients.html', {'data_from_client': data})

def show_client(request, id):
    client = Client.objects.get(id=id)
    return render(request, 'client.html', {'client': client})

def show_salesman(request):
    data = Salesman.objects.all().prefetch_related('products')
    return render(request, 'salesman.html', {'data': data})

def show_seller(request, id):
    data = Salesman.objects.get(id=id)
    return render(request, 'seller.html', {'data': data})

def show_product(request):
    product = Product.objects.all()
    return render(request, 'product.html', {'data': product})

def show_sales(request):
    data = Sales.objects.all()
    return render(request, 'sales.html', {'data': data})

def edit_clients(request, id):
    client = Client.objects.get(id=id)
    return render(request, 'edit_clients.html', {'client': client})

def add_client(request):
    if request.method == 'POST':
        name = request.POST['user_name']
        lastname = request.POST['user_lastname']
        phone = request.POST['user_phone']
        email = request.POST['user_email']
        db = Client(name=name, lastname=lastname, phone=phone, email=email)
        db.save()

        return redirect('show_clients')

    return render(request, 'add_client.html')

def add_salesman(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        lastname = request.POST.get('lastname')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        employment_date_str = request.POST.get('date')
        position = request.POST.get('cash')

        try:
            employment_date_str = datetime.strptime(employment_date_str, '%Y-%m-%d').date()
        except ValueError:
            return HttpResponse("Invalid date format")

        # check Salesman with this Email
        existing_salesman = Salesman.objects.filter(email=email).first()

        if existing_salesman:
            # add new product to already exists
            product_name = request.POST.get('product_name')
            description = request.POST.get('description')

            db_product = Product(
                name=product_name,
                description=description
            )
            db_product.save()

            existing_salesman.products.add(db_product)

            return redirect('show_salesman')

        # if not found Salesman with this Email than Create
        db_salesman = Salesman(
            name=name,
            lastname=lastname,
            phone=phone,
            email=email,
            employment_date=employment_date_str,
            position=position
        )
        db_salesman.save()

        product_name = request.POST.get('product_name')
        description = request.POST.get('description')

        db_product = Product(
            name=product_name,
            description=description
        )
        db_product.save()

        db_salesman.products.add(db_product)

        return redirect('show_salesman')

    return render(request, 'add_salesman.html')


