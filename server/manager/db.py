from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

from server.config.factory import settings

Base = declarative_base()
engine = create_engine(url=settings.RDS_URL)
