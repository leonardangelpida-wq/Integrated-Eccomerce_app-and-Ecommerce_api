import requests
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from django.contrib.auth.models import User

API_URL = "http://127.0.0.1:8001"  # FastAPI backend

# ---------- PRODUCTS ----------

def home(request):
    """List all products (from FastAPI)"""
    response = requests.get(f"{API_URL}/items")
    products = response.json() if response.status_code == 200 else []
    return render(request, "home.html", {"products": products})


def product(request, pk):
    """Get a single product by ID (from FastAPI)"""
    response = requests.get(f"{API_URL}/items/{pk}")
    product = response.json() if response.status_code == 200 else None
    return render(request, "product.html", {"product": product})

# ---------- STATIC PAGES ----------

def about(request):
    return render(request, 'about.html', {})

# ---------- AUTH ----------

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You've been logged in successfully 🎉")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password ❌")
            return redirect('login')

    return render(request, 'login.html', {})

def guest_login(request):
    # Get or create a predefined guest user
    guest_user, created = User.objects.get_or_create(
        username='guest_user',
        defaults={'email': 'guest@example.com'}
    )
    guest_user.set_unusable_password()  # optional: prevent login with password
    guest_user.save()

    # Log the guest in
    login(request, guest_user)

    # Redirect to homepage or shop
    return redirect('home')


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out 👋")
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have registered successfully ✅")
            return redirect('home')
        else:
            messages.error(request, "Hindi po pwede ate ❌")
            return redirect('register')

    return render(request, 'register.html', {'form': form})
