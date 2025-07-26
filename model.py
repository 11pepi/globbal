from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
import db

class URLs(db.Base):
    __tablename__ = "URLs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String)
    title = Column(String)

    # One-to-many: one URL has many keywords
    keywords = relationship("Keywords", back_populates="url")

class Keywords(db.Base):
    __tablename__ = "keywords"
    id = Column(Integer, primary_key=True, autoincrement=True)
    word = Column(String, index=True)
    weight = Column(Integer)
    url_id = Column(ForeignKey("URLs.id"), index=True)

    # Many-to-one: each keyword links to one URL
    url = relationship("URLs", back_populates="keywords")
