CREATE TABLE users(
id SERIAL PRIMARY KEY,
first_name VARCHAR(20) NOT NULL,
second_name VARCHAR(20) NOT NULL,
father_name VARCHAR(20),
email VARCHAR(25) UNIQUE NOT NULL,
passwords VARCHAR(10) NOT NULL,
birthday DATE NOT NULL,
last_login TIMESTAMP,
plan_id SMALLINT,
role_id SMALLINT
);


