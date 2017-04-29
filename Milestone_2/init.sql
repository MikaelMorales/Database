CREATE TABLE Story_Type (
	id INT NOT NULL,
	name VARCHAR(40),
	PRIMARY KEY (id)
);

CREATE TABLE Country (
	id INT NOT NULL,
	code VARCHAR(4),
	name VARCHAR(40),
	PRIMARY KEY (id)
);

CREATE TABLE Series_Publication_Type (
	id INT NOT NULL,
	name VARCHAR(16),
	PRIMARY KEY (id)
);

CREATE TABLE Language (
	id INT NOT NULL,
	code VARCHAR(4),
	name VARCHAR(40),
	PRIMARY KEY (id)
);

CREATE TABLE Publisher (
	id INT NOT NULL,
	name VARCHAR(128),
	country_id INT NOT NULL,
	year_began INT,
	year_ended INT,
	notes TEXT,
	url VARCHAR(256),
	PRIMARY KEY (id),
	FOREIGN KEY (country_id) REFERENCES Country(id)
);

CREATE TABLE Brand_Group (
	id INT NOT NULL,
	name VARCHAR(128),
	year_began INT,
	year_ended INT,
	notes TEXT,
	url VARCHAR(256),
	publisher_id INT NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (publisher_id) REFERENCES Publisher(id)
);

CREATE TABLE Indicia_Publisher (
	id INT NOT NULL,
	name VARCHAR(128),
	publisher_id INT NOT NULL,
	country_id INT NOT NULL,
	year_began INT,
	year_ended INT,
	is_surrogate INT,
	notes TEXT,
	url VARCHAR(256),
	PRIMARY KEY (id),
	FOREIGN KEY (publisher_id) REFERENCES Publisher(id),
	FOREIGN KEY (country_id) REFERENCES Country(id)
);

CREATE TABLE Issue (
	id INT NOT NULL,
	number VARCHAR(64),
	series_id INT,
	indicia_publisher_id INT,
	publication_date INT,
	price VARCHAR(16),
	page_count INT,
	indicia_frequency VARCHAR(160),
	notes TEXT,
	isbn VARCHAR(64),
	valid_isbn VARCHAR(64),
	barcode VARCHAR(64),
	title VARCHAR(128),
	on_sale_date INT,
	rating VARCHAR(128),
	PRIMARY KEY (id),
/* 	FOREIGN KEY (series_id) REFERENCES Series(id), */
	FOREIGN KEY (indicia_publisher_id) REFERENCES Indicia_Publisher(id)
);


CREATE TABLE Issue_Editing (
	id INT NOT NULL,
	name VARCHAR(32),
	PRIMARY KEY (id)
);

CREATE TABLE Issue_Has_Editing (
	 issue_id INT NOT NULL,
	 editing_id INT NOT NULL,
	 PRIMARY KEY (issue_id, editing_id),
	 FOREIGN KEY (issue_id) REFERENCES Issue(id),
	 FOREIGN KEY (editing_id) REFERENCES Issue_Editing(id)
);

CREATE TABLE Story (
	id INT NOT NULL,
	title VARCHAR(512),
	issue_id INT,
	letters TEXT,
	editing VARCHAR(512),
	synopsis TEXT,
	reprint_notes TEXT,
	notes TEXT,
	type_id INT,
	PRIMARY KEY (id),
	FOREIGN KEY (issue_id) REFERENCES Issue(id),
	FOREIGN KEY (type_id) REFERENCES Story_Type(id)
);

CREATE TABLE Series (
	id INT NOT NULL,
	name VARCHAR(256),
	format VARCHAR(256),
	year_began INT,
	year_ended INT,
	publication_dates INT,
	first_issue_id INT,
	last_issue_id INT,
	publisher_id INT NOT NULL,
	country_id INT NOT NULL,
	language_id INT NOT NULL,
	notes TEXT,
	dimensions VARCHAR(256),
	publishing_format VARCHAR(128),
	publication_type_id INT,
	PRIMARY KEY (id),
	FOREIGN KEY (first_issue_id) REFERENCES Issue(id),
	FOREIGN KEY (last_issue_id) REFERENCES Issue(id),
	FOREIGN KEY (publisher_id) REFERENCES Publisher(id),
	FOREIGN KEY (language_id) REFERENCES Language(id),
	FOREIGN KEY (country_id) REFERENCES Country(id),
	FOREIGN KEY (publication_type_id) REFERENCES Series_Publication_Type(id)
);

ALTER TABLE Issue ADD CONSTRAINT series_id FOREIGN KEY (series_id) REFERENCES Series(id);


CREATE TABLE Serie_Binding (
	id INT NOT NULL,
	name VARCHAR(32),
	PRIMARY KEY (id)
);

CREATE TABLE Serie_Has_Binding (
	series_id INT NOT NULL,
	binding_id INT NOT NULL,
	PRIMARY KEY (series_id, binding_id),
	FOREIGN KEY (series_id) REFERENCES Series(id),
	FOREIGN KEY (binding_id) REFERENCES Serie_Binding(id)
);

CREATE TABLE Serie_Colors (
	id INT NOT NULL,
	name VARCHAR(64),
	PRIMARY KEY (id)
);

CREATE TABLE Serie_Has_Colors (
	series_id INT NOT NULL,
	color_id INT NOT NULL,
	PRIMARY KEY (series_id, color_id),
	FOREIGN KEY (series_id) REFERENCES Series(id),
	FOREIGN KEY (color_id) REFERENCES Serie_Colors(id)
);

CREATE TABLE Story_Features (
	id INT NOT NULL,
	name VARCHAR(64),
	PRIMARY KEY (id)
);

CREATE TABLE Story_Has_Features (
	story_id INT NOT NULL,
	feature_id INT NOT NULL,
	PRIMARY KEY (story_id, feature_id),
	FOREIGN KEY (story_id) REFERENCES Story(id),
	FOREIGN KEY (feature_id) REFERENCES Story_Features(id)
);

CREATE TABLE Story_Artists (
	id INT NOT NULL,
	name VARCHAR(64),
	PRIMARY KEY(id)
);

CREATE TABLE Story_Has_Inks (
	story_id INT NOT NULL,
	artist_id INT NOT NULL,
	PRIMARY KEY (story_id, artist_id),
	FOREIGN KEY(story_id) REFERENCES Story(id),
	FOREIGN KEY(artist_id) REFERENCES Story_Artists(id)
);

CREATE TABLE Story_Has_Colors (
	story_id INT NOT NULL,
	artist_id INT NOT NULL,
	PRIMARY KEY (story_id, artist_id),
	FOREIGN KEY(story_id) REFERENCES Story(id),
	FOREIGN KEY(artist_id) REFERENCES Story_Artists(id)
);

CREATE TABLE Story_Has_Pencils (
	story_id INT NOT NULL,
	artist_id INT NOT NULL,
	PRIMARY KEY (story_id, artist_id),
	FOREIGN KEY(story_id) REFERENCES Story(id),
	FOREIGN KEY(artist_id) REFERENCES Story_Artists(id)
);

CREATE TABLE Story_Has_Scripts (
	story_id INT NOT NULL,
	artist_id INT NOT NULL,
	PRIMARY KEY (story_id, artist_id),
	FOREIGN KEY(story_id) REFERENCES Story(id),
	FOREIGN KEY(artist_id) REFERENCES Story_Artists(id)
);

CREATE TABLE Story_Genres (
	id INT NOT NULL,
	name VARCHAR(32),
	PRIMARY KEY(id)
);

CREATE TABLE Story_Has_Genres (
	story_id INT NOT NULL,
	genre_id INT NOT NULL,
	PRIMARY KEY(story_id, genre_id),
	FOREIGN KEY(story_id) REFERENCES Story(id),
	FOREIGN KEY(genre_id) REFERENCES Story_Genres(id)
);

CREATE TABLE Story_Characters (
	id INT NOT NULL,
	name VARCHAR(2048),
	PRIMARY KEY(id)
);

CREATE TABLE Story_Has_Characters (
	story_id INT NOT NULL,
	character_id INT NOT NULL,
	PRIMARY KEY(story_id, character_id),
	FOREIGN KEY(story_id) REFERENCES Story(id),
	FOREIGN KEY(character_id) REFERENCES Story_Characters(id)
);

CREATE TABLE Story_Reprint (
	origin_id INT NOT NULL,
	target_id INT NOT NULL,
	PRIMARY KEY (origin_id, target_id),
	FOREIGN KEY (origin_id) REFERENCES Story(id),
	FOREIGN KEY (target_id) REFERENCES Story(id)
);

CREATE TABLE Issue_Reprint (
	origin_id INT NOT NULL,
	target_id INT NOT NULL,
	PRIMARY KEY (origin_id, target_id),
	FOREIGN KEY (origin_id) REFERENCES Story(id),
	FOREIGN KEY (target_id) REFERENCES Story(id)
);