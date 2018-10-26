from app import db
from sqlalchemy import Column, ForeignKey, Integer, String, REAL, DateTime, Boolean, func, Float
from sqlalchemy.orm import relationship

from string import digits

class Function_build(db.Model):
    __tablename__ = 'Function_build'
    __bind_key__ = 'Dhomas'

    id = Column(Integer, primary_key=True)
    function_name = Column(String(100), nullable=False)
    avg = Column(Float, nullable=False)
    std = Column(Float, nullable=False)
    max = Column(Float, nullable=False)
    min = Column(Float, nullable=False)
    build = Column(Integer, primary_key=False)

    def __init__(self, name, samples, build):
        self.name = name
        self.samples = samples
        self.build = build

    def __repr__(self):
        return self.name


class Build_time(db.Model):
    __tablename__ = 'Build_time'
    __bind_key__ = 'Dhomas'


    id = Column(Integer, primary_key=True)
    build_number = Column(Integer, primary_key=False)
    build_duration = Column(Integer, primary_key=False)


    def __init__(self, build_number, build_duration):
        self.build_number = build_number
        self.build_duration = build_duration

    def __repr__(self):
        return str(self.build_duration)
