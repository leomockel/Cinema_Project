import sqlalchemy as db
import psycopg2
import pandas as pd
import os


def update_db():

    # connection to the database
    DATABASE_URL = "postgresql+psycopg2://postgres:root@localhost:5432/cinema_db"
    engine = db.create_engine(DATABASE_URL)
    connection = engine.connect()

    # Update movies on sql and csv
    up_movies = pd.read_csv("update_db/up_movies.csv").set_index("imdb_id")
    up_movies.to_sql("movies", engine, if_exists="append")
    movies = pd.read_csv("db_backup/movies_db.csv").set_index("imdb_id")
    pd.concat([movies, up_movies]).to_csv("db_backup/movies_db.csv")

    # Update actors on sql and csv
    if os.path.isfile("update_db/up_actor.csv"):
        actor = pd.read_csv("db_backup/actor_db.csv").set_index("actor_id")
        up_actor = pd.read_csv("update_db/up_actor.csv").set_index("actor_id")
        up_actor.to_sql("actors", engine, if_exists="append")
        pd.concat([actor, up_actor]).to_csv("db_backup/actor_db.csv")

    # Update country on sql and csv
    if os.path.isfile("update_db/up_country.csv"):
        country = pd.read_csv("db_backup/country_db.csv").set_index("country_id")
        up_country = pd.read_csv("update_db/up_country.csv").set_index("country_id")
        up_country.to_sql("country", engine, if_exists="append")
        pd.concat([country, up_country]).to_csv("db_backup/country_db.csv")

    # Update directors on sql and csv
    if os.path.isfile("update_db/up_director.csv"):
        director = pd.read_csv("db_backup/director_db.csv").set_index("director_id")
        up_director = pd.read_csv("update_db/up_dir.csv").set_index("director_id")
        up_director.to_sql("directors", engine, if_exists="append")
        pd.concat([director, up_director]).to_csv("db_backup/director_db.csv")

    # Update language on sql and csv
    if os.path.isfile("update_db/up_language.csv"):
        language = pd.read_csv("db_backup/language_db.csv").set_index("language_id")
        up_language = pd.read_csv("update_db/up_language.csv").set_index("language_id")
        up_language.to_sql("language", engine, if_exists="append")
        pd.concat([language , up_language]).to_csv("db_backup/language_db.csv")

    # Update production on sql and csv
    if os.path.isfile("update_db/up_production.csv"):
        production = pd.read_csv("db_backup/production_db.csv").set_index("prod_id")
        up_production = pd.read_csv("update_db/up_prod.csv").set_index("prod_id")
        up_production.to_sql("production", engine, if_exists="append")
        pd.concat([production, up_production]).to_csv("db_backup/production_db.csv")

    # Update movie_actor on sql and csv
    if os.path.isfile("update_db/up_movie_actor.csv"):
        movie_actor = pd.read_csv("db_backup/movie_actor_db_2.csv").set_index("movie_id")
        up_movie_actor = pd.read_csv("update_db/up_movie_actor.csv").set_index("movie_id")
        up_movie_actor.to_sql("movie_actor", engine, if_exists="append")
        pd.concat([movie_actor, up_movie_actor]).to_csv("db_backup/movie_actor_db_2.csv")

    # Update movie_country on sql and csv
    if os.path.isfile("update_db/up_movie_country.csv"):
        movie_country = pd.read_csv("db_backup/movie_country_db.csv").set_index("movie_id")
        up_movie_country = pd.read_csv("update_db/up_movie_country.csv").set_index("movie_id")
        up_movie_country.to_sql("movie_country", engine, if_exists="append")
        pd.concat([movie_country, up_movie_country]).to_csv("db_backup/movie_country_db.csv")

        if os.path.isfile("update_db/up_movie_dir.csv"):
    # Update movie_director on sql and csv
        movie_dir = pd.read_csv("db_backup/movie_dir_db.csv").set_index("movie_id")
        up_movie_dir = pd.read_csv("update_db/up_movie_dir.csv").set_index("movie_id")
        up_movie_dir.to_sql("movie_director", engine, if_exists="append")
        pd.concat([movie_dir, up_movie_dir]).to_csv("db_backup/movie_dir_db.csv")

    # Update movie_genre on sql and csv
    if os.path.isfile("update_db/up_movie_genre.csv"):
        movie_genre = pd.read_csv("db_backup/movie_genre_db.csv").set_index("movie_id")
        up_movie_genre = pd.read_csv("update_db/up_movie_genre.csv").set_index("movie_id")
        up_movie_genre.to_sql("movie_genre", engine, if_exists="append")
        pd.concat([movie_genre, up_movie_genre]).to_csv("db_backup/movie_genre_db.csv")

    # Update movie_language on sql and csv
    if os.path.isfile("update_db/up_movie_language.csv"):
        movie_language = pd.read_csv("db_backup/movie_language_db.csv").set_index("movie_id")
        up_movie_language = pd.read_csv("update_db/up_movie_language.csv").set_index("movie_id")
        up_movie_language.to_sql("movie_language", engine, if_exists="append")
        pd.concat([movie_language, up_movie_language]).to_csv("db_backup/movie_language_db.csv")

    # Update movie_prod on sql and csv
    if os.path.isfile("update_db/up_movie_prod.csv"):
        movie_prod = pd.read_csv("db_backup/movie_prod_db.csv").set_index("movie_id")
        up_movie_prod = pd.read_csv("update_db/up_movie_prod.csv").set_index("movie_id")
        up_movie_prod.to_sql("movie_prod", engine, if_exists="append")
        pd.concat([movie_prod, up_movie_prod]).to_csv("db_backup/movie_prod_db.csv")

    # Update user_list on sql and csv
    up_users = pd.read_csv("update_db/up_user.csv").set_index("movie_id")
    up_users.to_sql("user_list", engine, if_exists="append")
    users = pd.read_csv("db_backup/user_list_db.csv").set_index("imdb_id")
    pd.concat([users, up_users]).to_csv("db_backup/user_list_db.csv")
