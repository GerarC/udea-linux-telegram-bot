CREATE_AUTISPUNTOS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS autispuntos (
    chat_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    points INT NOT NULL DEFAULT 0,
    PRIMARY KEY (chat_id, user_id)
)
"""

HAS_USERNAME_COLUMN_SQL = """
SELECT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'autispuntos' AND column_name = 'username'
)
"""

# Backfill group_members from the old autispuntos.username column before dropping it.
# NOTE: that column mixed usernames and full names, so (like group_members' own legacy
# backfill) the value goes to full_name and username stays empty.
BACKFILL_MEMBERS_SQL = """
INSERT INTO group_members (chat_id, user_id, username, full_name)
SELECT chat_id, user_id, '', username FROM autispuntos
ON CONFLICT (chat_id, user_id) DO UPDATE SET full_name = EXCLUDED.full_name
"""

DROP_USERNAME_COLUMN_SQL = "ALTER TABLE autispuntos DROP COLUMN username"

ADD_MEMBER_FK_SQL = """
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'autispuntos_member_fkey'
    ) THEN
        ALTER TABLE autispuntos
        ADD CONSTRAINT autispuntos_member_fkey
        FOREIGN KEY (chat_id, user_id) REFERENCES group_members (chat_id, user_id);
    END IF;
END $$;
"""

ADD_POINTS_SQL = """
INSERT INTO autispuntos (chat_id, user_id, points)
VALUES ($1, $2, $3)
ON CONFLICT (chat_id, user_id)
DO UPDATE SET points = autispuntos.points + EXCLUDED.points
RETURNING points
"""

GET_POINTS_SQL = """
SELECT gm.user_id, gm.username, gm.full_name, ap.points
FROM autispuntos ap
JOIN group_members gm ON gm.chat_id = ap.chat_id AND gm.user_id = ap.user_id
WHERE ap.chat_id = $1 AND ap.user_id = $2
"""

GET_RANKING_SQL = """
SELECT gm.user_id, gm.username, gm.full_name, ap.points
FROM autispuntos ap
JOIN group_members gm ON gm.chat_id = ap.chat_id AND gm.user_id = ap.user_id
WHERE ap.chat_id = $1
ORDER BY ap.points DESC
LIMIT $2
"""

GET_POSITION_SQL = """
SELECT rank FROM (
    SELECT user_id, RANK() OVER (ORDER BY points DESC) AS rank
    FROM autispuntos
    WHERE chat_id = $1
) ranked
WHERE user_id = $2
"""
