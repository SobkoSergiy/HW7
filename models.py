from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, REAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///alcbase7.db', echo=False)  # :memory:
DBSession = sessionmaker(bind=engine)
session = DBSession()
Base = declarative_base()


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(7), nullable=False)

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'))
    group = relationship(Group)
    

class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)

class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False)
    teach_id = Column(Integer, ForeignKey('teachers.id'))
    teach = relationship(Teacher)


class Rating(Base):
    __tablename__ = 'ratings'
    id = Column(Integer, primary_key=True)
    rate = Column(Integer, nullable=False)
    week = Column(Integer, nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'))
    course = relationship(Course)
    stud_id = Column(Integer, ForeignKey('students.id'))
    stud = relationship(Student)

class Temp(Base):
    __tablename__ = 'temps'
    id = Column(Integer, primary_key=True)
    sn = Column(String(40), nullable=False)
    cn = Column(String(25), nullable=False)
    ra = Column(REAL, nullable=False)

Base.metadata.create_all(engine)
Base.metadata.bind = engine

session.close()
print("Tables created")
