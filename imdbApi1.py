from bs4 import BeautifulSoup
import requests
import os
import json
import csv
import unittest
import sqlite3
import matplotlib
import matplotlib.pyplot as plt

def Top250(key):
    parameters = {'apiKey': key}
    url = 'https://imdb-api.com/en/API/Top250Movies/'
    response = requests.get(url, params=parameters).json()
    dct = response['items']
    return dct[:100]

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def setUpMoviesTable(data, cur, conn):
    title_lst = []
    rank_lst = []
    year_lst = []
    imdb_lst = []
    Director_lst = []
    for movie in data:
        title = movie['title']
        title_lst.append(title)
        rank = movie['rank']
        rank_lst.append(rank)
        year = movie['year']
        year_lst.append(year)
        imDbRating = movie['imDbRating']
        imdb_lst.append(imDbRating)
        dirr = movie['crew']
        Director = dirr.split('(dir.)')[0]
        Director_lst.append(Director)
    cur.execute('''CREATE TABLE IF NOT EXISTS Movies(title TEXT, rank TEXT, year TEXT, imDbRating TEXT, Director TEXT)''')
    count = 0
    for i in range(len(title_lst)):
        if count > 24:
            break
        if cur.execute('SELECT rank FROM Movies WHERE title = ? AND rank = ? AND year = ? AND imDbRating = ? AND Director = ?', (title_lst[i], rank_lst[i], year_lst[i], imdb_lst[i], Director_lst[i])).fetchone() == None:
            cur.execute('INSERT INTO Movies (title, rank, year, imDbRating, Director) VALUES (?,?,?,?,?)', (title_lst[i], rank_lst[i], year_lst[i], imdb_lst[i], Director_lst[i]))  
            count += 1
    conn.commit()

def main():
    json_data = Top250('k_401budis')
    cur, conn = setUpDatabase('movies.db')
    setUpMoviesTable(json_data, cur, conn)
    conn.close()

if __name__ == "__main__":
    main()