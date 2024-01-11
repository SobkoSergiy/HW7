from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, desc
from models import Group, Student, Course, Teacher, Rating, Temp


def select_1(session):  # 1.Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
    q = session.query(Student.name, func.round(func.avg(Rating.rate), 2).label('ra'))\
        .select_from(Rating)\
        .join(Student).filter(Rating.stud_id == Student.id)\
        .group_by(Student.id)\
        .order_by(desc('ra'))\
        .limit(5).all()
    return q


def select_2(session):  # 2.Знайти студента із найвищим середнім балом з певного предмета.

    temp = session.query(Student.name.label('sn'), Course.name.label('cn'), func.avg(Rating.rate).label('ra'))\
        .select_from(Rating)\
        .join(Student)\
        .join(Course)\
        .where((Rating.stud_id == Student.id) and (Rating.course_id == Course.id))\
        .group_by(Student.id, Course.id)
    
    for i in temp.all():
        t = Temp(sn=i.sn, cn = i.cn, ra = i.ra)
        session.add(t)

    q = session.query(Temp.sn, Temp.cn, func.MAX(Temp.ra).label('ma'))\
        .select_from(Temp)\
        .group_by(Temp.cn)\
        .order_by(desc("ma"))\
        .all()
    return q 


def select_3(session):  # 3.Знайти середній бал у групах з певного предмета.
    q = session.query(Group.name, Course.name,  func.round(func.avg(Rating.rate), 2))\
        .select_from(Rating)\
        .join(Course).filter(Rating.course_id == Course.id)\
        .join(Student).filter(Rating.stud_id == Student.id)\
        .join(Group).filter(Student.group_id == Group.id)\
        .group_by(Course.id, Group.id)\
        .order_by(Group.id)\
        .all()
    return q


def select_4(session):  # 4.Знайти середній бал на потоці (по всій таблиці оцінок).
    q = session.query(func.round(func.avg(Rating.rate), 2)).select_from(Rating).all()
    return q
 

def select_5(session):  # 5.Знайти які курси читає певний викладач.
    q = session.query(Teacher.name, Course.name)\
        .select_from(Teacher)\
        .join(Course)\
        .order_by(Teacher.id)\
        .all()
    return q


def select_6(session):  # 6.Знайти список студентів у певній групі.
    q = session.query(Group.name, Student.name)\
        .select_from(Group)\
        .join(Student).filter(Student.group_id == Group.id)\
        .order_by(Group.id)\
        .all()
    return q                    


def select_7(session):  # 7.Знайти оцінки студентів у окремій групі з певного предмета.
    q = session.query(Group.name, Course.name, Rating.rate )\
        .select_from(Rating)\
        .join(Course).filter(Rating.course_id == Course.id)\
        .join(Student).filter(Rating.stud_id == Student.id)\
        .join(Group).filter(Student.group_id == Group.id)\
        .order_by(Group.id, Course.id)\
        .all()
    return q
 

def select_8(session):  # 8.Знайти середній бал, який ставить певний викладач зі своїх предметів.
    q = session.query(Teacher.name, Course.name, func.round(func.avg(Rating.rate), 2))\
        .select_from(Rating)\
        .join(Course).filter(Rating.course_id == Course.id)\
        .join(Teacher).filter(Course.teach_id == Teacher.id)\
        .group_by(Teacher.name, Course.name)\
        .order_by(Teacher.id)\
        .all()
    return q


def select_9(session):  # 9.Знайти список курсів, які відвідує студент.
    q = session.query(Student.name, Course.name)\
        .select_from(Rating)\
        .join(Student).filter(Rating.stud_id == Student.id)\
        .join(Course).filter(Rating.course_id == Course.id)\
        .where(Rating.week == 1)\
        .order_by(Student.id, Course.id)\
        .all()
    return q


def select_10(session): # 10.Список курсів, які певному студенту читає певний викладач.
    q = session.query(Teacher.name, Student.name, Course.name)\
        .select_from(Rating)\
        .join(Student).filter(Rating.stud_id == Student.id)\
        .join(Course).filter(Rating.course_id == Course.id)\
        .join(Teacher).filter(Course.teach_id == Teacher.id)\
        .where(Rating.week == 1)\
        .order_by(Teacher.id, Student.id, Course.id)\
        .all()
    return q    


def select_11(session): # 11. Середній бал, який певний викладач ставить певному студентові.
    q = session.query(Teacher.name, Student.name, func.round(func.avg(Rating.rate), 2))\
        .select_from(Rating)\
        .join(Student).filter(Rating.stud_id == Student.id)\
        .join(Course).filter(Rating.course_id == Course.id)\
        .join(Teacher).filter(Course.teach_id == Teacher.id)\
        .group_by(Teacher.id, Student.id)\
        .order_by(Teacher.id)\
        .all()
    return q


def select_12(session): # 12. Оцінки студентів у певній групі з певного предмета на останньому занятті.
    q = session.query(Group.name, Course.name, Rating.rate)\
        .select_from(Rating)\
        .join(Student).filter(Rating.stud_id == Student.id)\
        .join(Course).filter(Rating.course_id == Course.id)\
        .join(Group).filter(Student.group_id == Group.id)\
        .where(Rating.week == (session.query(func.max(Rating.week)).select_from(Rating).scalar_subquery()))\
        .group_by(Group.id, Course.id)\
        .order_by(Group.id, Course.id)\
        .all()
    return q    


tasks = [
"1.Знайти 5 студентів із найбільшим середнім балом з усіх предметів.",
"2.Знайти студента із найвищим середнім балом з певного предмета.",
"3.Знайти середній бал у групах з певного предмета.",
"4.Знайти середній бал на потоці (по всій таблиці оцінок).",
"5.Знайти які курси читає певний викладач.",
"6.Знайти список студентів у певній групі.",
"7.Знайти оцінки студентів у окремій групі з певного предмета.",
"8.Знайти середній бал, який ставить певний викладач зі своїх предметів.",
"9.Знайти список курсів, які відвідує студент.",
"10.Список курсів, які певному студенту читає певний викладач.",
"11. Середній бал, який певний викладач ставить певному студентові.",
"12. Оцінки студентів у певній групі з певного предмета на останньому занятті."
]

def execute_query(task, session):
    t = int(task) if 1 <= int(task) <= 12 else 1
    print(f"\n>> #{tasks[t-1]}")

    query = globals()[f'select_{task}'](session)
    if query:
        for i in query:
            print(i)
        print(f">> total: {len(query)} rows")


if __name__ == "__main__":

    def help():
        for t in tasks:
            print(t)

    def main():
        engine = create_engine('sqlite:///alcbase7.db', echo=False)  # :memory:
        DBSession = sessionmaker(bind=engine)
        session = DBSession()

        while True:
            try:
                consol = input("\nEnter the query number (? : help;  ex: exit):\n>>>")
                consol = consol.strip()
                if consol == "?":
                    help()
                elif consol == "ex":
                    break
                else:
                    if consol.isdigit():
                        execute_query(consol, session)
                    else:
                        print("sorry, I did not understand consol input")

            except ValueError as ve:
                print(ve)
    
        session.close()

    main()