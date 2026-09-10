CREATE_REMINDERS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS reminders (
    id BIGSERIAL PRIMARY KEY,
    chat_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    message TEXT NOT NULL,
    remind_at TIMESTAMPTZ NOT NULL,
    fired BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    FOREIGN KEY (chat_id, user_id) REFERENCES group_members (chat_id, user_id)
)
"""

CREATE_REMINDER_SQL = """
INSERT INTO reminders (chat_id, user_id, message, remind_at)
VALUES ($1, $2, $3, $4)
RETURNING id, chat_id, user_id, message, remind_at, fired
"""

GET_PENDING_REMINDERS_SQL = """
SELECT id, chat_id, user_id, message, remind_at, fired
FROM reminders
WHERE fired = false
ORDER BY remind_at ASC
"""

# NOTE: atomic check-and-set - see postgres.md. Pending reminders get rescheduled
# from the DB on every bot restart, so this guards against a reminder firing twice
# if a stale in-memory job somehow survives alongside the freshly rescheduled one.
TRY_FIRE_REMINDER_SQL = """
UPDATE reminders
SET fired = true
WHERE id = $1 AND fired = false
RETURNING id, chat_id, user_id, message, remind_at, fired
"""
