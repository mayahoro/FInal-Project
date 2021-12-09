from bs4 import BeautifulSoup
import requests
import os
import json
import csv
import unittest
import sqlite3
import matplotlib
import matplotlib.pyplot as plt

def getMovies():

    file = open("ultimateMovieRankings.html",'r')
    soup = BeautifulSoup(file,'html.parser')
    file.close()

    titles = []
    search_list = soup.find_all("td", class_="column-2")
    for i in search_list:
        strips = i.text.strip()
        titles.append(strips)

    money = []
    search_lists = soup.find_all("td", class_="column-5")
    for x in search_lists:
        stripss = x.text.strip()
        money.append(stripss)

    money_per_movie = zip(titles,money)
    money_per_movie_dict = dict(money_per_movie)
    return money_per_movie_dict

 
    




def main():
    getMovies()

if __name__ == "__main__":
    main()