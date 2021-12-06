from bs4 import BeautifulSoup
import requests
import os
import json
import csv
import unittest
import sqlite3
import matplotlib
import matplotlib.pyplot as plt

def get_data(filename):
    f = open('nv_tvv_250.html', 'r')
    read = f.read()
    soup = BeautifulSoup(read, 'html.parser')
    lst1 = []
    
    titles = soup.find_all('a', class_= 'title')
    for t in titles:
        lst1.append(t.text.strip())

    lst2 = []
    rating = soup.find_all('td', class_= 'imdbRating')
    for r in rating:
        lst2.append(r.text.strip())

    lst3 = []
    rank = soup.find_all('span', class_= 'secondaryInfo')
    for x in rank:
        lst3.append(x.text.strip())

    return list(zip(lst1,lst2,lst3))

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


def get_average_release_date(curr):
    pass