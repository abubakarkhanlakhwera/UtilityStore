from django.db import models
from django.contrib.auth.models import User
from home.models import Items

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) :
        return f"Cart of {self.User.username}"
    
    def get_total_price(self):
        return sum([item.get_total_price() for item in self.items.all()])

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self) :
        return f"{self.quantity} x {self.item.name}"
    
    def get_total_price(self):
        return self.quantity * self.item.get_discounted_price()