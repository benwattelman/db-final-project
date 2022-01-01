from utils.connect_to_db import mysql_connect, mysql_disconnect


def competition_across_genres(conn):
    query = """SELECT genre, production_company, popularity
                FROM (
                    SELECT production_companies_genres_popularity.GENRE as genre, production_companies_genres_popularity.PRODUCTION_COMPANY_NAME as production_company, production_companies_genres_popularity.production_companies_average_popularity_in_genre as popularity,
                    row_number() over (partition by GENRE order by production_companies_average_popularity_in_genre desc) AS ranking
                    FROM (
                        SELECT g.name as GENRE, pc.name as PRODUCTION_COMPANY_NAME, AVG(m.popularity) as production_companies_average_popularity_in_genre
                        FROM movies as m, production_companies as pc, movies_production_companies as mpc, genres as g, movie_genres as mg
                        WHERE m.id = mpc.movie_id
                        and pc.id = mpc.production_company_id
                        and m.id = mg.movie_id
                        and g.id = mg.genre_id
                        GROUP BY g.id, pc.id) AS production_companies_genres_popularity
                    ) AS ranking_production_companies_genres
                WHERE ranking <= 3
                ORDER BY genre, production_company"""
    cursor = conn.cursor()
    try:
        cursor.execute(query)
    except Exception as e:
        print(f"failed to run the requested query. Error: {e}")
        cursor.close()
        return
    print("genre, production_company, popularity")
    for (genre, production_company, popularity) in cursor:
        print(f"{genre}, {production_company}, {popularity}")
    cursor.close()


def currently_planned_films_across_genres(conn):
    query = """SELECT g.name as GENRE, count(*) as NUMBER_OF_PLANNED_MOVIES
                FROM movies as m, movie_genres as mg, genres as g
                WHERE m.id = mg.movie_id
                and g.id = mg.genre_id
                and (m.status <> "Released")
                GROUP BY g.name
                """
    cursor = conn.cursor()
    try:
        cursor.execute(query)
    except Exception as e:
        print(f"failed to run the requested query. Error: {e}")
        cursor.close()
        return
    print("genre, number of planned movies")
    for (genre, number_planned_movies) in cursor:
        print(f"{genre}, {number_planned_movies}")
    cursor.close()


def best_month_to_release_a_movie(conn):
    query = """SELECT MONTH(m.release_date) as Month, (COUNT(*) / 21) as AverageReleasesPerMonth
                FROM movies as m
                WHERE m.release_date >= "2000-01-01"
                GROUP BY MONTH(m.release_date)
                ORDER BY Month"""
    cursor = conn.cursor()
    try:
        cursor.execute(query)
    except Exception as e:
        print(f"failed to run the requested query. Error: {e}")
        cursor.close()
        return
    print("Month, AverageReleasesPerMonth")
    for (Month, AverageReleasesPerMonth) in cursor:
        print(f"{Month}, {AverageReleasesPerMonth}")
    cursor.close()


def sequel_profitability(conn):
    query = """SELECT collection_name, collection_size, first_movie, first_movie_vote_avg, collection_avg_votes
                FROM
                (SELECT m1.belongs_to_collection as collection_id, m1.title as first_movie, m1.votes_avg as first_movie_vote_avg
                FROM movies as m1
                WHERE m1.release_date <= ALL (
                    SELECT m2.release_date
                    FROM movies as m2
                    WHERE m1.belongs_to_collection = m2.belongs_to_collection)
                ) AS first_movie_per_collection,
                (SELECT c.id as collection_id, c.name as collection_name, AVG(m.votes_avg) as collection_avg_votes, count(*) as collection_size
                FROM movies as m, collections as c
                WHERE m.belongs_to_collection = c.id
                GROUP BY m.belongs_to_collection
                HAVING count(*) > 1) AS collections_averages
                WHERE first_movie_per_collection.collection_id = collections_averages.collection_id
                ORDER BY collection_avg_votes DESC"""
    cursor = conn.cursor()
    try:
        cursor.execute(query)
    except Exception as e:
        print(f"failed to run the requested query. Error: {e}")
        cursor.close()
        return
    print("collection_name, collection_size, first_movie, first_movie_vote_avg, collection_avg_votes")
    for (collection_name, collection_size, first_movie, first_movie_vote_avg, collection_avg_votes) in cursor:
        print(f"{collection_name}, {collection_size}, {first_movie}, {first_movie_vote_avg}, {collection_avg_votes}")
    cursor.close()


def best_filming_locations(conn):
    query = """SELECT pc.name as Country, (SUM(m.revenue) / COUNT(*)) as AverageRevenuePerMovie
            FROM movies as m, movies_production_countries as mpc, production_countries as pc
            WHERE m.id = mpc.movie_id and mpc.country_iso = pc.iso_3166_1
            GROUP BY (pc.name)
            HAVING SUM(m.revenue) > 0
            ORDER BY AverageRevenuePerMovie DESC
            LIMIT 50"""
    cursor = conn.cursor()
    try:
        cursor.execute(query)
    except Exception as e:
        print(f"failed to run the requested query. Error: {e}")
        cursor.close()
        return
    print("Country, AverageRevenuePerMovie")
    for (Country, AverageRevenuePerMovie) in cursor:
        print(f"{Country}, {AverageRevenuePerMovie}")
    cursor.close()


def should_the_catch_phrase_be_a_question(conn):
    query = """SELECT AVG(tq.revenue) as tagline_questions_predicted_revenue,
                AVG(tnq.revenue) as tagline_non_questions_predicted_revenue
                FROM taglines_as_questions as tq, taglines_not_questions as tnq"""
    cursor = conn.cursor()
    try:
        cursor.execute(query)
    except Exception as e:
        print(f"failed to run the requested query. Error: {e}")
        cursor.close()
        return
    print("tagline_questions_predicted_revenue, tagline_non_questions_predicted_revenue")
    for (tagline_questions_predicted_revenue, tagline_non_questions_predicted_revenue) in cursor:
        print(f"{tagline_questions_predicted_revenue}, {tagline_non_questions_predicted_revenue}")
    cursor.close()


def optimize_budget_for_maximal_marginal_revenue(conn):
    query = """SELECT m.budget as BudgetSize, ((SUM(m.revenue) - (m.budget*count(*))) / (m.budget*count(*))) as MarginalRevenue
                FROM movies as m
                WHERE m.budget > 10000
                GROUP BY m.budget
                ORDER BY MarginalRevenue DESC
                LIMIT 10"""
    cursor = conn.cursor()
    try:
        cursor.execute(query)
    except Exception as e:
        print(f"failed to run the requested query. Error: {e}")
        cursor.close()
        return
    print("BudgetSize, MarginalRevenue")
    for (BudgetSize, MarginalRevenue) in cursor:
        print(f"{BudgetSize}, {MarginalRevenue}")
    cursor.close()


if __name__ == '__main__':
    conn = mysql_connect()
    query_functions = [competition_across_genres, currently_planned_films_across_genres, best_month_to_release_a_movie,
                       sequel_profitability, best_filming_locations, should_the_catch_phrase_be_a_question,
                       optimize_budget_for_maximal_marginal_revenue]
    # RUN ALL QUERIES
    for query_function in query_functions:
        print(f"\n\n***{query_function.__name__} - Query Output***\n")
        query_function(conn)
    mysql_disconnect(conn)
