CREATE TABLE Story (
	id INTEGER,
	title CHAR(64),
	feature CHAR(64),
	issue_id INTEGER NOT NULL,
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
	type_id INTEGER NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (issue_id) REFERENCES Issue(id),
	FOREIGN KEY (type_id) REFERENCES Story_Type(id)
)

CREATE TABLE Series (
	id INTEGER,
	name CHAR(64),
	format TEXT,
	year_began INTEGER,
	year_ended INTEGER,
	publication_dates CHAR(20),
	first_issue_id INTEGER,
	last_issue_id INTEGER,
	publisher_id INTEGER,
	country_id INTEGER,
	language_id INTEGER,
	notes TEXT,
	color TEXT,
	dimensions CHAR(20),
	paper_stock TEXT,
	binding TEXT,
	publishing_format TEXT,
	publication_type_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY (first_issue_id) REFERENCES Issue(id),
	FOREIGN KEY (last_issue_id) REFERENCES Issue(id),
	FOREIGN KEY (publisher_id) REFERENCES Publisher(id),
	FOREIGN KEY (language_id) REFERENCES Language(id)
)

CREATE TABLE Issue (
	id INTEGER,
	issue_number INTEGER,
	series_id INTEGER,
	indicia_publisher_id INTEGER NOT NULL,
	publication_date CHAR(20),
	price INTEGER,
	page_count INTEGER,
	indicia_frequency CHAR(20),
	editing CHAR(20),
	notes CHAR(100),
	isbn CHAR(50),
	valid_isbn CHAR(50),
	barcode INTEGER,
	title CHAR(50),
	on_sale_date CHAR(20),
	rating INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY (series_id) REFERENCES Series(id),
	FOREIGN KEY (indicia_publisher_id) REFERENCES Indicia_Publisher(id)
)

CREATE TABLE Indicia_Publisher (
	id INTEGER,
	name CHAR(20),
	publisher_id INTEGER NOT NULL,
	country_id INTEGER NOT NULL,
	year_began INTEGER,
	year_ended INTEGER,
	is_surrogate INTEGER,
	notes CHAR(100),
	url CHAR(100),
	PRIMARY KEY (id),
	FOREIGN KEY (publisher_id) REFERENCES Publisher(id),
	FOREIGN KEY (country_id) REFERENCES Country(id)
)

CREATE TABLE Publisher (
	id INTEGER,
	name CHAR(50),
	country_id INTEGER NOT NULL,
	year_began INTEGER,
	year_ended INTEGER,
	notes CHAR(100),
	url CHAR(100),
	PRIMARY KEY (id),
	FOREIGN KEY (country_id) REFERENCES Country(id)
)

CREATE TABLE Brand_Group (
	id INTEGER,
	name CHAR(50),
	year_began INTEGER,
	year_ended INTEGER,
	notes CHAR(100),
	url CHAR(100),
	publisher_id INTEGER NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (publisher_id) REFERENCES Publisher(id)
)

CREATE TABLE Country (
	id INTEGER,
	code CHAR(10),
	name CHAR(30),
	PRIMARY KEY (id)
)

CREATE TABLE Language (
	id INTEGER,
	code CHAR(10),
	name CHAR(30),
	PRIMARY KEY (id)
)

CREATE TABLE Series_Publication_Type (
	id INTEGER,
	name CHAR(30),
	PRIMARY KEY (id)
)

CREATE TABLE Story_Type (
	id INTEGER,
	name CHAR(30),
	PRIMARY KEY (id)
)

CREATE TABLE Story_Reprint (
	id INTEGER,
	origin_id INTEGER NOT NULL,
	target_id INTEGER NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (origin_id) REFERENCES Story(id),
	FOREIGN KEY (target_id) REFERENCES Story(id)
)

CREATE TABLE Issue_Reprint (
	id INTEGER,
	origin_issue_id INTEGER NOT NULL,
	target_target_id INTEGER NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (origin_issue_id) REFERENCES Issue(id),
	FOREIGN KEY (target_target_id) REFERENCES Issue(id)
)