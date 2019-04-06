queries=["""
CREATE TABLE IF NOT EXISTS servers (
	id	BIGINT,
	added_on	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	welcome_channel	BIGINT,
	goodbye_channel	BIGINT,
	event_channel	BIGINT,
	log_channel	BIGINT,
	log_active	TEXT DEFAULT '{"msg":"1","name":"1" ,"votekick":"1", "delete_command":"0"}'	,
	log_whitelist	TEXT,
	entry_text	TEXT,
	entry_text_pm	TEXT,
	goodbye_text	TEXT,
	max_warns	INTEGER DEFAULT 3
);
"""
,"""
CREATE TABLE IF NOT EXISTS members (
	id	BIGINT,
	server_id	BIGINT,
	verified	INTEGER DEFAULT 0,
	in_server	INTEGER DEFAULT 1,
	warns	INTEGER DEFAULT 0,
	konishi TEXT DEFAULT NULL,
	crypto TEXT DEFAULT NULL,
	birthday date NULL
);
"""
,"""
CREATE TABLE IF NOT EXISTS setting_sessions (
	ID	BIGINT,
	token	TEXT,
	server_id	BIGINT,
	admin_id	BIGINT,
	timestamp	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	valid	INTEGER
);
""",
"""
CREATE TABLE IF NOT EXISTS playing_status (
	usr_id BIGINT,
	title TEXT
);
""",
"""
CREATE TABLE IF NOT EXISTS commands (
	command TEXT,
	usages BIGINT DEFAULT 0,
	server_id BIGINT DEFAULT NULL
);
"""
]
