CREATE TABLE pet_list(
id int PRIMARY KEY    NOT NULL,
type char(50)    NOT NULL
);
CREATE TABLE cat_facts(
id integer PRIMARY KEY  AUTOINCREMENT  NOT NULL,
fact text  NOT NULL,
last_shown  datetime
);
