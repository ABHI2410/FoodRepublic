## Change NO_OF_CORES for increasing performance only if CPU has more than 4 cores 


import requests
from bs4 import BeautifulSoup
import json
import sqlite3
import time

__master_data = {
}
__master_session = requests.Session()
def crawl(master_session,master_data,url):
    print('\n trying to crawl:',url)
    try:
        res = master_session.get(url)
    except:
        print("No network")
        time.sleep(30)
        crawl(master_session,master_data,url)
    soup = BeautifulSoup(res.content,'html.parser')
    prices = soup.findAll("span",attrs={'class':'bQEAj'})
    names = soup.findAll("div",attrs={'itemprop':"name"})
    res_name = soup.find("h1").text
    data = soup.find("div",attrs = {'class':'_1BpLF'})
    all_data = data.get_text("''").split("'")
    all_data = list(filter(lambda a: a != '', all_data))
    all_data = list(filter(lambda a: a != ' ', all_data))
    city_name = url.split('-')
    city = city_name[-2]
    first = all_data[0]
    if (first[0:5] == 'Opens' or first[0:6] == 'Closed' or first[0:10] == 'Restaurant' or first[0:6] == 'Closes'):
        cusine = all_data[1]
        address = all_data[2]
        ratings = all_data[3]
        no_of_ratings = all_data[4]
        price_for_two = all_data[8]
    else:
        cusine = all_data[0]
        address = all_data[1]
        ratings = all_data[2]
        no_of_ratings = all_data[3]
        price_for_two = all_data[7]

    try:
        data = { names[i].text:prices[i].text for i in range(len(prices))}
        master_data[res_name] = data
        file = open(f"./dump/{res_name}.json","w")
        file.write(json.dumps(data))
        file.close()
    except Exception as e:
        print(e)    
    try:
        con = sqlite3.connect('main.db')
        cur = con.cursor()
        for i in range(len(prices)):
            cur.execute('insert into menu values (?,?,?)',(res_name,names[i].text,prices[i].text,))
        cur.execute('insert into resturants values (?,?,?,?,?,?,?)',(res_name,cusine,address,city,ratings,no_of_ratings,price_for_two,))
        con.commit()
        con.close()
    except Exception as e:
        print(e)
    
    

file = open("final.txt","r")
lines = [line.strip() for line in file.readlines()]
file.close()


from multiprocessing import Pool

def f(line):
    crawl(__master_session,__master_data,line)
    return f"DONE {line}"

if __name__ == '__main__':
    NO_OF_CORES = 2
    with Pool(NO_OF_CORES) as p:
        print(p.map(f, lines))
    file = open(f"./dump/test1.json","w")
    file.write(json.dumps(__master_data))
    file.close()
