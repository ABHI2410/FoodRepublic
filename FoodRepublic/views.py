from django.shortcuts import render,redirect
from django.http import HttpResponse
import sqlite3
from django.contrib import messages 
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required



# Create your views here.

def home(request):
	con = sqlite3.connect("main.db")
	cur = con.cursor()
	cur.execute('select name,cusine,ratings,price_for_two from resturants where city = "mumbai" AND ratings > "4.5" AND ratings != "--"',)
	data = cur.fetchall()
	datas = []
	for num in data:
		if num not in datas:
			datas.append(num)
	
	return render(request,'FoodRepublic/Homepage.html',{ 'datas':datas })

def register(request):
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request,f'Account Created for {username} !')
			return redirect('login')
	else:
		form = UserRegistrationForm()
	return render(request,'FoodRepublic/register.html',{'form':form})

def rest(request,rest_name):
	con = sqlite3.connect("main.db")
	cur = con.cursor()
	cur.execute('select * from resturants where name like ?',(rest_name,))
	data = cur.fetchall()
	cur.execute('select dish,price from menu where name like ?',(rest_name,))
	data2 = cur.fetchall()
	datas = []
	for num in data2:
		if num not in datas:
			datas.append(num)
	length = len(datas)
	context = {
	'data' : data,
	'datas' : datas,
	'length' :length
	}
	return render(request,'FoodRepublic/rest.html',context)


def result(request):
	if request.method == "POST":
		getValue = request.POST["findnow"]
	con = sqlite3.connect("main.db")
	cur = con.cursor()
	cur.execute('select menu.dish,menu.price,resturants.ratings,resturants.name,resturants.address from resturants inner join menu on resturants.name=menu.name where dish like ? AND city like "mumbai"',(getValue,))
	data = cur.fetchall()
	context = { 'data' : data}
	return render(request,'FoodRepublic/result.html',context)

@login_required
def cart(request):
	getValuename,getValue= "",""
	if request.method == 'POST':
		getValue = request.POST["option"]
		value = []
		value = getValue.split(',')
		print(value)
		value.pop(0)
		getValuename = request.POST["rest_name"]
		print(getValuename)
		con = sqlite3.connect("main.db")
		cur = con.cursor()
		final_data = []
		total = 0
		for i in range (len(value)):
			cur.execute('select * from menu where name = ? AND dish = ?',(getValuename,value[i],))
			data = cur.fetchall()
			print(data)
			total += int(data[0][2])
			print(total)
			final_data.append(data[0])
			grand_total = total + 0.05*total
	context = {
	'final_data':final_data,
	'total':total,
	'grand_total':grand_total,

	}
	return render(request,'FoodRepublic/cart.html',context)
	

@login_required
def profile(request):

	return render(request,'FoodRepublic/profile.html')



		