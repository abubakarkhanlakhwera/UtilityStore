from django.shortcuts import render, redirect, get_object_or_404
from .models import Items, Store
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import StoreForm 
from .forms import ItemForm 

# Helper function to check if user is admin
def is_admin(user):
    return user.is_superuser

# Store detail view
def store_detail(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    items = store.items.all()  
    return render(request, 'home/store_detail.html', {'store': store, 'items': items})

# Items filtered by store type
def items_by_store_type(req, store_type):
    items = Items.objects.filter(type=store_type)
    return render(req, 'home/items_list.html', {'items': items, 'store_type': store_type})

# Item price view
def item_price(request, item_id):
    item = get_object_or_404(Items, id=item_id)
    return render(request, 'home/item_price.html', {'item': item})

# Item detail view
def item_detail(request, item_id):
    item = get_object_or_404(Items, id=item_id)
    return render(request, 'home/item_detail.html', {'item': item})

# View to delete a store (admin only)
@user_passes_test(is_admin)
def delete_store(req, store_id):
    store = get_object_or_404(Store, id=store_id)
    if req.method == "POST":
        store.delete()
        return redirect('home')
    return render(req, 'home/delete_store.html', {'store': store})  # Ensure a confirmation page or redirect logic

# View to list stores
def store_list(req):
    if req.user.is_superuser:
        stores = Store.objects.all()  # Admin sees all stores
    else:
        stores = Store.objects.filter(is_hidden=False)  # Non-admins see only non-hidden stores
    return render(req, 'home/store_list.html', {'stores': stores})

# View to edit a store (admin only)
@user_passes_test(is_admin)
def edit_store(req, store_id):
    store = get_object_or_404(Store, id=store_id)
    if req.method == "POST":
        form = StoreForm(req.POST, req.FILES, instance=store)  
        if form.is_valid():  # Save the form if valid
            store.is_hidden = 'is_hidden' in req.POST  # Check if the store should be hidden
            form.save()
            return redirect('home')  # Redirect to home or store detail after saving
    else:
        form = StoreForm(instance=store)  
    return render(req, 'home/edit_store.html', {'form': form, 'store': store})

# Assuming you have a form for items
def edit_item(request, item_id):
    item = get_object_or_404(Items, id=item_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('items_by_store_type', store_type=item.store.type)  # Adjust redirect as needed
    else:
        form = ItemForm(instance=item)
    return render(request, 'home/edit_item.html', {'form': form, 'item': item})

def delete_item(request, item_id):
    item = get_object_or_404(Items, id=item_id)
    if request.method == 'POST':
        item.delete()
        return redirect('items_by_store_type', store_type=item.store.type)  # Adjust redirect as needed
    return render(request, 'home/confirm_delete_item.html', {'item': item})

@login_required
def hide_store(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    if request.method == 'POST' and request.user.is_superuser:
        store.is_hidden = not store.is_hidden  # Toggle the hidden state
        store.save()
    return redirect('home')