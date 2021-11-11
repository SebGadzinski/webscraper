import tkinter.ttk

import requests
from bs4 import BeautifulSoup
import pandas as pd
from tkinter import *
from subprocess import Popen
from sys import platform
import os

main_list = []
list_of_businesses_unwanted = ['Tim Hortons', 'McDonalds', 'Starbucks']

def extract(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup.find_all('div', class_ = 'listing_right_section')

def transform(articles):
    for item in articles:
        name = item.find('h3', {'itemprop': 'name'}).text.strip('\n')
        if name in list_of_businesses_unwanted:
            continue
        address = item.find('span', {'itemprop': 'address'}).text.strip().replace('\n', '')
        try:
            website = item.find('li', class_ = 'mlr__item mlr__item--website').find("a", "mlr__item__cta")['href']
        except:
            website = ''
        try:
            tel = item.find('a', class_ = 'mlr__item__cta jsMlrMenu')['data-phone']
        except:
            tel = ''

        business = {
            'name': name,
            'address': address,
            'website': website,
            'tel': tel
        }
        main_list.append(business)
    return

def load():
    df = pd.DataFrame(main_list)
    print("Finish Grabbing")
    df.to_csv('buisnesses.csv', index=False)
    if platform == "darwin":
        os.startfile('buisnesses.csv')
    else:
        Popen('buisnesses.csv', shell=True)

def loadInfoForCSV(buisness, city, province):
    buisness_URL = buisness.replace(' ', "+").title()
    for x in range(1,9):
        print(f'Getting page {x}')
        articles = extract(f'https://www.yellowpages.ca/search/si/{x}/{buisness_URL}/{city.title()}+{province.title()}')
        if len(articles) > 0:
            transform(articles)
    load()
    print('Saved to CSV')

window = Tk()
window.title("Welcome to TutorialsPoint")
window.configure(background="grey");
window.rowconfigure(2)
window.columnconfigure(2)

buisnessLabel = Label(window, text="Business").grid(row=0, column=0, sticky=tkinter.NSEW)
cityLabel = Label(window, text="City").grid(row=1, column=0, sticky=tkinter.NSEW)
provinceLabel = Label(window, text="Province").grid(row=2, column=0, sticky=tkinter.NSEW)

buisnessInput = Entry(window)
buisnessInput.grid(row=0, column=1, sticky=tkinter.NSEW)
buisnessInput.insert(0, "Coffee Shops")
buisnessInput.bind("<FocusIn>", lambda args: buisnessInput.delete('0', 'end'))

cityInput = Entry(window)
cityInput.grid(row=1, column=1, sticky=tkinter.NSEW)
cityInput.insert(0, "City")
cityInput.bind("<FocusIn>", lambda args: cityInput.delete('0', 'end'))

provinceInput = tkinter.ttk.Combobox(window, values=["NS", "QC", "ON", "MB", "SK", "AB", "BC", "NT", "NB", "NB", "YT", "PE", "NU"])
provinceInput.grid(row=2, column=1, sticky=tkinter.NSEW)
provinceInput.current(2)

def clicked():
    loadInfoForCSV(buisnessInput.get(), cityInput.get(), provinceInput.get())

btn = tkinter.Button(window, text="Send To CSV", command=clicked).grid(row=3, column=0, columnspan = 2, sticky = tkinter.W+tkinter.E)

window.mainloop()

