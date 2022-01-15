import requests, csv
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
from collections import OrderedDict

def movie_imdb(imdb_id):

    #SELECT SYNOPSIS, GENRES, RATING, NUMBER RATE, YEAR, TITLE, ORIGINAL TITLE, COUNTRY,
    #SELECT LANGUAGE, BUDGET

    r1 = requests.get("https://www.imdb.com/title/"+imdb_id)
    bs = BeautifulSoup(r1.text, "html.parser")

    # Dictionnary for title, orginal_title, rating, num_rate

    info_dict = bs.find('script', {'type': 'application/ld+json'})
    info_dict = info_dict.text
    info_dict = OrderedDict(eval(info_dict))

    original_title = info_dict["name"]

    if original_title.find("&apos;") != -1:
        original_title = original_title.replace("&apos;", "'")

    if original_title.find("&amp") != -1:
        original_title = original_title.replace("&amp", "&")

    try :
        title = info_dict["alternateName"]
    except KeyError:
        title = info_dict["name"]

    if title.find("&amp") != -1:
        title = title.replace("&amp", "&")

    if title.find("&apos;") != -1:
        title = title.replace("&apos;", "'")

    try :
        rating = info_dict['aggregateRating']['ratingValue']
        num_rate = int(info_dict['aggregateRating']['ratingCount'])
    except KeyError:
        rating = ""
        num_rate = ""

    # Info budget bud_currency

    try:
        info_bud = bs.findAll('section', {'data-testid': 'BoxOffice'})
        info_bud = [text.text for text in info_bud][0]
        price = info_bud.split("EditBudget")[1].split(" ")[0]
        budget = int(price[1:].replace(',',''))
        bud_currency = price[0]
    except (IndexError, ValueError):
        budget = ""
        bud_currency = ""


    # Info YEAR

    year = bs.findAll('a', {'class': re.compile('ipc-link')})
    year = int([text.text for text in year][0].strip("– "))

    # Info genres
    genre_bs = bs.findAll('a', {'class': re.compile('ipc-metadata-list-item')})
    genre_bs = [text.text for text in genre_bs]

    genre_list = ["Action", "Adult", "Adventure", "Animation", "Biography", "Comedy", "Crime", "Documentary",
              "Drama", "Family", "Fantasy", "Film-Noir", "History", "Horror", "Music", "Musical", "Mystery",
              "News", "Reality-TV", "Romance", "Sci-Fi", "Short", "Sport", "Thriller", "War", "Western"]

    genres = [genre for genre in genre_bs if genre in genre_list]

    # Info SYNOPSIS
    try :
        syn = bs.findAll('div', {'class': 'ipc-html-content ipc-html-content--base'})[0]
        syn = [text.text for text in syn]
        synopsis = syn[0].split(" —")[0]
    except IndexError:
        synopsis = ""


    countries = bs.findAll('a', {'href': re.compile('country_of_origin')})
    if len(countries) == 0:
        country = ['None']
    else:
        country = ["USA" if text.text == "United States" else "UK" if text.text == "United Kingdom" \
                    else text.text for text in countries]


    language = bs.findAll('a', {'href': re.compile('primary_language')})
    if len(language) == 0:
        language = ["No Info"]
    else :
        language = [text.text for text in language]


    #SELECT CASTING, DIRECTOR, WRITERS

    r2 = requests.get("https://www.imdb.com/title/"+imdb_id+"/fullcredits")
    bs2 = BeautifulSoup(r2.text, "html.parser")

    #select casting
    cast_list = bs2.find_all('table', {'class': 'cast_list'})
    if cast_list == None or cast_list == []:
        cast = [""]
        cast_code = [""]
        cast_voice = [""]
    else :
        cast_list_test = bs2.find('table', {'class': 'cast_list'}).find_all('td', {'class':'primary_photo'})
        cast_list_char = bs2.find('table', {'class': 'cast_list'}).find_all('td', {'class':'character'})
        cast_char = [text.text.strip().replace(' \n', '') for text in cast_list_char]
        if len(cast_list_test) >= 30 :
            cast = [str(cast_list).split('img alt="')[i].split('" class="')[0] for i in range(1,31)]
            cast_code = [str(cast_list_test).split('/name/')[i].split('/">')[0] for i in range(1,31)]
            cast_voice = ["V" if "(voice)" in text else "U" if "uncredited" in text else "" \
                          for text in cast_char[:30]]
        else :
            cast = [str(cast_list).split('img alt="')[i].split('" class="')[0] \
                    for i in range(1,len(cast_list_test)+1)]
            cast_code = [str(cast_list_test).split('/name/')[i].split('/">')[0] \
                          for i in range(1,len(cast_list_test)+1)]
            cast_voice = ["V" if "(voice)" in text else "U" if "uncredited" in text else "" \
                          for text in cast_char[:len(cast_list_test)]]


    #select director
    test_dir = bs2.find('h4', {'id':'director'})
    if test_dir == None:
        director = [""]
        dir_code = [""]
    else :
        direct = bs2.find('table', {'class': 'simpleTable simpleCreditsTable'}) \
                .find_all('td', {'class': 'name'})
        direct_t = [text.text for text in direct]
        director = [i.strip() for i in direct_t]
        dir_code = [(str(direct).split('href="/name/')[i+1]).split('/"> ')[0] for i in range(len(director))]

    #SELECT RUNTIME

    r3 = requests.get("https://www.imdb.com/title/"+imdb_id+"/technical")
    bs3 = BeautifulSoup(r3.text, "html.parser")

    time = bs3.find('table', {'class': 'dataTable labelValueTable'}).find_all('tr', {'class': 'odd'})
    runtime = [text.text for text in time]
    try:
        if ("min (" in (runtime[0].strip())) and (" min)" in (runtime[0].strip())):
            duration = int((runtime[0].strip().split("min (")[1]).split(" min)")[0])
        elif "hr (" in (runtime[0].strip()):
            duration = int((runtime[0].strip().split("hr (")[1]).split(" min)")[0])
        else :
            duration = int((runtime[0].strip().split("Runtime")[1]).split(" min")[0])
    except (ValueError, IndexError):
        duration = ""


    #SELECT PRODUCTION

    r4 = requests.get("https://www.imdb.com/title/"+imdb_id+"/companycredits")
    bs4 = BeautifulSoup(r4.content, "html.parser")
    test = bs4.find('h4', {'id': 'production'})
    if test == None:
        production = [""]
        prod_code = [""]
    else :
        prod_list = bs4.find('ul', {'class': 'simpleList'}).find_all("li")
        prod_t = [text.text.strip() for text in prod_list]
        production = [pro.split("   ")[0] if "   " in pro else pro for pro in prod_t]

        prod_code = [(str(i).split("pany/")[1]).split('">')[0] for i in prod_list]

    if rating != "":
        return imdb_id, title, original_title, year, director, dir_code, cast, cast_code, cast_voice, genres, duration, \
        country, language, production, prod_code, synopsis, rating, num_rate, budget, bud_currency
    else:
        return imdb_id, title,"","","","","","","","","","","","","","","","","", ""
