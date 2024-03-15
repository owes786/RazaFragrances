from django.db import models
from accounts.models import User
from tinymce.models import HTMLField
from datetime import date

# Create your models here.
CATEGORY_CHOICE = (
    ('Attar', 'Attar'),
    ('Perfume', 'Perfume'),
    ('Deodent', 'Deodent'),
)

STOCK_CHOICE = (
    ('in stock', 'in stock'),
    ('out of stock', 'out of stock'),
)

class Product(models.Model):
    Title = models.CharField(max_length = 250)
    Mrp = models.FloatField()
    Selling_Price = models.FloatField()
    Description = models.TextField()
    Brand = models.CharField(max_length = 250, null = True)
    Category = models.CharField(choices = CATEGORY_CHOICE, max_length = 50)
    Stock = models.CharField(choices = STOCK_CHOICE, null = True, max_length = 250)
    Product_Image = models.ImageField(upload_to='image/', max_length=300, null=True, default=None)

def __str__(self):
    return str(self.id)

def __str__(self):
    return str(self.Title)


# ------------------------------------------------------------------------------------------------------------------

class Review(models.Model):
    user = models.ForeignKey(User, on_delete  = models.CASCADE)
    Product = models.ForeignKey(Product, on_delete  = models.CASCADE)
    Review_Description = models.TextField()
    image = models.ImageField(upload_to="ReviewImages/", max_length=300, null=True, default=None)
    Date = models.DateField(("Date"), default=date.today, null = True)



# ------------------------------------------------------------------------------------------------------------------

STATE_CHOICE = (
    ('Select State','Select State'),
    ('Andhra Pradesh','Andhra Pradesh'),
    ('Arunachal Pradesh','Arunachal Pradesh'),
    ('Assam','Assam'),
    ('Bihar','Bihar'),
    ('Chhattisgarh','Chhattisgarh'),
    ('Goa','Goa'),
    ('Gujarat','Gujarat'),
    ('Haryana','Haryana'),
    ('Himachal Pradesh','Himachal Pradesh'),
    ('Jharkhand','Jharkhand'),
    ('Karnataka','Karnataka'),
    ('Kerala','Kerala'),
    ('Madhya Pradesh','Madhya Pradesh'),
    ('Maharashtra','Maharashtra'),
    ('Manipur','Manipur'),
    ('Meghalaya','Meghalaya'),
    ('Mizoram','Mizoram'),
    ('Nagaland','Nagaland'),
    ('Odisha','Odisha'),
    ('Punjab','Punjab'),
    ('Rajasthan','Rajasthan'),
    ('Sikkim','Sikkim'),
    ('Tamil Nadu','Tamil Nadu'),
    ('Telangana','Telangana'),
    ('Tripura','Tripura'),
    ('Uttar Pradesh','Uttar Pradesh'),
    ('Uttarakhand','Uttarakhand'),
    ('West Bengal','West Bengal'),
    ('Amravati','Amravati'),
)

class Customer_Details(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    Name = models.CharField(max_length = 250)
    Mobile_Number = models.IntegerField()
    Pincode = models.IntegerField()
    City = models.CharField(max_length = 250, null = True)
    Address = models.TextField()
    State = models.CharField(choices = STATE_CHOICE, max_length = 250 ,default = 'State')
    Landmark = models.CharField(max_length = 250)

def __str__(self):
    return str(self.id)

#------------------------------------------------------------------------------------------------------------------

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, null=True)
    Product = models.ForeignKey(Product, on_delete = models.CASCADE, null=True)


#-----------------------------------------------------------------------------------------------------------------

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    Product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField(default = 1)

def __str__(self):
    return str(self.id)


#-----------------------------------------------------------------------------------------------------------------

class Buy_now_model(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    Product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField(default = 1)

def __str__(self):
    return str(self.id)


# -----------------------------------------------------------------------------------------------------------------
ORDER_STATUS = (
    ('Placed','Placed'),
    ('Shipped','Shipped'),
    ('Out for Delevery','Out for Delevery'),
    ('Delevered','Delevered'),
)


class OrderDetails(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    Product = models.ForeignKey(Product, on_delete = models.CASCADE, null = True)

    Title = models.CharField(max_length = 250, null=True)
    Mrp = models.FloatField(null=True)
    Selling_Price = models.FloatField(null=True)
    Quantity = models.IntegerField(null = True)
    Total_Amount = models.FloatField(null=True)
    Product_Image = models.ImageField(upload_to='image/', max_length=300, null=True, default=None)
    Razorpay_Order_id = models.CharField(max_length = 250, null=True)
    Razorpay_Payment_id = models.CharField(max_length = 250, null=True)
    Razorpay_signature = models.CharField(max_length = 250, null=True)
    Prepaid = models.BooleanField(db_default = False)

    Name = models.CharField(max_length = 250, null=True)
    Mobile_Number = models.CharField(null=True, max_length=12)
    Pincode = models.CharField(null=True, max_length=100)
    City = models.CharField(max_length = 250, null = True)
    Address = models.TextField(null = True)
    State = models.CharField(choices = STATE_CHOICE, max_length = 250 ,default = 'State', null=True)

    Landmark = models.CharField(max_length = 250, null=True)
    OrderDate = models.DateField(("Date"), default=date.today, null = True)
    Status = models.CharField(choices = ORDER_STATUS, default ='Placed', max_length= 250)
