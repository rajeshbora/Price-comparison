from tkinter import *
from tkinter import Scrollbar
from bs4 import BeautifulSoup
import requests
import webbrowser
from selenium import webdriver

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
# import manan as m
flipkart_url=""
ebay_url=""
croma_url=""
amazon_url=""
olx_url=""

opts = webdriver.FirefoxOptions()
opts.headless = True
driver = webdriver.Firefox(options=opts)

searching = False

def flipkart(name):
    try:
        global flipkart_url
        name1 = name.replace(" ", "+")
        flipkart_url=f'https://www.flipkart.com/search?q={name1}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off'
        res = requests.get(flipkart_url, headers=headers)

        soup = BeautifulSoup(res.text,'html.parser')

        # For single keyword search
        if soup.find("a", class_ = "s1Q9rs") != None:
            flipkart_name = soup.select('.s1Q9rs')[0].getText().strip()
        # If search keyword is more than one word
        elif soup.find("div", class_ ="_4rR01T") != None:
            flipkart_name = soup.select('._4rR01T')[0].getText().strip()

        flipkart_price = soup.select('._30jeq3')[0].getText().strip()  

        return f"{flipkart_name}\nPrice : {flipkart_price}\n"
    except:

        flipkart_price= 'Product Not Found'
    return flipkart_price

def amazon(name):
    try:
        global amazon_url
        name1 = name.replace(" ","+")
        amazon_url=f'https://www.amazon.in/s?k={name1}'
        res = requests.get(amazon_url,headers=headers)

        soup = BeautifulSoup(res.text,'html.parser')
        amazon_page = soup.select('.a-color-base.a-text-normal')
        amazon_price = ""
        amazon_page_length = int(len(amazon_page))
        for i in range(0,amazon_page_length):
            name = name.upper()
            amazon_name = soup.select('.a-color-base.a-text-normal')[i].getText().strip().upper()
            if name in amazon_name[0:20]:
                amazon_name = soup.select('.a-color-base.a-text-normal')[i].getText().strip().upper()
                amazon_price = soup.select('.a-price-whole')[i].getText().strip().upper()

                break
        if amazon_price != "":
            return f"{amazon_name}\nPrise : {amazon_price}\n"
    except:
        amazon_price = "Product Not Found"
    
    if amazon_price == "":
        amazon_price = "Product Not Found"

    return amazon_price



def ebay(name):
    try:
        global ebay_url
        name1 = name.replace(" ","+")
        ebay_url=f'https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw={name1}&_sacat=0'

        driver.get(ebay_url)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        ebay_title = ""
        ebay_price = ""
        all_divs = soup.find_all('li', {'class' : 's-item s-item__pl-on-bottom'})

        for divs in all_divs:
            title = divs.find('div', {'class' : 's-item__title'}).text
            titleUpper = title.upper()

            if name.upper() in titleUpper[:30]:
                ebay_title = title
                ebay_price = divs.find('div', {'class':'s-item__detail s-item__detail--primary'}).text
                break

        if ebay_price != "":
            return f"{ebay_title}\nPrice :{ebay_price}\n"
    except Exception as e:
        print(e)
        ebay_price = 'Product Not Found'

    if ebay_price == "":
        ebay_price = 'Product Not Found'
        
    return ebay_price


def croma(name):
    try:
        global croma_url
        name1 = name.replace(" ","+")
        croma_url=f'https://www.croma.com/search/?text={name1}'

        driver.get(croma_url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        croma_price = ""
        croma_title = ""
        list_of_products= soup.find_all('li',{'class':'product-item'})

        # iterate over the list of products returned
        for list in list_of_products:
            div = list.find('div', {'class':'product-info'})
            title = div.find('h3', {'class':'product-title plp-prod-title'}).text
            titleUpper = title.upper()

            # check if the product is actually what we're looking for
            if name.upper() in titleUpper[:30]:
                croma_price = div.find('span', {'class':'amount'}).text
                croma_title = title 
                break
        
        if croma_price != "":
            return f"{croma_title}\nPrice {croma_price}:\n"
    except Exception as e:
        print(e)
        croma_price = "Product Not Found"

    if croma_price == "":
        croma_price = "Product Not Found"
    return croma_price


def olx(name):
    try:
        global olx_url
        name1 = name.replace(" ","-")
        olx_url=f'https://www.olx.in/items/q-{name1}?isSearchCall=true'

        driver.get(olx_url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        olx_price = ""
        olx_title = ""
        olx_ul = soup.find_all('li', {'class': '_1DNjI'})

        for olx in olx_ul:
            div = olx.find('div', {'class':'fTZT3'})
            title = div.find('span', {'class':'_2poNJ'}).text
            titileUp = title.upper()

            if name.upper() in titileUp[:25]:
                olx_title = title 
                olx_price = div.find('span', {'class':'_2Ks63'}).text
                break

        if olx_price != "":
            return f"{olx_title}\nPrice :{olx_price}\n"
    except Exception as e:
        print(e)
        olx_price = 'Product Not Found'
    
    if olx_price == "":
        olx_price = 'Product Not Found'
        
    return olx_price

def urls():
    global flipkart_url
    global ebay_url
    global croma_url
    global amazon_url
    global olx_url
    return f"{flipkart_url}\n\n\n{ebay_url}\n\n\n{croma_url}\n\n\n{amazon_url}\n\n\n{olx}"



def open_url(event):
        global flipkart_url
        global ebay_url
        global croma_url
        global amazon_url
        global olx_url
        webbrowser.open_new(flipkart_url)
        webbrowser.open_new(ebay_url)
        webbrowser.open_new(croma_url)
        webbrowser.open_new(amazon_url)
        webbrowser.open_new(olx_url)

def search():
    global searching
    search_item = product_name.get()

    if not searching and search_item != "":
        searching = True 
        box1.insert(1.0,"Loding...")
        box2.insert(1.0,"Loding...")
        box3.insert(1.0,"Loding...")
        box4.insert(1.0,"Loding...")
        box5.insert(1.0,"Loding...")
        box6.insert(1.0,"Loding...")

        box1.delete(1.0,"end")
        box2.delete(1.0,"end")
        box3.delete(1.0,"end")
        box4.delete(1.0,"end")
        box5.delete(1.0,"end")
        box6.delete(1.0,"end")
        
        t1=flipkart(search_item)
        box1.insert(1.0,t1)

        t2=ebay(search_item)
        box2.insert(1.0,t2)

        t3=croma(search_item)
        box3.insert(1.0,t3)

        t4=amazon(search_item)
        box4.insert(1.0,t4)

        t5=olx(search_item)
        box5.insert(1.0,t5)

        t6 = urls()
        box6.insert(1.0,t6)

        searching = False 

# reset to defaults 
def clear():
    global searching
    global flipkart_url
    global ebay_url
    global croma_url
    global amazon_url
    global olx_url

    box1.delete(1.0,"end")
    box2.delete(1.0,"end")
    box3.delete(1.0,"end")
    box4.delete(1.0,"end")
    box5.delete(1.0,"end")
    box6.delete(1.0,"end")

    searching = False 
    flipkart_url=""
    ebay_url=""
    croma_url=""
    amazon_url=""
    olx_url=""

    product_name.set("")


window = Tk()
window.wm_title("Price comparison tool")
window.minsize(1500,700)

lable_one =  Label(window, text="Enter Product Name :", font=("courier", 10))
lable_one.place(relx=0.2, rely=0.1, anchor="center")

product_name =  StringVar()
product_name_entry =  Entry(window, textvariable=product_name, width=50)
product_name_entry.place(relx=0.5, rely=0.1, anchor="center")

search_button =  Button(window, text="Search", width=12, command=search)
search_button.place(relx=0.5, rely=0.2, anchor="center")

clear_button = Button(window, text="Clear", width=12, command=clear)
clear_button.place(relx=0.7, rely=0.1, anchor="center")

l1 =  Label(window, text="flipkart", font=("courier", 20))
l2 =  Label(window, text="ebay", font=("courier", 20))
l3 =  Label(window, text="croma", font=("courier", 20))
l4 =  Label(window, text="amazon", font=("courier", 20))
l5 =  Label(window, text="olx", font=("courier", 20))
l6 =  Label(window, text="All urls", font=("courier", 20))
l8 =  Label(window, text="Loding.....", font=("courier", 30))

l1.place(relx=0.1, rely=0.3, anchor="center")
l2.place(relx=0.5, rely=0.3, anchor="center")
l3.place(relx=0.8, rely=0.3, anchor="center")
l4.place(relx=0.1, rely=0.6, anchor="center")
l5.place(relx=0.5, rely=0.6, anchor="center")
l6.place(relx=0.8, rely=0.6, anchor="center")

scrollbar = Scrollbar(window)
box1 =  Text(window, height=7, width=50, yscrollcommand=scrollbar.set)

box2 =  Text(window, height=7, width=50, yscrollcommand=scrollbar.set)

box3 =  Text(window, height=7, width=50, yscrollcommand=scrollbar.set)

box4 =  Text(window, height=7, width=50, yscrollcommand=scrollbar.set)

box5 =  Text(window, height=7, width=50, yscrollcommand=scrollbar.set)


box1.place(relx=0.2, rely=0.4, anchor="center")
box2.place(relx=0.5, rely=0.4, anchor="center")
box3.place(relx=0.8, rely=0.4, anchor="center")
box4.place(relx=0.2, rely=0.7, anchor="center")
box5.place(relx=0.5, rely=0.7, anchor="center")

box6 =  Text(window, height=15, width=50, yscrollcommand=scrollbar.set, fg="blue", cursor="hand2")
box6.place(relx=0.8, rely=0.8, anchor="center")
box6.bind("<Button-1>", open_url)


window.mainloop()