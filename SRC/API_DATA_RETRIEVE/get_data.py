import requests

from utils.connect_to_db import mysql_connect, mysql_disconnect

db_code = "DbMysql26"

example_tmdb_api_request = "https://api.themoviedb.org/3/movie/550?api_key=c722ee1702b642f1eb03bbbb186ea45b"


def insert_to_movies(movie, conn):
    cursor = conn.cursor()
    movie_collection_id = movie.get('belongs_to_collection')
    movie_collection_id = movie_collection_id.get("id") if movie_collection_id else "NULL"
    insert_stmt = f"""INSERT IGNORE INTO DbMysql26.movies VALUES 
    ({movie.get('id',"NULL")}, '{movie.get('imdb_id', "NULL")}','{movie.get('title',"NULL")}', {movie_collection_id},
    {movie.get('budget',"NULL")},
    {movie.get('revenue',"NULL")},
    {movie.get('popularity',"NULL")}, 
    '{movie.get('status')}',
    {movie.get('vote_count',"NULL")},
    {movie.get('vote_average',"NULL")},
    '{movie.get('release_date')}', {movie.get('runtime',"NULL")},'{movie.get('tagline',"NULL")}')"""
    cursor.execute(insert_stmt)
    conn.commit()


def insert_production_country(movie, conn):
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


def insert_production_company(movie, conn):
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


def insert_to_movie_genres(movie, conn):
    cursor = conn.cursor()
    movie_id = movie['id']
    curr_movie_genres = movie['genres']
    for genre in curr_movie_genres:
        insert_stmt = f"""INSERT IGNORE INTO DbMysql26.movie_genres (movie_id, genre_id) VALUES ({movie_id}, {genre['id']})"""
        cursor.execute(insert_stmt)
        conn.commit()

def insert_to_collections(movie, conn):
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

def add_genres(tmdb_api_key, conn):
    api_request = f"https://api.themoviedb.org/3/genre/movie/list?api_key={tmdb_api_key}&language=en-US"
    response = requests.get(api_request)
    cursor = conn.cursor()
    genres = response.json()['genres']
    for genre in genres:
        insert_stmt = f"""INSERT IGNORE INTO DbMysql26.genres (id, name) VALUES ({genre['id']}, '{genre['name']}')"""
        cursor.execute(insert_stmt)
        conn.commit()
    print(cursor.rowcount, "Record inserted successfully into genres table")


def add_movie_related_info(tmdb_api_key, conn):
    for movie_id in range(74, 20000): #STARTED FROM 62
        api_request = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={tmdb_api_key}&language=en-US"
        response = requests.get(api_request)
        movie = response.json()
        if not movie.get('id'):
            continue
        insert_to_collections(movie,conn)
        insert_to_movies(movie, conn)
        insert_to_movie_genres(movie, conn)
        insert_production_company(movie, conn)
        insert_production_country(movie,conn)
        print(f"added movie {movie_id}")


if __name__ == '__main__':
    tmdb_api_key = "c722ee1702b642f1eb03bbbb186ea45b"
    conn = mysql_connect()
    add_movie_related_info(tmdb_api_key, conn)
    mysql_disconnect(conn)
