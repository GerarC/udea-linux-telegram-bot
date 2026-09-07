CREATE_NEWS_CHAT_STATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS news_chat_state (
    chat_id BIGINT PRIMARY KEY,
    last_fired_at TIMESTAMPTZ NOT NULL
)
"""

CREATE_NEWS_SENT_LINKS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS news_sent_links (
    chat_id BIGINT NOT NULL,
    link TEXT NOT NULL,
    sent_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (chat_id, link)
)
"""

# NOTE: atomic check-and-set. ON CONFLICT locks the existing row before evaluating
# the WHERE clause, so under concurrent_updates two triggers racing on the same
# chat_id serialize: the second sees the first's just-committed last_fired_at and
# correctly fails the cooldown check instead of both slipping through.
TRY_FIRE_SQL = """
INSERT INTO news_chat_state (chat_id, last_fired_at)
VALUES ($1, now())
ON CONFLICT (chat_id) DO UPDATE
    SET last_fired_at = now()
    WHERE news_chat_state.last_fired_at <= now() - ($2::int * interval '1 second')
RETURNING chat_id
"""

GET_RECENT_SQL = """
SELECT link FROM news_sent_links
WHERE chat_id = $1
ORDER BY sent_at DESC
LIMIT $2
"""

MARK_SENT_SQL = """
INSERT INTO news_sent_links (chat_id, link)
VALUES ($1, $2)
ON CONFLICT (chat_id, link) DO UPDATE SET sent_at = now()
"""

PRUNE_SENT_LINKS_SQL = """
DELETE FROM news_sent_links
WHERE chat_id = $1 AND link NOT IN (
    SELECT link FROM news_sent_links WHERE chat_id = $1 ORDER BY sent_at DESC LIMIT $2
)
"""
