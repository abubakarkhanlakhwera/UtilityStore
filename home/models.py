from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Store(models.Model):
    type_of_Store = [
        ('Food', 'Food'),
        ('Utility', 'Utility'),
        ('Optical', 'Optical'),
        ('Gadget', 'Gadget'),
        ('Software', 'Software'),
    ]
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive')
    ]
    name = models.CharField(max_length=100)
    details = models.TextField(default="Store", max_length=1000)
    created_at = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='store_images/')
    location = models.CharField(max_length=50, blank=True, null=True, help_text="Physical or region location of the store", default="Chishtian")
    type = models.CharField(choices=type_of_Store, max_length=50)
    status = models.CharField(choices=STATUS_CHOICES, max_length=50, default="Active", help_text="Is the store currently active?")
    contact_email = models.EmailField(blank=True, null=True, help_text="Email address for contacting the store")
    contact_phone = models.IntegerField(blank=True, null=True, help_text="Phone number for contacting the store")
    categories = models.ManyToManyField('Category', related_name='stores', blank=True)
    is_hidden = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Stores"

    def __str__(self):
        return self.name

    def total_items(self):
        """Returns the total number of items in the store."""
        return self.items.aggregate(total=models.Sum('quantity'))['total'] or 0


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Items(models.Model):
    type_of_product = [
        ('Food', 'Food'),
        ('Utility', 'Utility'),
        ('Optical', 'Optical'),
        ('Gadget', 'Gadget'),
        ('Software', 'Software'),
    ]
    name = models.CharField(default="item", verbose_name="Item Name", help_text="Enter the name of the item", max_length=500)
    uploaded_by = models.CharField(max_length=50, default='')
    details = models.TextField(default="", verbose_name="Item Details", help_text="Detailed description of the item", null=True, blank=True)
    image = models.ImageField(upload_to='item_images/')
    date_added = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.IntegerField(default=0, null=True, blank=True)  # Discount percentage
    type = models.CharField(max_length=10, choices=type_of_product)
    store = models.ForeignKey('Store', on_delete=models.CASCADE, related_name='items', null=True, blank=True)
    keywords = models.CharField(max_length=200, blank=True, help_text="Enter keywords for search separated by commas")
    quantity = models.PositiveIntegerField(default=0, help_text="Number of items available in stock")

    class Meta:
        verbose_name_plural = "Items"

    def __str__(self):
        # Show the name of the item followed by stock status
        stock_status = "Out of Stock" if self.quantity == 0 else f"Available: {self.quantity}"
        return f"{self.name} - {stock_status}"

    def get_discounted_price(self):
        """Calculates and returns the price after applying the discount."""
        if self.discount:
            discount_amount = (self.price * self.discount) / 100
            discounted_price = self.price - discount_amount
            return round(discounted_price, 2)
        return self.price

    def purchase_item(self, quantity_to_purchase):
        """Deducts the purchased quantity from the available stock."""
        if self.quantity >= quantity_to_purchase:
            self.quantity -= quantity_to_purchase
            self.save()
            return True
        return False

