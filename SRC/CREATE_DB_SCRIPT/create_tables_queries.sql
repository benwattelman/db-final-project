CREATE TABLE genres (
	id int,
    name VARCHAR(255)
    );

CREATE TABLE movies (
	id int NOT NULL,
    imdb_id VARCHAR(50),
    title VARCHAR(255), 
    belongs_to_collection int,
    budget int, 
    revenue int, 
    popularity float, 
    status ENUM('Rumored', 'Planned', 'In Production', 'Post Production', 'Released', 'Canceled') default 'Released', 
    vote_count int, 
    votes_avg float, 
    release_date date not null, 
    runtime int, 
    tagline VARCHAR(1000),
    PRIMARY KEY (id),
    FOREIGN KEY (belongs_to_collection) REFERENCES collections(id));
    
CREATE TABLE actors (
	id int,
    name VARCHAR(255) NOT NULL, 
    imdb_id VARCHAR(50),
    gender int NOT NULL, 
    birthday VARCHAR(50), 
    deathday VARCHAR(50), 
    popularity float, 
    place_of_birth VARCHAR(255),
    PRIMARY KEY (id),
    check (gender >= 0),
    check (gender < 4)
    );

CREATE TABLE production_companies (
	id int not null,
    name VARCHAR(255),
    origin_country VARCHAR(255),
    PRIMARY KEY (id)
    );


CREATE TABLE collections (
	id int not null,
    name VARCHAR(255),
	PRIMARY KEY (id)
    );
    
CREATE TABLE production_countries (
	iso_3166 VARCHAR(255) not null,
    name VARCHAR(255),
    PRIMARY KEY (iso_3166)
    );
  
  -- MANY TO MANY RELATIONS
  
CREATE TABLE movies_production_companies (
	movie_id int not null,
    production_company_id int not null,
    FOREIGN KEY (movie_id) REFERENCES movies(id),
    FOREIGN KEY (production_company_id) REFERENCES production_companies(id)
    );

CREATE TABLE movies_actors (
	movie_id int not null,
    actor_id int not null,
    FOREIGN KEY (movie_id) REFERENCES movies(id),
    FOREIGN KEY (actor_id) REFERENCES actors(id)
    );

CREATE TABLE movies_production_countries (
	movie_id int not null,
    country_iso VARCHAR(255) not null,
    FOREIGN KEY (movie_id) REFERENCES movies(id),
    FOREIGN KEY (country_iso) REFERENCES production_countries(iso_3166)
    );

CREATE TABLE movie_genres (
	movie_id int not null,
    genre_id int not null,
    FOREIGN KEY (movie_id) REFERENCES movies(id),
    FOREIGN KEY (genre_id) REFERENCES genres(id)
    );
