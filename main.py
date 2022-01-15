import requests, csv
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
from collections import OrderedDict
from scraper import movie_imdb
from data_scrap import getting_datas
from update_db import update_db
import os
import sqlalchemy as db
import psycopg2

if __name__ == '__main__':
    getting_datas()
    update_db()
