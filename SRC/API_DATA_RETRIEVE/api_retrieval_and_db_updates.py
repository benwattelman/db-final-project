import asyncio

import aiohttp
import requests

from utils.connect_to_db import mysql_connect, mysql_disconnect

db_code = "DbMysql26"

example_tmdb_api_request = "https://api.themoviedb.org/3/movie/550?api_key=c722ee1702b642f1eb03bbbb186ea45b"


def insert_to_movies(movie, conn):
    """
    a function that takes a movie details dictionary and inserts to the movie table
    :param movie: dictionary with movie details generated from the tmdb json
    :param conn: mysql connection to our DB
    """
    cursor = conn.cursor()
    movie_collection_id = movie.get('belongs_to_collection')
    movie_collection_id = movie_collection_id.get("id") if movie_collection_id else "NULL"
    insert_stmt = f"""INSERT IGNORE INTO DbMysql26.movies VALUES 
    ({movie.get('id', "NULL")}, '{movie.get('imdb_id', "NULL")}','{movie.get('title', "NULL")}', {movie_collection_id},
    {movie.get('budget', "NULL")},
    {movie.get('revenue', "NULL")},
    {movie.get('popularity', "NULL")}, 
    '{movie.get('status')}',
    {movie.get('vote_count', "NULL")},
    {movie.get('vote_average', "NULL")},
    '{movie.get('release_date')}', {movie.get('runtime', "NULL")},'{movie.get('tagline', "NULL")}')"""
    cursor.execute(insert_stmt)
    conn.commit()
    cursor.close()


def insert_production_country(movie, conn):
    """
    a function that takes a movie details dictionary and extracts from it the countries where it was produced
    for each country it inserts it to production_countries table (if it isn't there already)
    also it inserts the relation between the movie and the country into the many-to-many table of movies_production_countries
    :param movie: dictionary with movie details generated from the tmdb json
    :param conn: mysql connection to our DB
    """
    cursor = conn.cursor()
    movie_id = movie['id']
    curr_movie_production_countries = movie['production_countries']
    for country in curr_movie_production_countries:
        try:
            # add company to production_countries table if not exists
            replace_stmt = f"""INSERT IGNORE INTO DbMysql26.production_countries VALUES ('{country['iso_3166_1']}','{country['name']}')"""
            cursor.execute(replace_stmt)
            conn.commit()
        except:
            print(f"failed to update {country.get('name')} country")
        # add company and movie to the many to many relation
        insert_stmt = f"""INSERT IGNORE INTO DbMysql26.movies_production_countries (movie_id, country_iso) VALUES ({movie_id}, '{country['iso_3166_1']}')"""
        cursor.execute(insert_stmt)
        conn.commit()
    cursor.close()


def insert_production_company(movie, conn):
    """
    a function that takes a movie details dictionary and extracts from it the companies that produced it
    for each company it inserts it to production_companies table (if it isn't there already)
    also it inserts the relation between the movie and the company into the many-to-many table of movies_production_companies
    :param movie: dictionary with movie details generated from the tmdb json
    :param conn: mysql connection to our DB
    """
    cursor = conn.cursor()
    movie_id = movie['id']
    curr_movie_production_companies = movie['production_companies']
    for company in curr_movie_production_companies:
        # add company to production_companies table if not exists
        try:
            replace_stmt = f"""INSERT IGNORE INTO DbMysql26.production_companies VALUES ({company['id']},'{company['name']}','{company['origin_country']}' )"""
            cursor.execute(replace_stmt)
            conn.commit()
        except:
            print(f"failed to update {company.get('name')} company")
        # add company and movie to the many to many relation
        insert_stmt = f"""INSERT IGNORE INTO DbMysql26.movies_production_companies (movie_id, production_company_id) VALUES ({movie_id}, {company['id']})"""
        cursor.execute(insert_stmt)
        conn.commit()
    cursor.close()


def insert_to_movie_genres(movie, conn):
    """
    a function that takes a movie details dictionary and extracts from it the movie's genres
    genres table was created using a seperate API endpoint that supplied all the genres at once.
    thus all we need to do is insert the relation between the movie and the genre into the many-to-many table of movie_genres
    :param movie: dictionary with movie details generated from the tmdb json
    :param conn: mysql connection to our DB
    """
    cursor = conn.cursor()
    movie_id = movie['id']
    curr_movie_genres = movie['genres']
    for genre in curr_movie_genres:
        insert_stmt = f"""INSERT IGNORE INTO DbMysql26.movie_genres (movie_id, genre_id) VALUES ({movie_id}, {genre['id']})"""
        cursor.execute(insert_stmt)
        conn.commit()
    cursor.close()


def insert_to_collections(movie, conn):
    """
        a function that takes a movie details dictionary and extracts from it the collection it belongs to
        because the relation between movie to collection is many-to-one we need to insert the collection details
        to the collections table and the movies table will hold the collection id as foreign key.
        that is why we need to call this function before the insert_movie function (in case it is the first movie in the collection)
        :param movie: dictionary with movie details generated from the tmdb json
        :param conn: mysql connection to our DB
    """
    cursor = conn.cursor()
    curr_movie_collection = movie.get('belongs_to_collection')
    movie_collection_id = curr_movie_collection.get("id") if curr_movie_collection else None
    if movie_collection_id:
        # add collection if not exists
        try:
            replace_stmt = f"""INSERT IGNORE INTO DbMysql26.collections VALUES ({curr_movie_collection['id']},'{curr_movie_collection['name']}')"""
            cursor.execute(replace_stmt)
            conn.commit()
        except:
            print(f"failed to update {curr_movie_collection.get('name')} movie_collection")
    cursor.close()


def add_genres(tmdb_api_key, conn):
    """
    a function that uses a seperate API endpoint called genre/movie/list that supplies all the genres at one list.
    thus all we need to do is insert each genre as an entry to genres table
    :param tmdb_api_key: key for api calls to tmdb API
    :param conn: mysql connection to our DB
    """
    api_request = f"https://api.themoviedb.org/3/genre/movie/list?api_key={tmdb_api_key}&language=en-US"
    response = requests.get(api_request)
    cursor = conn.cursor()
    genres = response.json()['genres']
    for genre in genres:
        insert_stmt = f"""INSERT IGNORE INTO DbMysql26.genres (id, name) VALUES ({genre['id']}, '{genre['name']}')"""
        cursor.execute(insert_stmt)
        conn.commit()
    print(cursor.rowcount, "Record inserted successfully into genres table")
    cursor.close()


async def add_movie_related_info():
    """
    the main loop for api retrieval, parsing and inserting the information properly to the db.
    each API call retrieves information about a single movie.
    for the specific movie we first check it has id which is our DB primary key
    if so we start by inserting its collection to collections table
    then we insert its details to movies table
    and afterwards we fill in all the extended information about its connections to countries, genres and companies.
    this function uses async API calls to make the API retrieval process much faster.
    """
    tmdb_api_key = "c722ee1702b642f1eb03bbbb186ea45b"
    conn = mysql_connect()
    add_genres(tmdb_api_key,conn)
    async with aiohttp.ClientSession() as session:
        for movie_id in range(62, 50000):
            api_request = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={tmdb_api_key}&language=en-US"
            async with session.get(api_request) as response:
                movie = await response.json()
                if not movie.get('id'):
                    continue
                insert_to_collections(movie, conn)
                try:
                    insert_to_movies(movie, conn)
                except Exception as e:
                    print(f"failed to add movie {movie_id}. Error: {e}")
                    continue
                insert_to_movie_genres(movie, conn)
                insert_production_company(movie, conn)
                insert_production_country(movie, conn)
                print(f"added movie {movie_id}")
    mysql_disconnect(conn)


if __name__ == '__main__':
    asyncio.run(add_movie_related_info())
