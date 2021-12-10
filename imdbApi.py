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
    dct = response['items']
    #print(dct[:100])
    return dct[:100]
    #print(response)
    #return response

def getDirectors(key):
    top_dir = Top250(key)
    director_list = []
    for dir in top_dir:
        directors = dir['crew']
        #print(directors.split('(dir.)')[0])
        director_list.append(directors.split('(dir.)')[0])
    #print(director_list)
    return director_list

def countDirectors(directors):
    lst_of_directors = []
    director_frequency = {}
    for i in directors:
        lst_of_directors.append(i)
    for i in lst_of_directors:
        if i not in director_frequency:
            director_frequency[i] = 1
        else:
            director_frequency[i] += 1
    #print(director_frequency)
    return director_frequency


def director_pie(director_frequency):
    directors = []
    frequency = []
    for x, y in director_frequency.items():
        directors.append(x)
        frequency.append(y)
    plt.pie(frequency[:14], labels=directors[:14],radius=5,labeldistance=0.45,startangle=90,rotatelabels =True,counterclock=False)
    plt.title('Amount of Times a Director has Directed a Movie in the Top 250 Movies')
    plt.axis('equal')
    plt.show()
 


def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


def setUpMoviesTable(data, cur, conn):
    cur.execute('DROP TABLE IF EXISTS Movies')
    cur.execute('CREATE TABLE IF NOT EXISTS "Movies"("title" TEXT PRIMARY KEY, "rank" TEXT, "year" TEXT, "imDbRating" TEXT, "Director" TEXT)')
    #for movie in data['items']:
    #dir = []
    for movie in data:
        title = movie['title']
        rank = movie['rank']
        year = movie['year']
        imDbRating = movie['imDbRating']
        dirr = movie['crew']
        Director = dirr.split('(dir.)')[0]
        cur.execute('SELECT rank from Movies WHERE title = ?', (title,))
        cur.execute('INSERT OR IGNORE INTO Movies (title, rank, year, imDbRating, Director) VALUES (?,?,?,?,?)', (title, rank, year, imDbRating, Director))  
        cur.execute("SELECT * FROM Movies LIMIT 25")
       # for row in cur:
           # print(row[:25])

   #cur.execute('DROP TABLE IF EXISTS Cast and Crew')
    #cur.execute('CREATE TABLE IF NOT EXISTS "Cast and Crew"("crew" TEXT PRIMARY KEY')
           
    conn.commit()

def setUpDirectorsTable(director_dict, cur, conn):
    cur.execute('DROP TABLE IF EXISTS Directors')
    cur.execute('CREATE TABLE IF NOT EXISTS "Directors"("Director" TEXT PRIMARY KEY, "Appearance" TEXT)')
    for key, value in director_dict.items():
        cur.execute('INSERT INTO Directors (Director, Appearance) VALUES (?,?)', (key,value))
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

    #print(year_frequency_sorted[:14])
    
    return year_frequency_sorted[:14]
    #print(lst_of_years)

def barchart_year_and_frequency(dictionary):
    x, y = zip(*dictionary)
    plt.bar(x, y,alpha=1)
    plt.xticks(x, rotation = 45)
    plt.ylabel('Frequency of Year')
    plt.xlabel('Year')
    plt.title('Amount of Times a Movie in the Top 250 Movies was in a Certain Year')
    plt.tight_layout()
    plt.show()
    



def main():
    json_data = Top250('k_26f33bxj')
    directors = getDirectors('k_26f33bxj')
    director_dict = countDirectors(directors)
    cur, conn = setUpDatabase('movies.db')
    setUpMoviesTable(json_data, cur, conn)
    setUpDirectorsTable(director_dict, cur, conn)
    getAvgRating(json_data, cur, conn)
    dct = getDictOfYears(json_data, cur, conn)
    barchart_year_and_frequency(dct)
    director_pie(director_dict)
    conn.close()


if __name__ == "__main__":
    main()