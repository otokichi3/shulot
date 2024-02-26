-- 削除
DELETE FROM shulot.participation_history;

INSERT INTO shulot.participation_history
VALUES
	(UUID(), "sato", NOW(), NOW());
INSERT INTO shulot.participation_history
VALUES
	(UUID(), "ito", NOW(), NOW());
INSERT INTO shulot.participation_history
VALUES
	(UUID(), "yamamoto", NOW(), NOW());
INSERT INTO shulot.participation_history
VALUES
	(UUID(), "nakamura", NOW(), NOW());
INSERT INTO shulot.participation_history
VALUES
	(UUID(), "sato", NOW() + INTERVAL 1 MINUTE, NOW() + INTERVAL 1 MINUTE);
INSERT INTO shulot.participation_history
VALUES
	(UUID(), "kato", NOW() + INTERVAL 1 MINUTE, NOW() + INTERVAL 1 MINUTE);
INSERT INTO shulot.participation_history
VALUES
	(UUID(), "yoshida", NOW() + INTERVAL 1 MINUTE, NOW() + INTERVAL 1 MINUTE);
INSERT INTO shulot.participation_history
VALUES
	(UUID(), "yamada", NOW() + INTERVAL 1 MINUTE, NOW() + INTERVAL 1 MINUTE);