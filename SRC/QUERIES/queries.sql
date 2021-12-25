# query 1 - most successful actors

# query 2 - competition across genres !! NOT_DONE_YET !!
SELECT pc.id as ID, pc.name as PRODUCTION_COMPANY_NAME, SUM(m.popularity) /*did this by popularity, there are other options we should consider*/
FROM movies as m, production_companies as pc, movies_production_companies as mpc, genres as g, movies_genres as mg
WHERE m.id = mpc.movie_id
and pc.id = mpc.production_company_id
and m.id = mg.movie_id
and g.id = mg.genre_id
GROUP BY g.id, pc.id as production_companies_popularity --todo: validate this

# query 3 - currently planned film across genres
SELECT g.name as GENRE, count(*) as NUMBER_OF_PLANNED_MOVIES
FROM movies as m, movie_genres as mg, genres as g
WHERE m.id = mg.movie_id
and g.id = mg.genre_id
and (m.status <> "Released") --todo: create index on m.status*/
GROUP BY g.name

# query 4 - best release months


# query 5 - sequel profitability

# query 6 - best filming countries

# query 7 - should the catch phrase be a question?
