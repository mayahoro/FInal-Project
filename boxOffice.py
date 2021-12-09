from bs4 import BeautifulSoup
import requests
import os
import json
import csv
import unittest
import sqlite3
import matplotlib
import matplotlib.pyplot as plt

def main():
    json_data = Top250('k_401budis')
    cur, conn = setUpDatabase('movies.db')
    setUpMoviesTable(json_data, cur, conn)
    getAvgRating(json_data, cur, conn)
    dct = getDictOfYears(json_data, cur, conn)
    barchart_year_and_frequency(dct)
    conn.close()


if __name__ == "__main__":
    main()