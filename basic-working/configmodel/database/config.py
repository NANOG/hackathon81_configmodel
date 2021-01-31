"""Config database model."""

from sqlalchemy import Column, ForeignKey, Integer, JSON, String  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore

from configmodel.database import Base


class ConfigDB(Base):  # type: ignore
    """ORM config object."""

    __tablename__ = "config"
    config_id = Column(Integer, primary_key=True)
    hostname = Column(String(128), nullable=False)
    schema = Column(String(128), nullable=False)
    config = Column(JSON, nullable=False)
    service_id = Column(Integer, ForeignKey("service.service_id"))
    service = relationship("ServiceDB", back_populates="configs")

    def __repr__(self):
        return "<id %r hostname %r schema %r>" % (
            self.config_id,
            self.hostname,
            self.schema,
        )
