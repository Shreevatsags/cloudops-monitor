from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)
from sqlalchemy.sql import func

from app.database import Base


class Deployment(Base):
    __tablename__ = "deployments"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    application_id = Column(
        Integer,
        ForeignKey("applications.id"),
        nullable=False
    )

    version = Column(
        String(100),
        nullable=False
    )

    status = Column(
        String(50),
        default="pending",
        nullable=False
    )

    started_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    completed_at = Column(
        DateTime(timezone=True),
        nullable=True
    )