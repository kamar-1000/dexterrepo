from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from dexmart.models import Product,Carousel,Order,OrderUpdate,Contact,ProductImage
import json 
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.
def home(request):
	prods=Product.objects.all()
	rated_prod=[]
	for prod in prods:
		if prod.toprated:
			rated_prod.append(prod)
	cats=[]
	for prod in prods:
		if prod.category not in cats:
			cats.append(prod.category)
	carousel=Carousel.objects.all()
	return render(request,'dexmart/home.html',{"prods":rated_prod,"cats":cats,"carousel":carousel,"range":range(1,len(carousel))})

def about(request):
	return render(request,'dexmart/about.html')

def tracker(request): 
	if request.method == "POST":
		try:
			orderid=int(request.POST['orderid'])
			email=request.POST['email']
		except:
			return JsonResponse ({"error":True})
		if Order.objects.filter(id=orderid,email=email).exists():
			order=Order.objects.filter(id=orderid,email=email)
			order=order[0]
			orderupdate=OrderUpdate.objects.filter(updateid=orderid)
			userdata={
			"name":order.name,"email":order.email,"address":order.address,"state":order.state,"city":order.city,"pincode":order.pincode,"tel":order.tel
			}
			orderitem=json.loads(order.orderdata)
			orderupdates={}
			count=1
			for update in orderupdate:
				orderupdates["update{}".format(count)]=[update.updatedesc,update.updatetime]
				count+=1
			#{"userdata":userdata,"orderitem":orderitem,"orderupdates":orderupdates}

			return JsonResponse({"userdata":userdata,"orderupdates":orderupdates,"orderdata":orderitem})#"orderitem":orderitem,"orderupdates":orderupdates})
		return JsonResponse ({"error":True})
	return render(request,'dexmart/tracker.html')

def cart(request):
	return render(request,'dexmart/cart.html')

def checkout(request):
	if request.method == 'POST':
		name=request.POST['name']
		email=request.POST['email']
		city=request.POST['city']
		state=request.POST['state']
		pincode=request.POST['pincode']
		address=request.POST['address']
		tel=request.POST['tel']
		orderdata=request.POST['orderdata']
		order=Order(name=name,email=email,city=city,state=state,pincode=pincode,address=address,tel=tel,orderdata=orderdata)
		order.save()
		orderupdate=OrderUpdate(updateid=order.id,updatedesc="Your Order Has Been Placed Successfully")
		orderupdate.save()
		
		try:
			subject='Dexmart - Thank you for purchasing product'
			msg='Your Order has been Successfully placed, You can Track your Order in Dexmart.com Tracker section, Your OrderID is {}'.format(order.id)
			email_from=settings.EMAIL_HOST_USER
			recipient_list=[email]
			send_mail(subject,msg,email_from,recipient_list)
			return redirect("/home")
		except:
			print("sending email error")
			return redirect("/home")
	return render(request,'dexmart/checkout.html')

def product(request):
	return render(request,'dexmart/product.html')

def contact(request):
	if request.method == "POST":
		name=request.POST['name']
		email=request.POST['email']
		tel=request.POST['tel']
		comment=request.POST['comment']
		print("post exe")
		contact=Contact(name=name,email=email,tel=tel,comment=comment)
		contact.save()
		return redirect("/home")
	return render(request,'dexmart/contact.html')

def productview(request,prodid):
	prodimg=ProductImage.objects.filter(product__id=prodid)
	prod=prodimg[0]
	feature=prod.product.feature.split("\n")
	return render(request,'dexmart/productview.html',{"prod":prod,"prodsimg":prodimg,"features":feature})

def search_for_keyword(key,data):
	if key in data.name or key in data.category or key in data.subcate or key in data.desc:
		return True
	return False
def search_for_price(price,data):
	if int(data.price) <= int(price):
		return True
	return False
def search(request):
	key=request.POST['keyword'].lower()
	price=request.POST.get('price',"")
	prods=[]
	products=Product.objects.all()
	for prod in products:
		if search_for_keyword(key,prod):
			prods.append(prod)
	prc=False
	if not price == "":
		prc=True
		prods2=[]
		for prod in prods:
			if search_for_price(price,prod):
				prods2.append(prod)
		del prods
		prods=prods2
	if prods==[]:
		return render(request,'dexmart/search.html',{"notfound":True})		
	return render(request,'dexmart/search.html',{"notfound":False,"prods":prods,"keyword":key,"prc":prc,"price":price})

def category(request,cat=""):
	products=Product.objects.all()
	prods=[]
	for prod in products:
		if cat in prod.category or cat in prod.subcate:
			prods.append(prod)
	return render(request,'dexmart/category.html',{"prods":prods})

