from scraper import movie_imdb
import pandas as pd

def getting_datas():
    # import movies to scrap
    df = pd.read_csv('movies_to_scrap/scrap_it.csv')
    imdb_id = df["imdb"].values

    # import movies in database
    db_df = pd.read_csv('db_backup/movies_db.csv')
    imdb_db = db_df["imdb_id"].values

    # keep only movies not in the database
    final_imdb = [i for i in imdb_id if i not in imdb_db]
    final_imdb = list(set(final_imdb))

    # scraping
    movies = [movie_imdb(movie) for movie in final_imdb]
    movie_df = pd.DataFrame(movies)

    # keep movies with a rating (the other are probably not available)
    movie_keep = movie_df.drop(movie_df[movie_df[3] == ""].index)
    too_soon = pd.DataFrame(movie_df[[0,1]].drop(movie_df[movie_df[3] != ""].index).values, \
                columns= ['imdb_id', 'title'])

    # save scraped movies with no ratings
    if len(too_soon) > 0:
        f_scrap = pd.read_csv('movies_to_scrap/too_soon.csv').set_index("imdb_id")
        f_scrap_df = pd.DataFrame(f_scrap, columns= ['imdb_id', 'title'])
        too_soon = pd.concat([f_scrap_df, too_soon]).set_index("imdb_id")
        too_soon.to_csv('movies_to_scrap/too_soon.csv')

    # convert data in lists
    imdb = list(movie_keep[0].values)
    title = list(movie_keep[1].values)
    original_title = list(movie_keep[2].values)
    year = list(movie_keep[3].values)
    director = list(movie_keep[4].values)
    dir_code = list(movie_keep[5].values)
    actors = list(movie_keep[6].values)
    actor_code = list(movie_keep[7].values)
    genres = list(movie_keep[8].values)
    duration = list(movie_keep[9].values)
    country = list(movie_keep[10].values)
    language = list(movie_keep[11].values)
    production = list(movie_keep[12].values)
    prod_code = list(movie_keep[13].values)
    synopsis = list(movie_keep[14].values)
    rating = list(movie_keep[15].values)
    num_rate = list(movie_keep[16].values)
    budget = list(movie_keep[17].values)
    bud_currency = list(movie_keep[18].values)
    saw = ["" for i in range(len(imdb))]
    db_saw = [False for i in range(len(imdb))]

    ## create the update country_db file

    # 1- import countries in database
    state_df = pd.read_csv('db_backup/country_db.csv')
    code_state = list(state_df.country_id.values)
    countries = list(state_df.name.values)
    max_country_id = max(code_state)

    # 2- check if a country in the scrap is not in the database
    update_state = []
    update_state_code = []
    for i in range(len(country)):
        for j in range(len(country[i])):
            if country[i][j] not in countries and country[i][j] != "":
                update_state.append(country[i][j])
                update_state_code.append(max_country_id + 1)
                max_country_id += 1

    # 3- create update dataframe
    state_data = {"country_id": update_state_code, "name": update_state}
    up_country = pd.DataFrame(state_data).set_index("country_id")
    country_df = pd.concat([state_df, up_country])

    # 4- create country_codes for scraped movies
    country_code = [int(country_df.country_id.values[list(country_df.name.values).index(country[i][j])]) \
                    for i in range(len(country)) for j in range(len(country[i]))]

    # 5- save updates of country if exists
    if len(up_country) > 0:
        up_country.to_csv("update_db/up_country.csv")


    ## create the update language_db file

    # 1- import language in database
    lan_df = pd.read_csv('db_backup/language_db.csv')
    code_lan = list(lan_df.language_id.values)
    lan = list(lan_df.name.values)
    max_language_id = max(code_lan)

    # 2- check if a language in the scrap is not in the database
    update_lan = []
    update_lan_code = []
    for i in range(len(language)):
        for j in range(len(language[i])):
            if language[i][j] not in lan and language[i][j] != "":
                update_lan.append(language[i][j])
                update_lan_code.append(max_language_id + 1)
                max_language_id += 1

    # 3- create update dataframe
    lan_data = {"language_id": update_lan_code, "name": update_lan}
    up_language = pd.DataFrame(lan_data).set_index("language_id")
    language_df = pd.concat([lan_df, up_language])

    # 4- create language_codes for scraped movies
    language_code = [int(language_df.language_id.values[list(language_df.name.values).index(language[i][j])]) \
                     for i in range(len(language)) for j in range(len(language[i]))]

    # 5- save updates of language if exists
    if len(up_language) > 0:
        up_language.to_csv("update_db/up_language.csv")

    # create genre_code
    genre_df = pd.read_csv("db_backup/genre_db.csv")
    genre_code = [genre_df.genre_id.values[list(genre_df.name.values).index(genres[i][j])] \
                 for i in range(len(genres)) for j in range(len(genres[i]))]

    # change the currency of the budget in dollars
    changer = pd.read_excel("currency_change.xlsx")
    def_budget = ["" if bud_currency[i] == "" else int(budget[i] * changer["Change"]\
                  .values[list(changer.Currencies.values).index(bud_currency[i])]) \
                  for i in range(len(bud_currency))]

    # transform lists to concatenated strings for selection_film
    dict_dir = {}
    dict_cast = {}
    dict_genre = {}
    dict_country = {}
    dict_language = {}
    dict_prod = {}

    temp_dir = []
    temp_cast = []
    temp_genre = []
    temp_country = []
    temp_language = []
    temp_prod = []

    ids = imdb[0]
    for i in range(len(imdb)):
        for j in range(len(director[i])):
            if ids == imdb[i]:
                temp_dir.append(director[i][j])
            elif ids != imdb[i]:
                dict_dir[ids] = " | ".join(temp_dir)
                ids = imdb[i]
                temp_dir = []
                temp_dir.append(director[i][j])
        dict_dir[ids] = " | ".join(temp_dir)

    ids = imdb[0]
    for i in range(len(imdb)):
        for j in range(len(cast[i])):
            if ids == imdb[i]:
                temp_cast.append(cast[i][j])
            elif ids != imdb[i]:
                dict_cast[ids] = " | ".join(temp_cast)
                ids = imdb[i]
                temp_cast = []
                temp_cast.append(cast[i][j])
        dict_cast[ids] = " | ".join(temp_cast)

    ids = imdb[0]
    for i in range(len(imdb)):
        for j in range(len(genres[i])):
            if ids == imdb[i]:
                temp_genre.append(genres[i][j])
            elif ids != imdb[i]:
                dict_genre[ids] = " | ".join(temp_genre)
                ids = imdb[i]
                temp_genre = []
                temp_genre.append(genres[i][j])
        dict_genre[ids] = " | ".join(temp_genre)

    ids = imdb[0]
    for i in range(len(imdb)):
        for j in range(len(country[i])):
            if ids == imdb[i]:
                temp_country.append(country[i][j])
            elif ids != imdb[i]:
                dict_country[ids] = " | ".join(temp_country)
                ids = imdb[i]
                temp_country = []
                temp_country.append(country[i][j])
        dict_country[ids] = " | ".join(temp_country)

    ids = imdb[0]
    for i in range(len(imdb)):
        for j in range(len(language[i])):
            if ids == imdb[i]:
                temp_language.append(language[i][j])
            elif ids != imdb[i]:
                dict_language[ids] = " | ".join(temp_language)
                ids = imdb[i]
                temp_language = []
                temp_language.append(language[i][j])
        dict_language[ids] = " | ".join(temp_language)

    ids = imdb[0]
    for i in range(len(imdb)):
        for j in range(len(production[i])):
            if ids == imdb[i]:
                temp_prod.append(production[i][j])
            elif ids != imdb[i]:
                dict_prod[ids] = " | ".join(temp_prod)
                ids = imdb[i]
                temp_prod = []
                temp_prod.append(production[i][j])
        dict_prod[ids] = " | ".join(temp_prod)

    # put data in a DataFrame and save
    select_data = {"imdb_id": imdb, "vu": saw, "à voir": saw, "title": title, "original_title": original_title, \
                   "year": year, "director": list(dict_dir.values()), "casting": list(dict_cast.values()), \
                   "genres": list(dict_genre.values()), "duration": duration, \
                   "country": list(dict_country.values()), "language": list(dict_language.values()), \
                   "production": list(dict_prod.values()), "synopsis": synopsis, "rating": rating, \
                   "num_rate": num_rate, "budget": def_budget}

    select = pd.DataFrame(select_data).set_index("imdb_id")
    select.to_csv("movies_scraped.csv")

    # update movies_db
    movie_data = {"imdb_id": imdb, "french_title": title, "original_title": original_title, "year": year, \
                   "duration": duration, "rating": rating, "num_rate": num_rate, "budget": def_budget, \
                   "synopsis": synopsis}
    up_movies = pd.DataFrame(movie_data).set_index("imdb_id")
    up_movies.to_csv("update_db/up_movies.csv")

    # update user_db
    user_data = {"movie_id": imdb, "saw": db_saw, "wishlist": db_saw}
    up_user = pd.DataFrame(user_data).set_index("movie_id")
    up_user.to_csv("update_db/up_user.csv")

    # update actor_db

    actor_df = pd.read_csv('db_backup/actor_db.csv')
    code_actor = list(actor_df.actor_id.values)

    update_cast_code = []
    update_cast = []

    for i in range(len(cast_code)):
        for j in range(len(cast_code[i])):
            if cast_code[i][j] not in code_actor:
                update_cast_code.append(cast_code[i][j])
                update_cast.append(cast[i][j])
                code_actor.append(cast_code[i][j])

    actor_data = {"actor_id": update_cast_code, "name": update_cast}
    up_actor = pd.DataFrame(actor_data)
    up_actor = up_actor.drop(up_actor[up_actor["actor_id"] == ""].index).set_index("actor_id")

    if len(update_cast) > 0:
        up_actor.to_csv("update_db/up_actor.csv")

    # update director_db

    dir_df = pd.read_csv('db_backup/director_db.csv')
    code_dir = list(dir_df.director_id.values)

    update_dir_code = []
    update_dir = []

    for i in range(len(dir_code)):
        for j in range(len(dir_code[i])):
            if dir_code[i][j] not in code_dir:
                update_dir_code.append(dir_code[i][j])
                update_dir.append(director[i][j])
                code_dir.append(dir_code[i][j])

    dir_data = {"director_id": update_dir_code, "name": update_dir}
    up_dir = pd.DataFrame(dir_data)
    up_dir = up_dir.drop(up_dir[up_dir["director_id"] == ""].index).set_index("director_id")

    if len(update_dir) > 0:
        up_dir.to_csv("update_db/up_dir.csv")

    # update production_db

    prod_df = pd.read_csv('db_backup/production_db.csv')
    code_prod = list(prod_df.prod_id.values)

    update_prod_code = []
    update_prod = []

    for i in range(len(prod_code)):
        for j in range(len(prod_code[i])):
            if prod_code[i][j] not in code_prod:
                update_prod_code.append(prod_code[i][j])
                update_prod.append(production[i][j])
                code_prod.append(prod_code[i][j])

    prod_data = {"prod_id": update_prod_code, "name": update_prod}
    up_prod = pd.DataFrame(prod_data)
    up_prod = up_prod.drop(up_prod[up_prod["prod_id"] == ""].index).set_index("prod_id")

    if len(update_prod) > 0:
        up_prod.to_csv("update_db/up_prod.csv")

    # update movie_actor_db

    cast_imdb = [imdb[i] for i in range(len(imdb)) for j in range(len(cast_code[i]))]
    all_actor = [cast_code[i][j] for i in range(len(imdb)) for j in range(len(cast_code[i]))]

    movie_cast_data = {"movie_id": cast_imdb, "actor_id": all_actor}
    up_movie_actor = pd.DataFrame(movie_cast_data)
    up_movie_actor = up_movie_actor.drop(up_movie_actor[up_movie_actor["actor_id"] == ""].index).set_index("movie_id")
    up_movie_actor.to_csv("update_db/up_movie_actor.csv")

    # update movie_dir_db

    dir_imdb = [imdb[i] for i in range(len(imdb)) for j in range(len(dir_code[i]))]
    all_dir = [dir_code[i][j] for i in range(len(imdb)) for j in range(len(dir_code[i]))]

    movie_dir_data = {"movie_id": dir_imdb, "director_id": all_dir}
    up_movie_dir = pd.DataFrame(movie_dir_data)
    up_movie_dir = up_movie_dir.drop(up_movie_dir[up_movie_dir["director_id"] == ""].index).set_index("movie_id")
    up_movie_dir.to_csv("update_db/up_movie_dir.csv")

    # update movie_prod_db

    prod_imdb = [imdb[i] for i in range(len(imdb)) for j in range(len(prod_code[i]))]
    all_prod = [prod_code[i][j] for i in range(len(imdb)) for j in range(len(prod_code[i]))]

    movie_prod_data = {"movie_id": prod_imdb, "prod_id": all_prod}
    up_movie_prod = pd.DataFrame(movie_prod_data)
    up_movie_prod = up_movie_prod.drop(up_movie_prod[up_movie_prod["prod_id"] == ""].index).set_index("movie_id")
    up_movie_prod.to_csv("update_db/up_movie_prod.csv")

    # update movie_genre_db

    genre_imdb = [imdb[i] for i in range(len(imdb)) for j in range(len(genres[i]))]

    movie_genre_data = {"movie_id": genre_imdb, "genre_id": genre_code}
    up_movie_genre = pd.DataFrame(movie_genre_data)
    up_movie_genre = up_movie_genre.drop(up_movie_genre[up_movie_genre["genre_id"] == ""].index).set_index("movie_id")
    up_movie_genre.to_csv("update_db/up_movie_genre.csv")


    # update movie_country_db

    country_imdb = [imdb[i] for i in range(len(imdb)) for j in range(len(country[i]))]

    movie_country_data = {"movie_id": country_imdb, "country_id": country_code}
    up_movie_country = pd.DataFrame(movie_country_data)
    up_movie_country = up_movie_country.drop(up_movie_country[up_movie_country["country_id"] == ""].index).set_index("movie_id")
    up_movie_country.to_csv("update_db/up_movie_country.csv")

    # update movie_language_db

    language_imdb = [imdb[i] for i in range(len(imdb)) for j in range(len(language[i]))]

    movie_language_data = {"movie_id": language_imdb, "language_id": language_code}
    up_movie_language = pd.DataFrame(movie_language_data)
    up_movie_language = up_movie_language.drop(up_movie_language[up_movie_language["language_id"] == ""].index).set_index("movie_id")
    up_movie_language.to_csv("update_db/up_movie_language.csv")
