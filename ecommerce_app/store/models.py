from django.db import models
import datetime
from django.contrib.auth.models import User

# Product Category (Electronics, Clothes, etc.)
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Meta:
    verbose_name_plural = 'categories'

# Product (belongs to a Category)
class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    description = models.TextField(max_length=250, default=0,blank=True, null=True)
    image = models.ImageField(upload_to='uploads/product/', blank=True, null=True)
    # add sale stuff
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    def __str__(self):
        return self.name

# Order (when a user checks out)
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    address = models.CharField(max_length=100, default='', blank=True)
    phone = models.CharField(max_length=12, default='',blank=True)
    quantity = models.IntegerField(default=1)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.product

# Customer
class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=12)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
