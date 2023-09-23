from sqlalchemy import Column, ForeignKey, Integer, MetaData, String, Table

metadata = MetaData()

event_table = Table(
    "event",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String(64), nullable=False),
    Column("description", String(128), nullable=False),
    Column("event_day", Integer, nullable=False),
    Column("event_month", Integer, nullable=False),
    Column("voice_id", String(128), nullable=True),
    Column("source_text", String(256), nullable=True),
    Column("author_id", String(64), nullable=False),
)

config_table = Table(
    "event_config",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("event_id", Integer, ForeignKey("event.id"), nullable=False),
    Column("duration", Integer, nullable=False, server_default="2"),
    Column("start_hour", Integer, nullable=False, server_default="-1"),
    Column("notify_before_days", Integer, nullable=False, server_default="7"),
)
