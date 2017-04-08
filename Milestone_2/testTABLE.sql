
SET @data_folder_name    =  '/Users/Niro/Documents/EPFL/Ecole/Semestre 6/Introduction to Database System/comics/';

 SET @input_file_name =@data_folder_name + 'language.csv' ;
 SET @test = 'sda';
SET @remove_line = 1;

CREATE TABLE Language (
	id INTEGER,
	code CHAR(8), -- code max length is 4 in the file but we prefer to be safe
	name TEXT,
	PRIMARY KEY (id)
);


 LOAD DATA LOCAL INFILE  
INTO TABLE Language
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE @remove_line LINES
(id,code,name);

