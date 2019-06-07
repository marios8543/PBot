queries=["""
CREATE TABLE IF NOT EXISTS servers (
    "id" bigint,
    "added_on" timestamp DEFAULT now(),
    "welcome_channel" bigint,
    "goodbye_channel" bigint,
    "event_channel" bigint,
    "log_channel" bigint,
    "log_whitelist" text,
    "entry_text" text,
    "entry_text_pm" text,
    "goodbye_text" text,
    "max_warns" integer DEFAULT '3',
    "antiflood_messages" integer DEFAULT '5' NOT NULL,
    "antiflood_time" integer DEFAULT '3' NOT NULL,
    "antiflood_warns" integer DEFAULT '4' NOT NULL,
    "antiflood_enabled" smallint DEFAULT '0' NOT NULL,
    "log_active_name" smallint DEFAULT '1' NOT NULL,
    "log_active_msg" smallint DEFAULT '1' NOT NULL
) WITH (oids = false);
"""
,"""
CREATE TABLE IF NOT EXISTS members (
    "id" bigint,
    "server_id" bigint,
    "verified" integer DEFAULT '0',
    "in_server" integer DEFAULT '1',
    "warns" integer DEFAULT '0',
    "birthday" date
) WITH (oids = false);
""",
"""
CREATE TABLE IF NOT EXISTS playing_status (
    "usr_id" bigint,
    "title" text
) WITH (oids = false);
""",
"""
CREATE TABLE IF NOT EXISTS commands (
    "command" text,
    "usages" bigint DEFAULT '0',
    "server_id" bigint
) WITH (oids = false);
"""
]
