from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    Unicode,
    Time,
    ForeignKey,
    )
# from webhelpers.text import urlify
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    )
from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Truck(Base):
    __tablename__ = 'trucks'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    location = relationship('Locations')
    cuisine = Column(Text)
    payment = Column(Text)
    twitter = Column(Text)
    website = Column(Text)

    @classmethod
    def all(cls):
        return DBSession.query(cls).order_by(cls.name).all()

    @classmethod
    def by_id(cls, id):
        return DBSession.query(cls).filter(cls.id == id).one()

    @classmethod
    def add_truck(cls, request):
        name = request.params.get('name', None)
        cuisine = request.params.get('cuisine', None)
        payment = request.params.get('payment', None)
        twitter = request.params.get('twitter', None)
        website = request.params.get('website', None)
        new_entry = cls(name=name, cuisine=cuisine, payment=payment,
                        twitter=twitter, website=website)
        DBSession.add(new_entry)


class Locations(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    truck_id = Column(Integer, ForeignKey('trucks.id'))
    day = Column(Text)
    start_time = Column(Time)
    end_time = Column(Time)
    address = Column(Text)
    neighborhood = Column(Text)

    def __str__(self):
        return self.neighborhood

    def __repr__(self):
        return self.neighborhood


Index('truck_index', Truck.name, unique=True, mysql_length=255)
