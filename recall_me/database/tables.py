from sqlalchemy import Integer  # type: ignore
from sqlalchemy import Column, DateTime, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base  # type: ignore

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


class ScreenState(DeclarativeBase):
    __tablename__ = "screen_state"
    id = Column(Integer, primary_key=True, autoincrement=True)
    state_id = Column(Integer, nullable=False, unique=True)
    state_description = Column(String(32), nullable=False, unique=True)


class EventState(DeclarativeBase):
    __tablename__ = "event_state"
    id = Column(Integer, primary_key=True, autoincrement=True)
    callback_id = Column(String(64), nullable=False, unique=True)
    user_id = Column(String(64), nullable=False)
    previous_state = Column(
        Integer, ForeignKey("screen_state.state_id", ondelete="CASCADE"), nullable=False
    )
    current_state = Column(
        Integer, ForeignKey("screen_state.state_id", ondelete="CASCADE"), nullable=False
    )
    event_metadata = Column(JSONB, nullable=True)
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )
