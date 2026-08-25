from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)
from sqlalchemy.sql import func

from app.database import Base


class DeploymentLog(Base):
    __tablename__ = "deployment_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    deployment_id = Column(
        Integer,
        ForeignKey("deployments.id"),
        nullable=False
    )

    message = Column(
        String(1000),
        nullable=False
    )

    timestamp = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )