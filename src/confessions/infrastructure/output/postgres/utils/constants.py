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

CREATE_CONFESSION_SQL = """
INSERT INTO confessions (chat_id, user_id, content)
VALUES ($1, $2, $3)
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

CREATE_CONFESSION_TITLES_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS confession_titles (
    id SERIAL PRIMARY KEY,
    emoji TEXT NOT NULL,
    title TEXT NOT NULL,
    footer TEXT NOT NULL,
    UNIQUE (title)
)
"""

# NOTE: seeds the built-in flavor titles once - ON CONFLICT (title) makes this
# idempotent across restarts. Add more via sql/confession_titles_seed.sql.
SEED_CONFESSION_TITLES_SQL = """
INSERT INTO confession_titles (emoji, title, footer) VALUES
    ('🕯️', 'Confesión anónima', 'Enviado desde las profundidades del /dev/null'),
    ('🩸', 'Confesión del abismo', 'El universo decidió que esto debía saberse'),
    ('🧠', 'Confesión residual', 'Transmitido anónimamente')
ON CONFLICT (title) DO NOTHING
"""

GET_RANDOM_CONFESSION_TITLE_SQL = """
SELECT emoji, title, footer FROM confession_titles ORDER BY random() LIMIT 1
"""
