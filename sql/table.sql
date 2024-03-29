-- プレイヤー情報
DROP TABLE IF EXISTS shulot.player;

CREATE TABLE IF NOT EXISTS shulot.player (
	id VARCHAR(64) NOT NULL PRIMARY KEY,
	name VARCHAR(64) NOT NULL,
	sex TINYINT,
	level TINYINT NOT NULL DEFAULT(3),
	on_break TINYINT NOT NULL DEFAULT(0),
	created_at TIMESTAMP DEFAULT(CURRENT_TIMESTAMP),
	updated_at TIMESTAMP DEFAULT(CURRENT_TIMESTAMP)
);

-- 参加履歴
DROP TABLE IF EXISTS shulot.participation_history;

CREATE TABLE IF NOT EXISTS shulot.participation_history (
	id VARCHAR(64) NOT NULL PRIMARY KEY,
	player_id VARCHAR(64) NOT NULL,
	created_at TIMESTAMP DEFAULT(CURRENT_TIMESTAMP),
	updated_at TIMESTAMP DEFAULT(CURRENT_TIMESTAMP)
);

DROP TABLE IF EXISTS shulot.pair;

CREATE TABLE IF NOT EXISTS shulot.pair (
	id VARCHAR(64) NOT NULL PRIMARY KEY,
	player1_id VARCHAR(64) NOT NULL,
	player2_id VARCHAR(64) NOT NULL,
	created_at TIMESTAMP DEFAULT(CURRENT_TIMESTAMP),
	updated_at TIMESTAMP DEFAULT(CURRENT_TIMESTAMP)
);

-- 試合確定時に登録しておく
-- ペアIDが発行され、game テーブル登録時に使えるようになる
DROP TABLE IF EXISTS shulot.match;

CREATE TABLE IF NOT EXISTS shulot.match (
	id VARCHAR(64) NOT NULL PRIMARY KEY,
	pair1_id VARCHAR(64) NOT NULL,
	pair2_id VARCHAR(64) NOT NULL,
	created_at TIMESTAMP DEFAULT(CURRENT_TIMESTAMP),
	updated_at TIMESTAMP DEFAULT(CURRENT_TIMESTAMP)
);

DROP TABLE IF EXISTS shulot.game;

CREATE TABLE IF NOT EXISTS shulot.game (
	id VARCHAR(64) NOT NULL PRIMARY KEY,
	match_id VARCHAR(64) NOT NULL,
	winner_id VARCHAR(64) COMMENT '勝者のペアID',
	winner_score TINYINT,
	loser_id VARCHAR(64) COMMENT '敗者のペアID',
	loser_score TINYINT,
	created_at TIMESTAMP DEFAULT(CURRENT_TIMESTAMP),
	updated_at TIMESTAMP DEFAULT(CURRENT_TIMESTAMP)
);
