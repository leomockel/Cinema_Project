import requests, csv
from bs4 import BeautifulSoup
import re
import pandas as pd
from scraper_function import *

df = pd.read_excel('to_scrap.xlsx')
imdb_id = df["imdb"].values
movies = []
for movie in imdb_id:
    movies.append(movie_imdb(movie))

columns_name = ["imdb_id", "vu", "à voir", "title", "original_title", "year", "director", "casting", "genres", "duration", "country", "language", \
"writers", "production", "synopsis", "rating", "num_rate", "budget", "income"]

result = pd.DataFrame(movies, columns = columns_name)

result.to_csv("movies_scraped.csv")
