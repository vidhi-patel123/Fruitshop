from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=10)
    otp = models.IntegerField(default=1234)

    def __str__(self):
        return self.email
    
class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=20)
    message = models.TextField(max_length=1000)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Add_product(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    category_id=models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    price = models.IntegerField()
    qty = models.IntegerField()
    pic = models.ImageField(upload_to='img')
    dec = models.TextField()

    def __str__(self):
        return self.name
    
class Add_to_cart(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    product_id = models.ForeignKey(Add_product,on_delete=models.CASCADE)
    pic = models.ImageField()
    name = models.CharField(max_length=25)
    price = models.IntegerField()
    qty = models.IntegerField()
    total_price=models.IntegerField()

    def __str__(self):
        return self.name

class Address(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=10)
    user_name = models.CharField(max_length=10)
    email = models.EmailField()
    address = models.TextField()
    address_2 = models.TextField()
    country = models.CharField(max_length=10)
    state = models.CharField(max_length = 10)
    pincode = models.IntegerField()
    list = models.TextField()

    def __str__(self):
        return self.first_name
    
class Add_to_wishlist(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    product_id = models.ForeignKey(Add_product,on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    price = models.IntegerField()
    pic = models.ImageField(upload_to='img')
    
    def __str__(self):
        return self.name
    
class Order(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    product_id = models.ForeignKey(Add_product,on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    price = models.IntegerField()
    qty = models.IntegerField()
    total_price = models.IntegerField()
    pic = models.ImageField(upload_to='img')
    
    def __str__(self):
        return self.name
    
class Category_Gallery(models.Model):
    # category_id=models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
class Category_Product(models.Model):
    # product_id = models.ForeignKey(Add_product,on_delete=models.CASCADE)
    G_id = models.ForeignKey(Category_Gallery,on_delete=models.CASCADE)
    pic = models.ImageField(upload_to='img')
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    