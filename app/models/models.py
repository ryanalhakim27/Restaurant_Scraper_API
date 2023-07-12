from sqlalchemy import (
    Column, 
    Integer, 
    String, 
    ForeignKey, 
    Text, 
    Float, 
    Time,
    MetaData)
from sqlalchemy.orm import relationship
from app.models.database import Base, engine


class General_information(Base):
    __tablename__='general_information'

    resto_id=Column('resto_id',Integer, primary_key=True)
    resto_name=Column('resto_name',String(250))
    resto_type=Column('resto_type',String(250))
    resto_address=Column('resto_address',Text)
    resto_rating=Column('resto_rating',Float, nullable=True)
    rating_numbers=Column('rating_numbers',Integer)
    resto_link=Column('resto_link',Text)

    operation_time=relationship('Operation_time', backref='general_information',uselist=True)
    crowd_level=relationship('Crowd_level',backref='general_information',uselist=True)
    about= relationship('About_Table',backref='general_information',uselist=True)


class Operation_time(Base):
    __tablename__='operation_time'

    resto_id=Column('resto_id',Integer, ForeignKey('general_information.resto_id'),primary_key=True)
    days=Column('days',String(250),primary_key=True)
    open_hour=Column('open_hour',Time)
    close_hour=Column('close_hour',Time)


class Crowd_level(Base):
    __tablename__='crowd_level'

    resto_id=Column('resto_id',Integer, ForeignKey('general_information.resto_id'),primary_key=True)
    day=Column('day',String(250),primary_key=True)
    hour=Column('hour',String(250),primary_key=True)
    crowd_time_level=Column('crowd_time_level',String(250))


class About_Table(Base):
    __tablename__='about_table'

    resto_id=Column('resto_id',Integer, ForeignKey('general_information.resto_id'),primary_key=True)
    type_about=Column('type_about',String(250),primary_key=True)
    seq=Column('seq',Integer,primary_key=True)
    about_values=Column('about_values',String(250))



Base.metadata.create_all(bind=engine, checkfirst=True)