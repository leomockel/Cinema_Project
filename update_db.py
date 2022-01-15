import sqlalchemy as db
import psycopg2
import pandas as pd
import os


def update_db():

    # set dictionnary with name of database in csv as key, and value is a list containing name of the update file for database,
    # name of the column to set index and name of the database on SQL, to make the update
    dict_file = {"movies_db":["up_movies", "imdb_id", "movies"], "actor_db":["up_actor", "actor_id", "actors"], \
                 "country_db":["up_country", "country_id", "country"], "director_db":["up_director", "director_id", "directors"], \
                 "genre_db":["up_genre", "genre_id", "genres"], "language_db":["up_language", "language_id", "language"], \
                 "production_db":["up_production", "prod_id", "production"], "movie_actor_db_2":["up_movie_actor", "movie_id", "movie_actor"], \
                 "movie_country_db":["up_movie_country", "movie_id", "movie_country"], "movie_dir_db":["up_movie_dir", "movie_id", "movie_director"], \
                 "movie_genre_db":["up_movie_genre", "movie_id", "movie_genre"], "movie_language_db":["up_movie_language", "movie_id", "movie_language"], \
                 "movie_prod_db":["up_movie_prod", "movie_id", "movie_prod"], "user_list_db":["up_user", "movie_id", "user_list"]}


    # connection to the database
    DATABASE_URL = "postgresql+psycopg2://postgres:root@localhost:5432/cinema_db"
    engine = db.create_engine(DATABASE_URL)
    connection = engine.connect()

    # update of the database on CSV, SQL an suppression of the update file
    for key, value in dict_file.items():
        if os.path.isfile(f"update_db/{value[0]}.csv"):
            database = pd.read_csv(f"db_backup/{key}.csv").set_index(value[1])
            up = pd.read_csv(f"update_db/{value[0]}.csv").set_index(value[1])
            up.to_sql(value[2], engine, if_exists="append")
            pd.concat([database, up]).to_csv(f"db_backup/{key}.csv")
            #os.remove(f"update_db/{value[0]}.csv")
