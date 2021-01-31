"""Service database model."""

from sqlalchemy import Column, Integer, String  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore

from configmodel.database import Base


class ServiceDB(Base):  # type: ignore
    """ORM service object."""

    __tablename__ = "service"
    service_id = Column(Integer, primary_key=True)
    schema = Column(String(128), nullable=False)
    configs = relationship("ConfigDB", back_populates="service", cascade="all, delete")

    def __repr__(self):
        return "<id %r schema %r>" % (
            self.service_id,
            self.schema,
        )
