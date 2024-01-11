from random import randint
import faker
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from models import Group, Student, Course, Teacher, Rating


TOTAL_GROUPS = 3
TOTAL_STUDENTS = 30
TOTAL_TEACHERS = 4
TOTAL_COURSES = 5
TOTAL_RATINGS = 4

engine = create_engine('sqlite:///alcbase7.db', echo=False)  # :memory:
DBSession = sessionmaker(bind=engine)
session = DBSession()
fr = faker.Faker()


for i in range(TOTAL_GROUPS):
    g = Group(name=f"Group{i+1}")
    session.add(g)
session.commit()    

for i in range(TOTAL_STUDENTS):
    g = i%TOTAL_GROUPS + 1
    s = Student(name=fr.name()+f" {i+1} <g{g}>", group_id=g)
    session.add(s)
session.commit()    

for i in range(TOTAL_TEACHERS):
    t = Teacher(name= fr.name() + f" {i+1}")
    session.add(t)
session.commit()    

for i in range(TOTAL_COURSES):
    t = i%TOTAL_TEACHERS + 1
    c = Course(name= f"Course{i+1} <t{t}>", teach_id=t)
    session.add(c)
session.commit()    

for i in range(TOTAL_RATINGS):  
    for s in range(TOTAL_STUDENTS):
        for j in range(TOTAL_COURSES):
            r = Rating(rate=randint(1, 20), week=i+1, stud_id=s+1 , course_id=j+1)
            session.add(r)
session.commit()    

for i in session.query(Group).all():
    print(f'Group: id: {i.id}, name: {i.name}')

for i in session.query(Student).all():
    print(f'Student: id: {i.id}, name: {i.name}, group_id: {i.group_id}')

for i in session.query(Teacher).all():
    print(f'Teacher: id: {i.id}, name: {i.name}')

for i in session.query(Course).all():
    print(f'Course: id: {i.id}, name: {i.name}, teach_id: {i.teach_id}')

for i in session.query(Rating).all():
    print(f'Rating: id: {i.id}, rate: {i.rate}, week: {i.week}, course_id: {i.course_id}, stud_id: {i.stud_id}')


session.close()
