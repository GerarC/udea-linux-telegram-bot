CREATE_USER_MESSAGE_STATS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS user_message_stats (
    chat_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    period_month DATE NOT NULL,
    message_count BIGINT NOT NULL DEFAULT 0,
    PRIMARY KEY (chat_id, user_id, period_month),
    FOREIGN KEY (chat_id, user_id) REFERENCES group_members (chat_id, user_id)
)
"""

HAS_PERIOD_MONTH_COLUMN_SQL = """
SELECT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'user_message_stats' AND column_name = 'period_month'
)
"""

# NOTE: this table predates monthly tracking and was never used by the deployed bot
# (feature not yet released), so dropping the pre-migration table loses no real data.
DROP_LEGACY_USER_MESSAGE_STATS_TABLE_SQL = "DROP TABLE IF EXISTS user_message_stats"

# NOTE: chat-level (not per-user), so no FK to group_members - see CLAUDE.md rule 8.
CREATE_CHAT_ACTIVITY_TIMELINE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS chat_activity_timeline (
    chat_id BIGINT NOT NULL,
    hour_of_day SMALLINT NOT NULL,
    weekday SMALLINT NOT NULL,
    message_count BIGINT NOT NULL DEFAULT 0,
    PRIMARY KEY (chat_id, hour_of_day, weekday)
)
"""

REGISTER_MESSAGE_SQL = """
INSERT INTO user_message_stats (chat_id, user_id, period_month, message_count)
VALUES ($1, $2, $3, 1)
ON CONFLICT (chat_id, user_id, period_month) DO UPDATE SET message_count = user_message_stats.message_count + 1
"""

REGISTER_TIMELINE_SQL = """
INSERT INTO chat_activity_timeline (chat_id, hour_of_day, weekday, message_count)
VALUES ($1, $2, $3, 1)
ON CONFLICT (chat_id, hour_of_day, weekday) DO UPDATE SET message_count = chat_activity_timeline.message_count + 1
"""

GET_MONTHLY_RANKING_SQL = """
SELECT gm.user_id, gm.username, ums.message_count
FROM user_message_stats ums
JOIN group_members gm ON gm.chat_id = ums.chat_id AND gm.user_id = ums.user_id
WHERE ums.chat_id = $1 AND ums.period_month = $2
ORDER BY ums.message_count DESC
LIMIT $3
"""

GET_ALL_TIME_RANKING_SQL = """
SELECT gm.user_id, gm.username, SUM(ums.message_count)::bigint AS message_count
FROM user_message_stats ums
JOIN group_members gm ON gm.chat_id = ums.chat_id AND gm.user_id = ums.user_id
WHERE ums.chat_id = $1
GROUP BY gm.user_id, gm.username
ORDER BY message_count DESC
LIMIT $2
"""

GET_MONTHLY_STATS_SQL = """
SELECT message_count, rank FROM (
    SELECT user_id, message_count, RANK() OVER (ORDER BY message_count DESC) AS rank
    FROM user_message_stats
    WHERE chat_id = $1 AND period_month = $2
) ranked
WHERE user_id = $3
"""

GET_ALL_TIME_STATS_SQL = """
SELECT message_count, rank FROM (
    SELECT user_id, SUM(message_count)::bigint AS message_count,
           RANK() OVER (ORDER BY SUM(message_count) DESC) AS rank
    FROM user_message_stats
    WHERE chat_id = $1
    GROUP BY user_id
) ranked
WHERE user_id = $2
"""

GET_CHAT_MONTHLY_TOTALS_SQL = """
SELECT COALESCE(SUM(message_count), 0)::bigint AS total, COUNT(DISTINCT user_id) AS participants
FROM user_message_stats
WHERE chat_id = $1 AND period_month = $2
"""

GET_CHAT_ALL_TIME_TOTAL_SQL = """
SELECT COALESCE(SUM(message_count), 0)::bigint AS total
FROM user_message_stats
WHERE chat_id = $1
"""

GET_PEAK_HOUR_SQL = """
SELECT hour_of_day
FROM chat_activity_timeline
WHERE chat_id = $1
GROUP BY hour_of_day
ORDER BY AVG(message_count) DESC
LIMIT 1
"""

GET_PEAK_WEEKDAY_SQL = """
SELECT weekday
FROM chat_activity_timeline
WHERE chat_id = $1
GROUP BY weekday
ORDER BY AVG(message_count) DESC
LIMIT 1
"""
