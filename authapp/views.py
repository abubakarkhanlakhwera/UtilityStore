from django.contrib.auth.models import User
from django.shortcuts import render, redirect
import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from home.models import Store, Items

def auth_page(req):
    if req.user.is_authenticated:
        return redirect('home')
    return render(req, 'authapp/auth.html')

def signup(req):
    if req.method == "POST":
        form = UserCreationForm(req.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(req, 'authapp/signup.html', {'form': form})  # Ensure you render the form

@login_required
def home(req):
    total_users = User.objects.count()
    total_stores = Store.objects.count()

    # Filter stores based on user type
    if req.user.is_superuser:
        stores = Store.objects.all()  # Admin sees all stores
    else:
        stores = Store.objects.filter(is_hidden=False)  # Regular users see only non-hidden stores

    items = Items.objects.all()
    new_signups_today = User.objects.filter(date_joined__date=datetime.date.today()).count()

    context = {
        'total_users': total_users,
        'total_stores': total_stores,
        'stores': stores,
        'new_signups_today': new_signups_today,
    }
    
    return render(req, 'home/home.html', context)
def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect to home view if user is logged in
    else:
        return redirect('login')