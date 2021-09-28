CREATE table users (id SERIAL PRIMARY KEY, email TEXT, name TEXT, password_hash TEXT);

CREATE table favourites (id SERIAL PRIMARY KEY, user_id INTEGER, recipe_id INTEGER, notes TEXT, CONSTRAINT fk_users FOREIGN KEY(user_id) REFERENCES users(id));

INSERT INTO favourites (user_id, recipe_id) VALUES ('session')

INSERT INTO users (email, name, password_hash) VALUES ('bob@example.com', 'Bob Marley', 'password');

