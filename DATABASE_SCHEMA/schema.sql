CREATE DATABASE brazilboard;

\c brazilboard


CREATE TABLE role(
	id SERIAL PRIMARY KEY,
	name VARCHAR(20),
	description VARCHAR(40)
);

CREATE TABLE user(
	id SERIAL PRIMARY KEY,
	uuid VARCHAR(22),
	username VARCHAR(100),
	email VARCHAR(255),
	password VARCHAR(60),
	role_id INTEGER,
	picture_uploaded BOOLEAN,
	created TIMESTAMP,
	last_login TIMESTAMP,
	active BOOLEAN,
	signature VARCHAR(500),
	FOREIGN KEY(role_id) REFERENCES role(id)
);

CREATE TABLE forum(
	uuid VARCHAR(8) PRIMARY KEY NOT NULL,
	name VARCHAR(80),
	owner_id int NOT NULL,
	created timestamp,
	FOREIGN KEY(owner_id) REFERENCES "user"(id)
);

CREATE TABLE topic(
	uuid VARCHAR(8) PRIMARY KEY NOT NULL,
	name VARCHAR(80),
	owner_id int NOT NULL,
	forum_uuid VARCHAR(8) NOT NULL,
	created timestamp,
	FOREIGN KEY(owner_id) REFERENCES "user"(id),
	FOREIGN KEY(forum_uuid) REFERENCES forum(uuid)
);

CREATE TABLE post(
	uuid VARCHAR(8) PRIMARY KEY NOT NULL,
	content VARCHAR(10000),
	owner_id int NOT NULL,
	topic_uuid VARCHAR(8) NOT NULL,
	created timestamp,
	FOREIGN KEY(owner_id) REFERENCES "user"(id),
	FOREIGN KEY(topic_uuid) REFERENCES topic(uuid)
);


CREATE TABLE forum_acl(
	id SERIAL PRIMARY KEY,
	forum_uuid VARCHAR(8) NOT NULL,
	role_id INT NOT NULL,
	read_topic BOOLEAN,
	write_topic BOOLEAN,
	edit_topic BOOLEAN,
	delete_topic BOOLEAN,
	write_post BOOLEAN,
	edit_post BOOLEAN,
	delete_post BOOLEAN,
	write_pool BOOLEAN,
	edit_pool BOOLEAN,
	delete_pool BOOLEAN,
	FOREIGN KEY(forum_uuid) REFERENCES forum(uuid),
	FOREIGN KEY(role_id) REFERENCES role(id)
);

CREATE TABLE moderator_acl(
	id SERIAL PRIMARY KEY,
	forum_uuid VARCHAR(8) NOT NULL,
	user_id INT NOT NULL,
	FOREIGN KEY(forum_uuid) REFERENCES forum(uuid),
	FOREIGN KEY(user_id) REFERENCES "user"(id)
);

INSERT INTO role(name,description) VALUES('VISITOR', 'Visitante');
INSERT INTO role(name,description) VALUES('LOGGED_USER', 'Usuário Autenticado');
INSERT INTO role(name,description) VALUES('MODERATOR', 'Usuário Moderador');
INSERT INTO role(name,description) VALUES('ADMIN', 'Administrador');



INSERT INTO "user"(uuid,username,email,password,role_id,picture_uploaded,created,last_login,active) 
	VALUES('1', 'alan', 'alanreis88@gmail.com', '123', 1, 'false', now(), now(), 'true');
