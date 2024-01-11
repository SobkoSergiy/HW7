from Application import Application

def help_sam():
    print(70*"-" + '''
?, how, help - print a list of commands;          
??, sample  - print a list of samples;
q, exit, close, quit - quit the program;
          
    >> command samples:
list Teachers << show all Teachers' rows
= t << same as previous action
create Teachers 'Boris Jonson' << create a new row 'Boris Jonson' in Teachers model
+ t "Boris Jonson" << same as previous action
update Teachers 3 name 'Andry Bezos' << set name into row with id=3 in the Teachers' model
~ T 3 name 'Andry Bezos'  << same as previous action        
3 ~ t 'Andry Bezos' name  << same as previous action        
'Andry Bezos' ~ Teachers 3 name  << same as previous action        
remove Teachers 3 << delete row having id=3 in the Teachers' model
- t 3 << same as previous action 
update Ratings 3 rate '11' << set rate = 11 into row with id=3 in the Ratings' model                   
* 11 << complete the request number 11           
          
    >> command format (type parameters in any order):
(=,get,list)   model << show all model's rows 
(+,new,create) model "value" << create a new row
(-,del,remove) model id << delete row with id in the model
(~,set,update) model id field "value" << set a new field value with id row in the model 
(*,lay,query)  number << complete the request of the specified number
''' + 70*"-")

def help():
    print(70*"-" + '''
?, how, help << print a list of commands;
??, exam  << print a list of examples;
q, close, quit, exit << quit the program;
          
    >> command format (type parameters in any order):
(=,get,list)   model << show all model's rows 
(+,new,create) model "value" << create a new row
(-,del,remove) model id << delete row with id in the model
(~,set,update) model id field "value" << set a new field value with id row in the model 
(*,lay,query)  number << complete the request of the specified number
          
model:  (Students|S)(Groups|G)(Teachers|T)(Courses|C)(Ratings|R) in any case  
id:     the id code of a specific row
field:  depending on the structure of the model
"value": the actual value of the previously specified field, in quotes
          
number: request number from 1 to 12 according to the following list:
 1. Find the 5 students with the highest average score in all subjects.
 2. Find the student with the highest average score in a certain subject.
 3. Find the average score in groups for a certain subject.
 4. Find the average score on the stream (across the entire score table).
 5. Find out what courses a certain teacher teaches.
 6. Find a list of students in a certain group.
 7. Find the grades of students in a separate group on a certain subject.
 8. Find the average score given by a certain teacher in his subjects.
 9. Find the list of courses attended by the student.
10. List of courses taught to a certain student by a certain teacher.
11. The average score given by a certain teacher to a certain student.
12. Grades of students in a certain group on a certain subject in the last lesson.
''' + 70*"-")

def quotas_split(cons):
    start = end = i = 0
    flag = True

    while i < len(cons):
        if (cons[i] == "'") or (cons[i] == '"'):
            if flag: 
                start = i + 1
            else:
                end = i
            flag = not flag
        i += 1

    if start > end:
        print("error: Odd number of quotes")
        return '', None 
    if end == 0:
        return '', cons.split()
    return cons[start:end], (cons[:start-1] + cons[end+1:]).split()


def extract_action(r):
    if r in ("+", "new", "create"):
        return "new"
    if r in ("-", "del", "remove"):
        return "del"
    if r in ("~", "set", "update"):
        return "set"
    if r in ("=", "get", "list"):
        return "get"
    if r in ("*", "lay", "query"):
        return "lay"
    return ""

def extract_model(r):
    if r in ("s", "students"):
        return "students"
    if r in ("g", "groups"):
        return "groups"
    if r in ("t", "teachers"):
        return "teachers"
    if r in ("c", "courses"):
        return "courses"
    if r in ("r", "ratings"):
        return "ratings"
    return ""


def explain(consol):
    value, rest = quotas_split(consol)
    if not rest:
        return False    

    action = model = id = field = ""
    for row in rest:
        r = row.lower()
        if action == "":
            action = extract_action(r)
        if model == "": 
            model = extract_model(r)
        if (id == "") and row.isdecimal():        
            id = r
        if (field == "") and (r in ("name", "group_id", "teach_id", "rate", "week", "course_id", "stud_id")):
            field = r

    if (action == ""):
        print("input error: ACTION must be specified")
        return False
    if (action != "lay") and (model == ""):
        print("input error: MODEL must be specified")
        return False
    if action == "new": 
        if value == "":
            print("command CREATE error: no value specified")
            return False
        else:
            field = "name"
    if (action == "del") and (id == ""):
        print("command REMOVE error: no id specified")
        return False
    if (action == "set") and ((id == "") or (field == "") or (value == "")):
        print("command UPDATE error: no id or field or value specified")
        return False
    if (action == "lay") and (id == ""):
        print("command QUERY error: no id specified")
        return False
    
    order = {}
    order["act"] = action
    order["model"] = model
    order["id"] = id
    order["field"] = field
    order["value"] = value
    return order


def main():
    print("\n>>> DB_CLI 0.2.2")

    app = Application('sqlite:///alcbase7.db') 
    app.start()
    while True:
        try:
            consol = input("\nEnter the command ( ? : help;  q : quit ):\n>>>")
            match consol.strip().lower():
                case 'q' | 'quit' | 'exit' | 'close':
                    break
                case '?' | '' | 'how' | 'help':
                    help()
                case '??' | 'sample':
                    help_sam()
                case _:
                    if (order := explain(consol)):
                        app.execute(order)

        except ValueError as ve:
            print(ve)

    app.finish()


if __name__ == "__main__":
    main()
