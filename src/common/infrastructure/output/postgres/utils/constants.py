CREATE_GROUP_MEMBERS_SQL = """
CREATE TABLE IF NOT EXISTS group_members (
    chat_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    username TEXT NOT NULL,
    full_name TEXT NOT NULL DEFAULT '',
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (chat_id, user_id)
)
"""

HAS_FULL_NAME_COLUMN_SQL = """
SELECT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'group_members' AND column_name = 'full_name'
)
"""

ADD_FULL_NAME_COLUMN_SQL = "ALTER TABLE group_members ADD COLUMN full_name TEXT NOT NULL DEFAULT ''"

# One-time backfill: before full_name existed, username held "username or full_name"
# mixed together and can't be told apart, so every legacy value is moved to full_name
# and username starts empty - each row gets its real username back the next time
# that person writes (see UPSERT_MEMBER_SQL).
MOVE_LEGACY_USERNAMES_TO_FULL_NAME_SQL = "UPDATE group_members SET full_name = username, username = ''"

# NOTE: an empty full_name (e.g. a user targeted by a typed @username, which carries no real
# name) never wipes the stored one; username CAN legitimately become empty (user removed it).
UPSERT_MEMBER_SQL = """
INSERT INTO group_members (chat_id, user_id, username, full_name)
VALUES ($1, $2, $3, $4)
ON CONFLICT (chat_id, user_id) DO UPDATE
SET username = EXCLUDED.username,
    full_name = COALESCE(NULLIF(EXCLUDED.full_name, ''), group_members.full_name),
    updated_at = now()
"""

FIND_MEMBER_BY_USERNAME_SQL = """
SELECT user_id FROM group_members
WHERE chat_id = $1 AND username <> '' AND lower(username) = lower($2)
"""
