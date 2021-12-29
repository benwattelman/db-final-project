-- query 1 - competition across genres !! NOT_DONE_YET !!
SELECT pc.id as ID, pc.name as PRODUCTION_COMPANY_NAME, SUM(m.popularity) /*did this by popularity, there are other options we should consider*/
FROM movies as m, production_companies as pc, movies_production_companies as mpc, genres as g, movies_genres as mg
WHERE m.id = mpc.movie_id
and pc.id = mpc.production_company_id
and m.id = mg.movie_id
and g.id = mg.genre_id
GROUP BY g.id, pc.id as production_companies_popularity --todo: validate this

-- query 2 - currently planned film across genres
SELECT g.name as GENRE, count(*) as NUMBER_OF_PLANNED_MOVIES
FROM movies as m, movie_genres as mg, genres as g
WHERE m.id = mg.movie_id
and g.id = mg.genre_id
and (m.status <> "Released") --todo: create index on m.status*/
GROUP BY g.name

-- query 3 - best release months
SELECT MONTH(m.release_date) as Month, (COUNT(*) / 21) as AverageReleasesPerMonth
FROM movies as m
WHERE m.release_date >= "2000-01-01"
GROUP BY MONTH(m.release_date)
ORDER BY Month

-- query 4 - sequel profitability

-- query 5 - best filming countries
SELECT pc.name as Country, (SUM(m.revenue) / COUNT(*)) as AverageRevenuePerMovie
FROM movies as m, movies_production_countries as mpc, production_countries as pc
WHERE m.id = mpc.movie_id and mpc.country_iso = pc.iso_3166_1 --todo: create indices on primary keys m.id and pc.iso_3166_1 like we said in doc? or is it redundant?
GROUP BY (pc.name)
HAVING SUM(m.revenue) > 0
ORDER BY AverageRevenuePerMovie DESC
LIMIT 50

-- query 6 - should the catch phrase be a question?

-- query 7 - which budget size generates best marginal revenue todo: is this maybe too simple? no grouping or anything
SELECT m.title as Title, m.budget as BudgetSize, ((m.revenue - m.budget) / m.budget) as MarginalRevenue
FROM movies as m
WHERE m.budget > 10000 --todo: create index on m.budget (and refer to it in doc)
ORDER BY MarginalRevenue DESC
LIMIT 10