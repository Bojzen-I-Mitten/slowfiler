from app import db
from sqlalchemy import Column, ForeignKey, Integer, String, REAL, DateTime, Boolean, func, Float
from sqlalchemy.orm import relationship

from string import digits

class Build(db.Model):
    __tablename__ = 'Build'
    __bind_key__ = 'Dhomas'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    samples = Column(Float, nullable=False)
    build = Column(Integer, primary_key=False)

    def __init__(self, name, samples, build):
        self.name = name
        self.samples = samples
        self.build = build

    def __repr__(self):
        return self.name