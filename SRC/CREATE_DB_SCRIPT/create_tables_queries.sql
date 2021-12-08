CREATE TABLE genres (
	id int NOT NULL,
    name VARCHAR(255),
    PRIMARY KEY (id)
    );

CREATE TABLE actors (
	id int NOT NULL,
    name VARCHAR(255) NOT NULL,
    imdb_id CHAR(9),
    gender int NOT NULL,
    check (gender >= 0),
    check (gender < 4),
    birthday VARCHAR(50),
    deathday VARCHAR(50),
    popularity float,
    place_of_birth VARCHAR(255),
    PRIMARY KEY (id)
    );

CREATE TABLE production_companies (
	id int NOT NULL,
    name VARCHAR(255),
    origin_country VARCHAR(255),
    PRIMARY KEY (id)
    );


CREATE TABLE collections (
	id int NOT NULL,
    name VARCHAR(255),
	PRIMARY KEY (id)
    );

CREATE TABLE production_countries (
	iso_3166_1 VARCHAR(16) NOT NULL,
    name VARCHAR(255),
    PRIMARY KEY (iso_3166_1)
    );


CREATE TABLE movies (
	id int NOT NULL,
    imdb_id CHAR(9),
    title VARCHAR(255),
    belongs_to_collection int,
    budget int,
    revenue int,
    popularity float,
    status ENUM('Rumored', 'Planned', 'In Production', 'Post Production', 'Released', 'Canceled') default 'Released',
    vote_count int,
    votes_avg float,
    release_date date NOT NULL,
    runtime int,
    tagline VARCHAR(1000),
    PRIMARY KEY (id),
    FOREIGN KEY (belongs_to_collection) REFERENCES collections(id));

  -- MANY TO MANY RELATIONS
  
CREATE TABLE movies_production_companies (
	movie_id int NOT NULL,
    production_company_id int NOT NULL,
    FOREIGN KEY (movie_id) REFERENCES movies(id),
    FOREIGN KEY (production_company_id) REFERENCES production_companies(id)
    );

CREATE TABLE movies_actors (
	movie_id int NOT NULL,
    actor_id int NOT NULL,
    FOREIGN KEY (movie_id) REFERENCES movies(id),
    FOREIGN KEY (actor_id) REFERENCES actors(id)
    );

CREATE TABLE movies_production_countries (
	movie_id int NOT NULL,
    country_iso VARCHAR(16) NOT NULL,
    FOREIGN KEY (movie_id) REFERENCES movies(id),
    FOREIGN KEY (country_iso) REFERENCES production_countries(iso_3166_1)
    );

CREATE TABLE movie_genres (
	movie_id int NOT NULL,
    genre_id int NOT NULL,
    FOREIGN KEY (movie_id) REFERENCES movies(id),
    FOREIGN KEY (genre_id) REFERENCES genres(id)
    );
