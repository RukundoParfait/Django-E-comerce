from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Product(models.Model):
    name=models.CharField(max_length=500)
    category=models.CharField(max_length=300)
    price=models.FloatField()
    digital=models.BooleanField(default=False, null=True, blank=True)
    image=models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url=self.image.url
        except:
            url=''
        return url
    
class Order(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    completed=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.customer}'s order"

    @property
    def get_cart_total(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.IntegerField(default=0, null=True, blank=True)
    order=models.ForeignKey(Order, on_delete=models.CASCADE)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} {self.product}(s)"
    
    @property
    def get_total(self):
        return self.product.price*int(self.quantity)

class ShippingAdress(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    order=models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    firstname=models.CharField(max_length=200)
    lastname=models.CharField(max_length=200)
    city=models.CharField(max_length=200)
    country=models.CharField(max_length=200)
    phone=models.CharField(max_length=200)
    email=models.EmailField(max_length=200)
    
    def __str__(self):
        return f"{self.city},{self.country} to {self.firstname} {self.lastname}"