
import sqlite3


# Create your views here.

def home():
	con = sqlite3.connect("../main.db")
	cur = con.cursor()
	cur.execute('select name,cusine,ratings,price_for_two from resturants where city = "mumbai" AND ratings > "4.5" AND ratings != "--"',)
	data = cur.fetchall()
	print(len(data))
	print(data)


home()
	


