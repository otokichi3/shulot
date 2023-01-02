DROP TABLE IF EXISTS shulot.player;

CREATE TABLE IF NOT EXISTS shulot.player (
	id varchar(255) NOT NULL PRIMARY KEY,
	name varchar(64) NOT NULL,
	sex tinyint,
	LEVEL tinyint NOT NULL DEFAULT(3),
	created_at timestamp DEFAULT(CURRENT_TIMESTAMP),
	updated_at timestamp DEFAULT(CURRENT_TIMESTAMP)
);