-- 削除
DELETE FROM shulot.participation_history;

INSERT INTO shulot.participation_history
VALUES
	(UUID(), "yoshizaki", NOW(), NOW());
INSERT INTO shulot.participation_history
VALUES
	(UUID(), "kanazawa", NOW(), NOW());
INSERT INTO shulot.participation_history
VALUES
	(UUID(), "zakiyama", NOW(), NOW());
INSERT INTO shulot.participation_history
VALUES
	(UUID(), "iizumi", NOW(), NOW());
INSERT INTO shulot.participation_history
VALUES
	(UUID(), "yoshizaki", NOW() + INTERVAL 1 MINUTE, NOW() + INTERVAL 1 MINUTE);
INSERT INTO shulot.participation_history
VALUES
	(UUID(), "yamae", NOW() + INTERVAL 1 MINUTE, NOW() + INTERVAL 1 MINUTE);
INSERT INTO shulot.participation_history
VALUES
	(UUID(), "fukada", NOW() + INTERVAL 1 MINUTE, NOW() + INTERVAL 1 MINUTE);
INSERT INTO shulot.participation_history
VALUES
	(UUID(), "noi", NOW() + INTERVAL 1 MINUTE, NOW() + INTERVAL 1 MINUTE);