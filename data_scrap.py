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
    actor = list(movie_keep[6].values)
    actor_code = list(movie_keep[7].values)
    actor_status = list(movie_keep[8].values)
    genres = list(movie_keep[9].values)
    duration = list(movie_keep[10].values)
    country = list(movie_keep[11].values)
    language = list(movie_keep[12].values)
    production = list(movie_keep[13].values)
    prod_code = list(movie_keep[14].values)
    synopsis = list(movie_keep[15].values)
    rating = list(movie_keep[16].values)
    num_rate = list(movie_keep[17].values)
    budget = list(movie_keep[18].values)
    bud_currency = list(movie_keep[19].values)
    saw = ["" for i in range(len(imdb))]
    db_saw = [False for i in range(len(imdb))]


    # change the currency of the budget in dollars
    changer = {"$":1, "€":1.17, "£":1.37}
    def_budget = [changer[bud_currency[i]]*budget[i] if budget[i] != "" else "" for i in range(len(budget))]

    # transform lists to concatenated strings for selection_film
    category = [actor, country, director, genres, language, production]

    temp_cat = []
    new_val = []

    for i in range(len(category)):
        for j in range(len(category[i])):
            temp_cat.append(" | ".join(category[i][j]))
        new_val.append(list(temp_cat))
        temp_cat = []

    actor_new = new_val[0]
    country_new = new_val[1]
    director_new = new_val[2]
    genre_new = new_val[3]
    language_new = new_val[4]
    production_new = new_val[5]

    select_data = {"imdb_id": imdb, "vu": saw, "à voir": saw, "title": title, "original_title": original_title, \
               "year": year,"director": director_new, "casting": actor_new, "genres": genre_new, \
               "duration": duration,"country": country_new, "language": language_new, "production": production_new, \
               "synopsis": synopsis, "rating": rating, "num_rate": num_rate, "budget": def_budget}
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

    # create genre codes
    genre_df = pd.read_csv("db_backup/genre_db.csv")
    genre_code = [genre_df.genre_id.values[list(genre_df.name.values).index(genres[i][j])] \
                 for i in range(len(genres)) for j in range(len(genres[i]))]

    # update movie_genre_db
    genre_imdb = [imdb[i] for i in range(len(imdb)) for j in range(len(genres[i]))]

    movie_genre_data = {"movie_id": genre_imdb, "genre_id": genre_code}
    up_movie_genre = pd.DataFrame(movie_genre_data)
    up_movie_genre = up_movie_genre.drop(up_movie_genre[up_movie_genre["genre_id"] == ""].index).set_index("movie_id")
    up_movie_genre.to_csv("update_db/up_movie_genre.csv")

    # update actors and movie_actor
    act_db = pd.read_csv(f'db_backup/actor_db.csv')
    act_id_db = list(act_db.actor_id)

    cast_imdb = [imdb[i] for i in range(len(imdb)) for j in range(len(actor_code[i]))]
    all_actors = [actor[i][j] for i in range(len(imdb)) for j in range(len(actor[i]))]
    all_codes = [actor_code[i][j] for i in range(len(imdb)) for j in range(len(actor_code[i]))]
    all_status = [actor_status[i][j] for i in range(len(imdb)) for j in range(len(actor_status[i]))]

    movie_actor = {"movie_id": cast_imdb, "actor_id": all_codes, "name": all_actors, "status": all_status}
    movie_actor_df = pd.DataFrame(movie_actor)
    movie_actor_df = movie_actor_df.drop(movie_actor_df[movie_actor_df["actor_id"] == ""].index)
    movie_actor_df = movie_actor_df.drop(movie_actor_df[movie_actor_df["status"] == "U"].index)
    movie_actor_df = movie_actor_df.drop_duplicates()
    movie_actor_df.drop(["name"], axis=1).set_index("movie_id").to_csv("update_db/up_movie_actor.csv")

    actors_df = movie_actor_df.drop(["movie_id", "status"], axis=1).drop_duplicates()
    act_id = []
    act_name = []
    for i in range(len(actors_df.actor_id.values)):
        if actors_df.actor_id.values[i] not in act_id_db:
            act_id.append(actors_df.actor_id.values[i])
            act_name.append(actors_df.name.values[i])

    new_act_col = {"actor_id": act_id, "name": act_name}
    new_actors = pd.DataFrame(new_act_col)
    new_actors.set_index("actor_id").to_csv("update_db/up_actor.csv")

    # update all the other variables
    total_var = [country, language, director, production]
    var_name = ["country", "language", "director", "production"]
    var_code_list = [dir_code, dir_code, dir_code, prod_code]
    col_name = ["country", "language", "director", "prod"]
    up_file = ["country", "language", "dir", "prod"]

    # 1- import backup and set max_id
    for i in range(len(var_name)):
        var_df = pd.read_csv(f'db_backup/{var_name[i]}_db.csv')
        code_db = list(var_df.iloc[:,0])
        name_db = list(var_df.iloc[:,1])
        if i < 2:
            max_id = max(code_db)

    # 2- check if a data in the scrap is not in the database
        up_name = []
        up_code = []
        for j in range(len(total_var[i])):
            for k in range(len(total_var[i][j])):
                if i < 2 and total_var[i][j][k] not in name_db and total_var[i][j][k] != "":
                    up_name.append(total_var[i][j][k])
                    up_code.append(max_id + 1)
                    max_id += 1
                elif i >= 2 and var_code_list[i][j][k] not in code_db:
                    up_name.append(total_var[i][j][k])
                    up_code.append(var_code_list[i][j][k])

   # 3- create update dataframe
        data_col = {col_name[i]+"_id": up_code, "name": up_name}
        up_var = pd.DataFrame(data_col).set_index(col_name[i]+"_id")
        up_df = pd.concat([var_df, up_var]).drop_duplicates()


        if len(up_var) > 0:
            up_var.to_csv(f"update_db/up_{var_name[i]}.csv")

    # 4- create codes for scraped movies
        if i < 2 :
            var_code = [int(up_df[f"{col_name[i]}_id"].values[list(up_df.name.values).index(total_var[i][j][k])]) \
                        for j in range(len(total_var[i])) for k in range(len(total_var[i][j]))]
            var_imdb = [imdb[j] for j in range(len(imdb)) for k in range(len(total_var[i][j]))]
        else :
            var_imdb = [imdb[j] for j in range(len(imdb)) for k in range(len(var_code_list[i][j]))]
            var_code = [var_code_list[i][j][k] for j in range(len(imdb)) for k in range(len(var_code_list[i][j]))]

    # 5- create many to many relationship
        movie_var_data = {"movie_id": var_imdb, f"{col_name[i]}_id": var_code}
        up_movie_var = pd.DataFrame(movie_var_data)
        up_movie_var = up_movie_var.drop(up_movie_var[up_movie_var[f"{col_name[i]}_id"] == ""].index).set_index("movie_id")
        up_movie_var = up_movie_var.drop_duplicates()
        up_movie_var.to_csv(f"update_db/up_movie_{up_file[i]}.csv")
