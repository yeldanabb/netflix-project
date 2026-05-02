from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

movie_category = Table('movie_category', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id')),
    Column('category_id', Integer, ForeignKey('categories.id'))
)

class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True, index=True)
    show_id = Column(String, unique=True, nullable=False)
    type = Column(String)
    title = Column(String, nullable=False)
    director = Column(String)
    cast = Column(String)
    country = Column(String)
    date_added = Column(Date)
    release_year = Column(Integer)
    rating = Column(String, ForeignKey('ratings.name'))
    duration = Column(String)
    description = Column(String)

    rating_rel = relationship('Rating', back_populates='movies')
    categories = relationship('Category', secondary=movie_category, back_populates='movies')

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    movies = relationship('Movie', secondary=movie_category, back_populates='categories')

class Rating(Base):
    __tablename__ = 'ratings'
    name = Column(String, primary_key=True)
    movies = relationship('Movie', back_populates='rating_rel')

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
