CREATE_CONFESSIONS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS confessions (
    id BIGSERIAL PRIMARY KEY,
    chat_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    is_deleted BOOLEAN NOT NULL DEFAULT false,
    FOREIGN KEY (chat_id, user_id) REFERENCES group_members (chat_id, user_id)
)
"""

# NOTE: atomic check-and-set - see postgres.md. The INSERT only happens when the
# user has no confession in this chat newer than the cooldown window, so a burst of
# concurrent /confesar calls from the same user can't both slip through.
CREATE_CONFESSION_SQL = """
INSERT INTO confessions (chat_id, user_id, content)
SELECT $1, $2, $3
WHERE NOT EXISTS (
    SELECT 1 FROM confessions
    WHERE chat_id = $1 AND user_id = $2 AND created_at > now() - ($4 * interval '1 minute')
)
RETURNING id, chat_id, user_id, content, created_at, is_deleted
"""

GET_RECENT_CONFESSIONS_SQL = """
SELECT id, chat_id, user_id, content, created_at, is_deleted
FROM confessions
WHERE chat_id = $1 AND is_deleted = false
ORDER BY created_at DESC
LIMIT $2
"""

SOFT_DELETE_CONFESSION_SQL = """
UPDATE confessions
SET is_deleted = true
WHERE id = $1 AND chat_id = $2 AND is_deleted = false
RETURNING id, chat_id, user_id, content, created_at, is_deleted
"""
