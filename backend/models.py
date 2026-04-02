import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Note(Base):
    __tablename__ = "notes"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    title = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    content = sqlalchemy.Column(sqlalchemy.Text, nullable=True)