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
			msg='Your Order has been Successfully placed, You can Track your Order in kamar1000.pythonanywhere.com Tracker section, Your OrderID is {}'.format(order.id)
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
	prod=Product.objects.get(id=prodid)
	prodimg=None
	if prod.prodimg:	
		prodimg=ProductImage.objects.filter(product__id=prodid)
	feature=prod.feature.split("\n")
	return render(request,'dexmart/productview.html',{"prod":prod,"prodsimg":prodimg,"features":feature})

def search_for_keyword(key,data):	#key=[samsung,32gb,phone]
	count=0		#data=samsung standard edition 32gb smartphone
	for query in key:
		if query in data.name or query in data.category or query in data.subcate or query in data.desc:
			count+=1
	return count
def search_for_price(price,data):
	if int(data.price) <= int(price):
		return True
	return False
def search(request):
	keys=request.POST['keyword'].lower()
	key=keys.split(' ')
	print(key)
	price=request.POST.get('price',"")
	products=Product.objects.all()
	result={}
	prods=[]
	i=0.1
	for prod in products:
		count=search_for_keyword(key,prod)
		if count:
			if len(key)>1:
				if count in result:
					result[count-i]=prod
					i+=0.1
				else:
					result[count]=prod
			else:prods.append(prod)
	if len(key)>1:
		l=sorted(result.keys(),reverse=True)
		for i in l:
			prods.append(result[i])
	print(result)
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
	return render(request,'dexmart/search.html',{"notfound":False,"prods":prods,"keyword":keys,"prc":prc,"price":price})

def category(request,cat=""):
	products=Product.objects.all()
	prods=[]
	for prod in products:
		if cat in prod.category or cat in prod.subcate:
			prods.append(prod)
	return render(request,'dexmart/category.html',{"prods":prods})

 