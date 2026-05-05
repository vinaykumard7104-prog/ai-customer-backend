from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.sql import func
from database import Base


class User(Base):
    """Stores users who log in via Google OAuth."""
    __tablename__ = "users"

    id        = Column(Integer, primary_key=True, index=True)
    google_id = Column(String, unique=True, index=True, nullable=False)
    email     = Column(String, unique=True, index=True, nullable=False)
    name      = Column(String, nullable=True)
    picture   = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Analytics(Base):
    """Stores customer behaviour analytics predictions."""
    __tablename__ = "analytics"

    id         = Column(Integer, primary_key=True, index=True)
    engagement = Column(Float, nullable=False)
    churn      = Column(Float, nullable=False)
    conversion = Column(Float, nullable=False)

    # Optional input fields (populated when /predict POST is used)
    time_spent = Column(Float, nullable=True)
    clicks     = Column(Integer, nullable=True)
    pages      = Column(Integer, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
