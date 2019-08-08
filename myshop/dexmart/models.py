from django.db import models

# Create your models here.

class Product(models.Model):
	name=models.CharField(max_length=200)
	price=models.IntegerField()
	category=models.CharField(max_length=200)
	subcate=models.CharField(max_length=100)
	pubdate=models.DateField()
	description=models.BooleanField(default=False)
	desc=models.TextField(blank=True)
	keyfeatures=models.BooleanField(default=True)
	feature=models.TextField(blank=True)
	toprated=models.BooleanField(default=False)
	stock=models.BooleanField(default=False)
	image=models.ImageField(upload_to="dexmart/prod_img")
	deliveryby=models.DateField()
	rating=models.FloatField(default="",choices=((2.5,2.5),(2.8,2.8),(3.4,3.4),(3.5,2.5),(4.2,4.2),(4.4,4.4),(4.6,4.6),(4.8,4.8),(4.9,4.9)))
	brand=models.CharField(max_length=100)
	code=models.CharField(max_length=100)
	stock=models.BooleanField(default=True)
	prodimg=models.BooleanField(default=False)
	def __str__(self):
		return self.name
class ProductImage(models.Model):
	product=models.ForeignKey(Product,on_delete=models.CASCADE)
	image=models.ImageField(upload_to="dexmart/prod_img")
	imgtext=models.TextField(default="")
	def __str__(self):
		return self.product.name
class Carousel(models.Model):
	caption=models.CharField(max_length=100)
	name=models.CharField(max_length=100)
	image=models.ImageField(upload_to="dexmart/carousel_item")
	def __str__(self):
		return self.name

class Order(models.Model):
	orderdata=models.TextField()
	name=models.CharField(max_length=100)
	email=models.EmailField()
	state=models.CharField(max_length=100)
	city=models.CharField(max_length=100)
	pincode=models.IntegerField()
	address=models.CharField(max_length=200)
	tel=models.CharField(max_length=30)
	def __str__(self):
		return self.name

class OrderUpdate(models.Model):
	updateid=models.IntegerField()
	updatedesc=models.CharField(max_length=200)
	updatetime=models.DateField(auto_now_add=True)
	def __str__(self):
		return str(self.updateid)+"	"+self.updatedesc

class Contact(models.Model):
	name=models.CharField(max_length=100)
	email=models.EmailField()
	tel=models.CharField(max_length=30)
	comment=models.TextField(default="")
	def __str__(self):
		return self.name
