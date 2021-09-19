CREATE table users (id SERIAL PRIMARY KEY, email TEXT, name TEXT, password_hash TEXT);


INSERT INTO users (email, name, password_hash) VALUES ('bob@example.com', 'Bob Marley', 'example');

