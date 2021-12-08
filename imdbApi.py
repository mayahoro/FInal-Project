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
    #parameters = {'apiKey': key, 'limit': 25}
    parameters = {'apiKey': key}
    url = 'https://imdb-api.com/en/API/Top250Movies/'
    response = requests.get(url, params=parameters).json()
    #dct = response['items']
    #print(dct)
    #return dct
    return response

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


def setUpMoviesTable(data, cur, conn):
    cur.execute('DROP TABLE IF EXISTS Movies')
    cur.execute('CREATE TABLE IF NOT EXISTS "Movies"("title" TEXT PRIMARY KEY, "rank" TEXT, "year" TEXT, "imDbRating" TEXT)')
    for movie in data['items']:
        title = movie['title']
        rank = movie['rank']
        year = movie['year']
        imDbRating = movie['imDbRating']
        cur.execute('SELECT rank from Movies WHERE title = ?', (title,))
        cur.execute('INSERT OR IGNORE INTO Movies (title, rank, year, imDbRating) VALUES (?,?,?,?)', (title, rank, year, imDbRating))
    conn.commit()

#find the average imDb Rating
def getAvgRating(data, cur, conn):
    sums = 0
    ratings = cur.execute('SELECT imDbRating from Movies')
    lst_of_ratings = list(ratings)
    for i in lst_of_ratings:
        num = float(i[0])
        sums += num
    avg = sums / len(lst_of_ratings)
    return avg

#get a dictionary of years and how many times it was in the top 250 movies
def getDictOfYears(data, cur, conn):
    years = cur.execute('SELECT year from Movies')
    lst = list(years)
    lst_of_years = []
    year_frequency = {}
    for i in lst:
        lst_of_years.append(int(i[0]))
    for i in lst_of_years:
        if i not in year_frequency:
            year_frequency[i] = 1
        else:
            year_frequency[i] += 1
    year_frequency_sorted = sorted(year_frequency.items(), key=lambda x: x[1], reverse=True)

    print(year_frequency_sorted[:14])
    
    return year_frequency_sorted[:14]
    #print(lst_of_years)

#def barchart_year_and_frequency(dictionary):
    #for i in dictionary:
     #   years = i[0]
    #    freq = i[1]
   # plt.bar(years, freq,alpha=1)
  #  plt.xticks(, rotation = 90)
  #  plt.ylabel('Frequency of Year')
  #  plt.xlabel('Year')
   # plt.title('Amount of Times a Movie in the Top 250 Movies was in a Certain Year')
  #  plt.tight_layout()
   # plt.show()
    


def main():
    json_data = Top250('k_401budis')
    cur, conn = setUpDatabase('movies.db')
    setUpMoviesTable(json_data, cur, conn)
    getAvgRating(json_data, cur, conn)
    dct = getDictOfYears(json_data, cur, conn)
    #barchart_year_and_frequency(dct)
    conn.close()


if __name__ == "__main__":
    main()