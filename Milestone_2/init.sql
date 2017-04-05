--  Parameters variable for file path


SET @data_folder_name = ' /Users/Niro/Documents/EPFL/Ecole/Semestre 6/Introduction to Database System/comics/' ;
SET @clean_extension = '_clean.cvs';

SET @story = @data_folder_name + 'story'+@clean_extension;
SET @series = @data_folder_name + 'series'+ @clean_extension;
SET @issue = @data_folder_name + 'issue'+@clean_extension;
SET @indicia_publisher = @data_folder_name + 'indicia_publisher'+@clean_extension;
SET @publisher = @data_folder_name + 'publisher'+@clean_extension;
SET @brand_group = @data_folder_name + 'brand_group'+ @clean_extension;
SET @country = @data_folder_name + 'country'+ @clean_extension;
SET @language = @data_folder_name + 'language.csv' + @clean_extension;
SET @series_publication_type = @data_folder_name + 'series_publication_type.csv' + @clean_extension;
SET @story_type = @data_folder_name + 'story_reprint_csv' + @clean_extension;
SET @issue_reprint = @data_folder_name + 'issue_reprint.csv' + @clean_extension;
SET @story_reprint = @data_folder_name + 'story_reprint.csv' + @clean_extension;

/*
TODO:
    - How to choose the size of the CHAR type in order to be OPTIMAL. What type to choose to DATE  .
    - write sql file to LOAD cleaned  files.
    
*/



			
			
	



-- Part 1 is to create the table schema.

CREATE TABLE Story_Type (
	id INTEGER,
	name TEXT,
	PRIMARY KEY (id)
);

CREATE TABLE Series_Publication_Type (
	id INTEGER,
	name CHAR(16), -- maximum est 8 pour le moment mais permet d'avoir une marge.
	PRIMARY KEY (id)
);

CREATE TABLE Country (
	id INTEGER,
	code CHAR(8), -- code max length is 4 in the file but we prefer to be safe
	name TEXT,
	PRIMARY KEY (id)
);

CREATE TABLE Language (
	id INTEGER,
	code CHAR(8), -- code max length is 4 in the file but we prefer to be safe
	name TEXT,
	PRIMARY KEY (id)
);



CREATE TABLE Publisher (
	id INTEGER,
	name TEXT,
	country_id INTEGER NOT NULL, -- toujours vu: devrait rester NOT NULL
	year_began INTEGER,
	year_ended INTEGER, -- souvent NULL quand pas finis par exemple
	notes TEXT,
	url CHAR(256),
	PRIMARY KEY (id),
	FOREIGN KEY (country_id) REFERENCES Country(id)
);

CREATE TABLE Brand_Group (
	id INTEGER,
	name TEXT,
	year_began INTEGER, -- Souvent mis null 
	year_ended INTEGER, -- Presque jamais remplis, toujours NULL ou rien, on devrait clean mais le laisser quand même
	notes TEXT,
	url CHAR(256),
	publisher_id INTEGER NOT NULL, -- On peut laisser NOT NULL, toujours mis dans la table
	PRIMARY KEY (id),
	FOREIGN KEY (publisher_id) REFERENCES Publisher(id)
);

CREATE TABLE Indicia_Publisher (
	id INTEGER,
	name TEXT,
	publisher_id INTEGER NOT NULL, -- Toujours vu: devrait laisser not null
	country_id INTEGER NOT NULL, -- Pareil presque toujours vu
	year_began INTEGER, -- Des fois ils écrivent NULL a la place de laisser blanc: faudrait effacer tous les NULL
	year_ended INTEGER, -- Des fois ils écrivent NULL a la place de laisser blanc: faudrait effacer tous les NULL
	is_surrogate INTEGER, -- Always 0 or 1
	notes TEXT,
	url CHAR(256),
	PRIMARY KEY (id),
	FOREIGN KEY (publisher_id) REFERENCES Publisher(id),
	FOREIGN KEY (country_id) REFERENCES Country(id)
);

CREATE TABLE Issue (
	id INTEGER,
	issue_number CHAR(32),
	series_id INTEGER,
	indicia_publisher_id INTEGER, -- there was NOT NULL here but in the file, it's almost always NULL
	publication_date CHAR(64), -- for example "monthly"
	price TEXT,
	page_count INTEGER,
	indicia_frequency CHAR(64),
	editing TEXT,
	notes TEXT,
	on_sale_date DATE, -- or CHAR(20) for example (but in the file, it was YYYY-MM-DD)
	PRIMARY KEY (id),
	-- FOREIGN KEY (series_id) REFERENCES Series(id),  BECAUSE CIRCULAR REFERENCES
	FOREIGN KEY (indicia_publisher_id) REFERENCES Indicia_Publisher(id)
);

CREATE TABLE Series (
	id INTEGER,
	name TEXT,
	year_began INTEGER,
	year_ended INTEGER,
	publication_dates CHAR(64),
	first_issue_id INTEGER NOT NULL,
	last_issue_id INTEGER NOT NULL,
	publisher_id INTEGER,
	country_id INTEGER NOT NULL,
	language_id INTEGER,
	notes TEXT,
	color TEXT,
	dimensions TEXT,
	paper_stock TEXT,
	binding TEXT,
	publishing_format TEXT,
	publication_type_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY (first_issue_id) REFERENCES Issue(id),
	FOREIGN KEY (last_issue_id) REFERENCES Issue(id),
	FOREIGN KEY (publisher_id) REFERENCES Publisher(id),
	FOREIGN KEY (language_id) REFERENCES Language(id),
	FOREIGN KEY (country_id) REFERENCES Country(id)
);


-- ADD the remove foreign key because of the circular reference.
ALTER TABLE Issue
ADD FOREIGN KEY (series_id) REFERENCES Series(id);  




CREATE TABLE Story (
	id INTEGER,
	title TEXT,
	feature CHAR(64),
	issue_id INTEGER, -- Certaines ne le contienne pas donc a voir si on laisse NOT NULL
	script TEXT,
	pencils CHAR(64),
	inks CHAR(64),
	colors CHAR(64),
	letters CHAR(64),
	editing TEXT,
	genre CHAR(64),
	characters TEXT,
	synopsis TEXT,
	reprint_notes TEXT,
	notes TEXT,
	type_id INTEGER NOT NULL, -- Je l'ai presque tout le temps vu on pourrait le garder not null
	PRIMARY KEY (id),
	FOREIGN KEY (issue_id) REFERENCES Issue(id),
	FOREIGN KEY (type_id) REFERENCES Story_Type(id)
);


CREATE TABLE Story_Reprint (
	id INTEGER,
	origin_id INTEGER NOT NULL,
	target_id INTEGER NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (origin_id) REFERENCES Story(id),
	FOREIGN KEY (target_id) REFERENCES Story(id)
);

CREATE TABLE Issue_Reprint (
	id INTEGER,
	origin_issue_id INTEGER NOT NULL,
	target_target_id INTEGER NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (origin_issue_id) REFERENCES Issue(id),
	FOREIGN KEY (target_target_id) REFERENCES Issue(id)
);



