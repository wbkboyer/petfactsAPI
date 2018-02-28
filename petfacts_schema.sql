CREATE TABLE pet_list(
id int PRIMARY KEY    NOT NULL,
type char(50)    NOT NULL
);
CREATE TABLE cat_facts(
id integer PRIMARY KEY  AUTOINCREMENT  NOT NULL,
fact text  NOT NULL,
last_shown  datetime
);
CREATE TABLE known_users(
id integer primary key  not null,
username char(25)  not null,
latest_query datetime
, last_received_fact datetime);
CREATE TABLE logs(
id integer primary key not null,
requester char(25) not null,
response_code integer,
log_text text
);
