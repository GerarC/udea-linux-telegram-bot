CREATE_INSULTS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS banter_insults (
    id SERIAL PRIMARY KEY,
    phrase TEXT NOT NULL
)
"""

CREATE_COMPLIMENTS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS banter_compliments (
    id SERIAL PRIMARY KEY,
    phrase TEXT NOT NULL
)
"""

CREATE_BANTER_STATS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS banter_stats (
    chat_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    insults_received INT NOT NULL DEFAULT 0,
    compliments_received INT NOT NULL DEFAULT 0,
    PRIMARY KEY (chat_id, user_id),
    FOREIGN KEY (chat_id, user_id) REFERENCES group_members (chat_id, user_id)
)
"""

HAS_INSULTS_CHAT_ID_COLUMN_SQL = """
SELECT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'banter_insults' AND column_name = 'chat_id'
)
"""

ADD_INSULTS_CHAT_ID_COLUMN_SQL = "ALTER TABLE banter_insults ADD COLUMN chat_id BIGINT"

# One-time migration: insults predated chat scoping - backfill the existing rows
# to the one chat they already belonged to instead of losing them.
BACKFILL_INSULTS_CHAT_ID_SQL = "UPDATE banter_insults SET chat_id = $1 WHERE chat_id IS NULL"

ALTER_INSULTS_CHAT_ID_NOT_NULL_SQL = "ALTER TABLE banter_insults ALTER COLUMN chat_id SET NOT NULL"

CREATE_INSULTS_CHAT_ID_INDEX_SQL = "CREATE INDEX IF NOT EXISTS banter_insults_chat_id_idx ON banter_insults (chat_id)"

HAS_COMPLIMENTS_CHAT_ID_COLUMN_SQL = """
SELECT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'banter_compliments' AND column_name = 'chat_id'
)
"""

# One-time migration: the old flat compliment phrases weren't tied to any chat -
# cleared out (per product decision) instead of guessing which chat they belonged to.
DELETE_ALL_COMPLIMENTS_SQL = "DELETE FROM banter_compliments"

ADD_COMPLIMENTS_CHAT_ID_COLUMN_SQL = "ALTER TABLE banter_compliments ADD COLUMN chat_id BIGINT NOT NULL"

CREATE_COMPLIMENTS_CHAT_ID_INDEX_SQL = (
    "CREATE INDEX IF NOT EXISTS banter_compliments_chat_id_idx ON banter_compliments (chat_id)"
)

GET_RANDOM_INSULT_SQL = "SELECT phrase FROM banter_insults WHERE chat_id = $1 ORDER BY random() LIMIT 1"

GET_RANDOM_COMPLIMENT_SQL = "SELECT phrase FROM banter_compliments WHERE chat_id = $1 ORDER BY random() LIMIT 1"

ADD_INSULT_SQL = "INSERT INTO banter_insults (chat_id, phrase) VALUES ($1, $2)"

ADD_COMPLIMENT_SQL = "INSERT INTO banter_compliments (chat_id, phrase) VALUES ($1, $2)"

RECORD_INSULT_SQL = """
INSERT INTO banter_stats (chat_id, user_id, insults_received, compliments_received)
VALUES ($1, $2, 1, 0)
ON CONFLICT (chat_id, user_id)
DO UPDATE SET insults_received = banter_stats.insults_received + 1
"""

RECORD_COMPLIMENT_SQL = """
INSERT INTO banter_stats (chat_id, user_id, insults_received, compliments_received)
VALUES ($1, $2, 0, 1)
ON CONFLICT (chat_id, user_id)
DO UPDATE SET compliments_received = banter_stats.compliments_received + 1
"""

GET_BANTER_STATS_SQL = """
SELECT gm.username, gm.full_name, bs.insults_received, bs.compliments_received
FROM banter_stats bs
JOIN group_members gm ON gm.chat_id = bs.chat_id AND gm.user_id = bs.user_id
WHERE bs.chat_id = $1 AND bs.user_id = $2
"""

GET_MOST_INSULTED_SQL = """
SELECT gm.user_id, gm.username, gm.full_name, bs.insults_received, bs.compliments_received
FROM banter_stats bs
JOIN group_members gm ON gm.chat_id = bs.chat_id AND gm.user_id = bs.user_id
WHERE bs.chat_id = $1 AND bs.insults_received > 0
ORDER BY bs.insults_received DESC
LIMIT 1
"""

GET_MOST_COMPLIMENTED_SQL = """
SELECT gm.user_id, gm.username, gm.full_name, bs.insults_received, bs.compliments_received
FROM banter_stats bs
JOIN group_members gm ON gm.chat_id = bs.chat_id AND gm.user_id = bs.user_id
WHERE bs.chat_id = $1 AND bs.compliments_received > 0
ORDER BY bs.compliments_received DESC
LIMIT 1
"""
