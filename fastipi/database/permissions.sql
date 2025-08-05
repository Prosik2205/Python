CREATE TABLE permissions(
id SERIAL PRIMARY KEY,
name VARCHAR(50) UNIQUE NOT NULL,         
description TEXT,                          
permissions JSONB NOT NULL DEFAULT '{}'
);