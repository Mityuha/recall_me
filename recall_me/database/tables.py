from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base

DeclarativeBase: type = declarative_base()
metadata = DeclarativeBase.metadata  # type: ignore


class EventTable(DeclarativeBase):
    __tablename__ = "event"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(64), nullable=False)
    description = Column(String(128), nullable=False)
    event_day = Column(Integer, nullable=False)
    event_month = Column(Integer, nullable=False)
    voice_id = Column(String(128), nullable=True)
    source_text = Column(String(256), nullable=True)
    author_id = Column(String(64), nullable=False)


class EventConfigTable(DeclarativeBase):
    __tablename__ = "event_config"

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(
        Integer,
        ForeignKey("event.id", ondelete="CASCADE"),
        nullable=False,
    )
    duration = Column(Integer, nullable=False, server_default="2")
    start_hour = Column(Integer, nullable=False, server_default="-1")
    notify_before_days = Column(Integer, nullable=False, server_default="7")
