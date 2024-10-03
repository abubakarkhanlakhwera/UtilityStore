from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from home.models import Items

@login_required
def add_to_cart(req, item_id):
    item = get_object_or_404(Items, id=item_id)
    cart, created = Cart.objects.get_or_create(user=req.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, item=item)
    
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart:cart_details')

@login_required
def remove_from_cart(req,item_id):
    cart = get_object_or_404(Cart, user=req.user)
    cart_item = get_object_or_404(CartItem, cart=cart, item_id=item_id)
    cart_item.delete()
    return redirect('cart:cart_details')

@login_required
def clear_cart(req):
    cart = get_object_or_404(Cart, user=req.user)
    cart.items.all().delete()
    return redirect('cart:cart_details')

@login_required
def cart_detail(request):
    cart = Cart.objects.filter(user=request.user).first()  # Fetch the cart for the logged-in user
    if not cart:
        cart_items = []
        total_price = 0
    else:
        cart_items = cart.items.all()
        total_price = cart.get_total_price()
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart/cart_detail.html', context)