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
# NOTE: superseded by chat_activity_daily below (weekday-merged rows can't tell an
# isolated spike from consistent daily activity - see chat_activity_daily). Kept
# here, still created, but no longer written to - it holds real historical data
# from before the migration and dropping/touching it isn't worth the risk for a
# table nobody queries anymore. New peak hour/weekday stats start fresh in
# chat_activity_daily from the migration date onward.
CREATE_CHAT_ACTIVITY_TIMELINE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS chat_activity_timeline (
    chat_id BIGINT NOT NULL,
    hour_of_day SMALLINT NOT NULL,
    weekday SMALLINT NOT NULL,
    message_count BIGINT NOT NULL DEFAULT 0,
    PRIMARY KEY (chat_id, hour_of_day, weekday)
)
"""

# NOTE: chat-level (not per-user), so no FK to group_members - see CLAUDE.md rule 8.
# One row per real calendar day (not merged by weekday like chat_activity_timeline
# was), so COUNT(*) in a GROUP BY is a genuine, unbounded sample size instead of a
# count capped at 7 (weekdays) or 24 (hours) - see GET_PEAK_HOUR_SQL/GET_PEAK_WEEKDAY_SQL.
CREATE_CHAT_ACTIVITY_DAILY_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS chat_activity_daily (
    chat_id BIGINT NOT NULL,
    activity_date DATE NOT NULL,
    hour_of_day SMALLINT NOT NULL,
    message_count BIGINT NOT NULL DEFAULT 0,
    PRIMARY KEY (chat_id, activity_date, hour_of_day)
)
"""

REGISTER_MESSAGE_SQL = """
INSERT INTO user_message_stats (chat_id, user_id, period_month, message_count)
VALUES ($1, $2, $3, 1)
ON CONFLICT (chat_id, user_id, period_month) DO UPDATE SET message_count = user_message_stats.message_count + 1
"""

REGISTER_DAILY_ACTIVITY_SQL = """
INSERT INTO chat_activity_daily (chat_id, activity_date, hour_of_day, message_count)
VALUES ($1, $2, $3, 1)
ON CONFLICT (chat_id, activity_date, hour_of_day)
DO UPDATE SET message_count = chat_activity_daily.message_count + 1
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

# NOTE: plain AVG(message_count) is biased toward slots with few active days (an
# isolated spike on 1-2 days can outrank a slot active every day with more total
# volume). chat_activity_daily has one row per real calendar day, so COUNT(*) per
# hour is now a genuine, unbounded sample size (unlike the old chat_activity_timeline,
# capped at 7 weekdays) - so we shrink each hour's average toward the chat's overall
# per-active-hour average, in proportion to how few days that hour has on record
# (empirical Bayes / Laplace-style smoothing, "k" pseudo-observations of the global
# average). This scales correctly as more real days accumulate, unlike a fixed
# ceiling: an hour with 50 days on record barely gets shrunk, one with 2 days does.
GET_PEAK_HOUR_SQL = """
WITH per_hour AS (
    SELECT hour_of_day, SUM(message_count)::numeric AS total, COUNT(*)::numeric AS days
    FROM chat_activity_daily
    WHERE chat_id = $1
    GROUP BY hour_of_day
),
chat_average AS (
    SELECT SUM(total) / NULLIF(SUM(days), 0) AS global_avg, LEAST(AVG(days), 7) AS k
    FROM per_hour
)
SELECT per_hour.hour_of_day
FROM per_hour, chat_average
ORDER BY (per_hour.total + chat_average.k * chat_average.global_avg) / (per_hour.days + chat_average.k) DESC
LIMIT 1
"""

GET_PEAK_WEEKDAY_SQL = """
WITH per_weekday AS (
    SELECT (EXTRACT(ISODOW FROM activity_date)::int - 1) AS weekday,
           SUM(message_count)::numeric AS total, COUNT(*)::numeric AS days
    FROM chat_activity_daily
    WHERE chat_id = $1
    GROUP BY weekday
),
chat_average AS (
    SELECT SUM(total) / NULLIF(SUM(days), 0) AS global_avg, LEAST(AVG(days), 7) AS k
    FROM per_weekday
)
SELECT per_weekday.weekday
FROM per_weekday, chat_average
ORDER BY (per_weekday.total + chat_average.k * chat_average.global_avg) / (per_weekday.days + chat_average.k) DESC
LIMIT 1
"""
