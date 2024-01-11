from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from models import Group, Student, Course, Teacher, Rating, Temp
from my_select import execute_query



class Application:
    def __init__(self, data):
        self.data = data
        self.session = None

    def start(self):
        engine = create_engine(self.data, echo=False)  # :memory:
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()  # Session()
        print("The session was successfully opened")

    def finish(self):
        self.session.close()
        print("The session was closed")


    def execute(self, order):
        print(f"\n>> execute: {order=}")
        act = order.get("act", '')
        if act == "lay":
            execute_query(order.get("id", ''), self.session)
        elif act in ("new", "del", "set", "get"):
            getattr(self, f'{act}_data')(order)
        else:
            print("error: unknown actions")


    def new_data(self, order):
        model = order['model']
        val = order['value']
        print(f"create: model = {model.capitalize()!r}, value = {val!r}")

        if model == "students":
            row = Student(name = val, group_id = 1)
        elif model == "groups":
            row = Group(name = val)
        elif model == "teachers":
            row = Teacher(name = val)
        elif model == "courses":
            row = Course(name = val, teach_id = 1)
        else: # model == "ratings"
            row = Rating(rate = int(val), week = 1, group_id=1, teach_id=1)

        self.session.add(row)
        self.session.commit()


    def set_data(self, order):  
        model = order['model']
        id = int(order['id'])
        val = order['value']
        print(f"set: model = {model.capitalize()!r}, id = {id}, value = {val!r}")

        if model == "students":
            row = self.session.query(Student).get(id)
            row.name = val
        elif model == "groups":
            row = self.session.query(Group).get(id)
            row.name = val
        elif model == "teachers":
            row = self.session.query(Teacher).get(id)
            row.name = val
        elif model == "courses":
            row = self.session.query(Course).get(id)
            row.name = val
        else: # model == "ratings"
            row = self.session.query(Rating).get(id)
            row.rate = int(val)

        self.session.add(row)
        self.session.commit()


    def del_data(self, order):
        model = order['model']
        id = int(order['id'])
        print(f"delete: model = {model.capitalize()!r}, id = {id}")

        if model == "students":
            row = self.session.query(Student).get(id)
        elif model == "groups":
            row = self.session.query(Group).get(id)
        elif model == "teachers":
            row = self.session.query(Teacher).get(id)
        elif model == "courses":
            row = self.session.query(Course).get(id)
        else: # model == "ratings"
            row = self.session.query(Rating).get(id)

        self.session.delete(row)
        self.session.commit()


    def get_data(self, order):
        model = order['model']
        print(f"list: model = {model.capitalize()!r}")

        if model == "students":
            for i in self.session.query(Student).all():
                print(f'id: {i.id:2}| group_id: {i.group_id:2}| name: {i.name}')
        elif model == "groups":
            for i in self.session.query(Group).all():
                print(f'id: {i.id:2}| name: {i.name}')
        elif model == "teachers":
            for i in self.session.query(Teacher).all():
                print(f'id: {i.id:2}| name: {i.name}')
        elif model == "courses":
            for i in self.session.query(Course).all():
                print(f'id: {i.id:2}| teach_id: {i.teach_id:2}| name: {i.name}')
        else: # model == "ratings"
            for i in self.session.query(Rating).all():
                print(f'id: {i.id:3}| rate: {i.rate:2}| week: {i.week:2}| course_id: {i.course_id:2}| stud_id: {i.stud_id:2}')




