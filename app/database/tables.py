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

    def __init__(self, name, avg, std, max, min, build):
        self.function_name = name
        self.avg = avg
        self.build = build
        self.std = std
        self.max = max
        self.min = min

    def __repr__(self):
        return self.function_name

    def __gt__(self, other):
        return self.id > other.id

class Build_data(db.Model):
    __tablename__ = 'Build_data'
    __bind_key__ = 'Dhomas'


    id = Column(Integer, primary_key=True)
    build_number = Column(Integer, primary_key=False)
    build_time_duration = Column(Integer, primary_key=False)
    build_ramusage = Column(Float, nullable=False)
    build_vramusage = Column(Float, nullable=False)

    def __init__(self, build_number, build_time_duration, build_ramusage, build_vramusage):
        self.build_number = build_number
        self.build_time_duration = build_time_duration
        self.build_ramusage = build_ramusage
        self.build_vramusage = build_vramusage

    def __gt__(self, other):
        self.build_number > other.build_number

    def __repr__(self):
        return str(self.build_time_duration)
