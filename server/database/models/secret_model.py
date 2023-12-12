from sqlalchemy import Column, String, Integer, DATETIME
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
LENGTH = 255


class Secret(Base):
    __tablename__ = "secret"
    __table_args__ = {'schema': 'iss'}

    salted_hash = Column("salted_hash", String(LENGTH), primary_key=True)
    secret_text = Column("secret_text", String(LENGTH))
    created_at = Column("created_at", DATETIME)
    expires_at = Column("expires_at", DATETIME)
    remaining_views = Column("remaining_views",  Integer)

    def __init__(self, provided_hash, secret_text, created_at, expires_at, remaining_views):
        self.salted_hash = provided_hash
        self.secret_text = secret_text
        self.created_at = created_at
        self.expires_at = expires_at
        self.remaining_views = remaining_views
