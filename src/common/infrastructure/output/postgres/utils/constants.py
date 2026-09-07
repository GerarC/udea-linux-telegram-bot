CREATE_GROUP_MEMBERS_SQL = """
CREATE TABLE IF NOT EXISTS group_members (
    chat_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    username TEXT NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (chat_id, user_id)
)
"""

UPSERT_MEMBER_SQL = """
INSERT INTO group_members (chat_id, user_id, username)
VALUES ($1, $2, $3)
ON CONFLICT (chat_id, user_id) DO UPDATE SET username = EXCLUDED.username, updated_at = now()
"""
