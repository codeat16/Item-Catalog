import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class UserID(Base):
    __tablename__ = 'userid'

    id = Column(Integer, primary_key=True)
    idstring = Column(String(250), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'idstring': self.idstring,
            'id': self.id,
        }


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('userid.id'))
    userid = relationship(UserID)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }


class Item(Base):
    __tablename__ = 'item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
        }


# set check_same_thread to False to deal with this version of sqlite error:
# ProgrammingError: (sqlite3.ProgrammingError) SQLite objects created in a
# thread can only be used in that same thread.
engine = create_engine(
    'sqlite:///itemcatalog.db',
    connect_args={'check_same_thread': False}
    )


Base.metadata.create_all(engine)
