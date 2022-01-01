--------------------------------------------------------------------------------
-- query 1 - competition across genres
SELECT genre, production_company, popularity
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
ORDER BY genre, production_company
--------------------------------------------------------------------------------

--------------------------------------------------------------------------------
-- query 2 - currently planned film across genres
SELECT g.name as GENRE, count(*) as NUMBER_OF_PLANNED_MOVIES
FROM movies as m, movie_genres as mg, genres as g
WHERE m.id = mg.movie_id
and g.id = mg.genre_id
and (m.status <> "Released")
GROUP BY g.name

-- index creation:
CREATE INDEX movie_statuses
ON movies (status)
--------------------------------------------------------------------------------

--------------------------------------------------------------------------------
-- query 3 - best release months
SELECT MONTH(m.release_date) as Month, (COUNT(*) / 21) as AverageReleasesPerMonth
FROM movies as m
WHERE m.release_date >= "2000-01-01"
GROUP BY MONTH(m.release_date)
ORDER BY Month
--------------------------------------------------------------------------------

--------------------------------------------------------------------------------
-- query 4 - sequel profitability
SELECT collection_name, collection_size, first_movie, first_movie_vote_avg, collection_avg_votes
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
ORDER BY collection_avg_votes DESC

-- index creation:
CREATE INDEX movie_collections
ON movies (belongs_to_collection)
--------------------------------------------------------------------------------

--------------------------------------------------------------------------------
-- query 5 - best filming countries
SELECT pc.name as Country, (SUM(m.revenue) / COUNT(*)) as AverageRevenuePerMovie
FROM movies as m, movies_production_countries as mpc, production_countries as pc
WHERE m.id = mpc.movie_id and mpc.country_iso = pc.iso_3166_1 --todo: create indices on primary keys m.id and pc.iso_3166_1 like we said in doc? or is it redundant?
GROUP BY (pc.name)
HAVING SUM(m.revenue) > 0
ORDER BY AverageRevenuePerMovie DESC
LIMIT 50
--------------------------------------------------------------------------------

--------------------------------------------------------------------------------
-- query 6 - should the catch phrase be a question or not?
CREATE VIEW taglines_as_questions AS
SELECT *
FROM movies as m
WHERE m.tagline LIKE 'When%?' OR m.tagline LIKE 'Where%?' OR m.tagline LIKE 'What%?' OR m.tagline LIKE 'How%?' OR m.tagline LIKE 'Who%?';

CREATE VIEW taglines_not_questions AS
(SELECT *
FROM movies as m
WHERE m.id NOT IN
(SELECT taglines_as_questions.id
FROM taglines_as_questions));

SELECT AVG(tq.revenue) as tagline_questions_predicted_revenue, AVG(tnq.revenue) as tagline_non_questions_predicted_revenue
FROM taglines_as_questions as tq, taglines_not_questions as tnq

CREATE FULLTEXT INDEX taglineIndex
ON movies(tagline)
--------------------------------------------------------------------------------

--------------------------------------------------------------------------------
-- query 7 - which budget size generates best marginal revenue
SELECT m.budget as BudgetSize, ((SUM(m.revenue) - (m.budget*count(*))) / (m.budget*count(*))) as MarginalRevenue
FROM movies as m
WHERE m.budget > 10000 --todo: create index on m.budget (and refer to it in doc)
GROUP BY m.budget
ORDER BY MarginalRevenue DESC
LIMIT 10
--------------------------------------------------------------------------------
