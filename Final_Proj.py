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

    all_lists = list(zip(lst1,lst2,lst3))
    return all_lists

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def setUpRelease(all_lists, cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Ratings (title TEXT PRIMARY KEY, year TEXT, rating INTEGER)")

    for x in all_lists[0:25]:
        title = x[0]
        year = x[1]
        rating = x[2]
        cur.execute("INSERT INTO Ratings (title, year, rating) VALUES(?, ?, ?)", (title, year, rating))
    conn.commit()



def get_average_release_date(cur):
    total_tv = 0
    cur.execute("SELECT dates FROM Ratings")
    find = cur.fetchall()
    for x in find:
        total_tv += 1
    
    sums = 0
    cur.execute("SELECT release_date FROM Ratings")
    for x in cur.fetchall():
        for y in x:
            sums += y
    average_release_date = str(sums/total_tv)
    return average_release_date 

def file_average_ratings(year,file):
    r = os.path.dirname(file)
    file = open(os.path.join(r, file), "w")
    with open(file) as f:
        csv.writer(file, delimiter=",", quotechar='"')
        file.write('Average Year: ')
        file.write(year)
    print("The average release date of the top 250 movies is around "+year+" years.")




