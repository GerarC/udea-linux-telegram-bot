CREATE_POLLS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS polls (
    id BIGSERIAL PRIMARY KEY,
    chat_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    question TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    FOREIGN KEY (chat_id, user_id) REFERENCES group_members (chat_id, user_id)
)
"""

CREATE_POLLS_INDEX_SQL = """
CREATE INDEX IF NOT EXISTS idx_polls_chat_user ON polls (chat_id, user_id)
"""

SAVE_POLL_SQL = """
INSERT INTO polls (chat_id, user_id, question) VALUES ($1, $2, $3)
"""

GET_POLL_COUNT_SQL = """
SELECT count(*) FROM polls WHERE chat_id = $1 AND user_id = $2
"""

GET_CHAT_POLL_COUNT_SQL = """
SELECT count(*) FROM polls WHERE chat_id = $1
"""
