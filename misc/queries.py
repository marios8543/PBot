queries=["""
CREATE TABLE IF NOT EXISTS `servers` (
	`id`	INTEGER,
	`added_on`	DATETIME DEFAULT CURRENT_TIMESTAMP,
	`welcome_channel`	INTEGER,
	`goodbye_channel`	INTEGER,
	`event_channel`	INTEGER,
	`log_channel`	INTEGER,
	`log_active`	TEXT DEFAULT '{"msg":"1","name":"1" ,"votekick":"1"}	',
	`log_whitelist`	TEXT,
	`entry_text`	TEXT,
	`entry_text_pm`	TEXT,
	`goodbye_text`	TEXT,
	`max_warns`	INTEGER DEFAULT 3
);
"""
,"""
CREATE TABLE IF NOT EXISTS `members` (
	`id`	INTEGER,
	`server_id`	INTEGER,
	`verified`	INTEGER DEFAULT 0,
	`in_server`	INTEGER DEFAULT 1,
	`warns`	INTEGER DEFAULT 0
);
"""
,"""
CREATE TABLE IF NOT EXISTS `setting_sessions` (
	`ID`	INTEGER,
	`token`	TEXT,
	`server_id`	INTEGER,
	`admin_id`	INTEGER,
	`timestamp`	DATETIME DEFAULT CURRENT_TIMESTAMP,
	`valid`	INTEGER
);
"""]