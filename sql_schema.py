'''CREATE TABLE new_nodes(id INTEGER  NOT NULL,lat REAL,lon REAL,
user TEXT,uid INTEGER,version INTEGER,changeset INTEGER,timestamp TEXT );

CREATE TABLE new_ways(id INTEGER  NOT NULL,user TEXT,uid INTEGER,
version INTEGER,changeset INTEGER,timestamp TEXT );

CREATE TABLE cleaned_nodetags(id INTEGER NOT NULL,key TEXT NOT NULL,
    value TEXT NOT NULL,
    type TEXT,
FOREIGN KEY (id) REFERENCES new_nodes(id) );

CREATE TABLE cleaned_waytags(id INTEGER NOT NULL,key TEXT NOT NULL,
    value TEXT NOT NULL,
    type TEXT,
FOREIGN KEY (id) REFERENCES new_ways(id) );




IMPORT YOUR CSV INTO A TABLE

sqlite3 openstreet.db  
sqlite> .mode csv
sqlite> .import new_nodes.csv new_nodes


sqlite> .mode csv
sqlite> .import new_ways.csv new_ways
 
sqlite> .mode csv
sqlite> .import cleaned_nodetags.csv cleaned_nodetags

sqlite> .mode csv
sqlite> .import cleaned_waytags.csv cleaned_waytags

'''