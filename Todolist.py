from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import date, timedelta

engine = create_engine('sqlite:///to_do_list.db')

Base = declarative_base()


class TodoList(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=date.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def get_date(day=0):
    """Returns a date object with who's date is relative to date of today"""
    new_date = date.today() + timedelta(days=day)
    return new_date


def get_missed_tasks():
    """Prints all uncompleted tasks that has exceeded deadline"""
    missed_tasks = session.query(TodoList).order_by(TodoList.deadline).filter(TodoList.deadline < date.today()).all()
    print('Missed tasks:')
    if missed_tasks:
        num = 1
        for task in missed_tasks:
            print(f"{num}. {task.task}")
            num += 1
        print()
    else:
        print("Nothing is missed!")
        print()


def delete_task():
    tasks = session.query(TodoList).order_by(TodoList.deadline).all()
    if tasks:
        print('Chose the number of the task you want to delete:')
        num = 1
        for task in tasks:
            print(f"{num}. {task.task}")
            num += 1
        task_to_delete = input()
        task_no = int(task_to_delete) + 1
        session.delete(tasks[task_no])
        session.commit()
        print('Task has been deleted!')
        print()
    else:
        print("Nothing to delete!")
        print()


def get_week_tasks():
    """Prints week sum of tasks on to do list"""
    for i in range(7):
        deadline = get_date(i)
        get_task_of_date(deadline)
        print()


def get_task_of_date(deadline=date.today()):
    """Prints the task/s of the given date if no date give prints task for the day"""
    print(f"{deadline.strftime('%A')} {deadline.strftime('%d')} {deadline.strftime('%b')}:")
    tasks = session.query(TodoList).order_by(TodoList.id).filter_by(deadline=deadline).all()
    if tasks:
        num = 1
        for task in tasks:
            print(f"{num}. {task.task}")
            num += 1
        print()
    else:
        print("Nothing to do!")
        print()


def add_task():
    """Requests task description and deadline and add to list"""
    task = input('Enter task >>')
    deadline = input('Enter deadline in YYY-MM-DD >>')
    deadline = date.fromisoformat(deadline)
    record = TodoList(task=task, deadline=deadline)
    session.add(record)
    session.commit()
    print('The task has been added!')
    print()


def get_all_tasks():
    """Prints all task on to do list"""
    print('All tasks:')
    num = 1
    for record in session.query(TodoList).order_by(TodoList.id):
        print(f"{num}. {record.task}")
        num += 1
    print()


menu_items = {
    '1': get_task_of_date,
    '2': get_week_tasks,
    '3': get_all_tasks,
    '4': get_missed_tasks,
    '5': add_task,
    '6': delete_task
}


def menu():
    global menu_items
    while True:
        print(
            "1) Today's tasks",
            "2) Week's tasks",
            "3) All tasks",
            "4) Missed tasks",
            "5) Add task",
            "6) Delete task",
            "0) Exit",
            sep='\n')
        action = input('Enter menu bar item number >>')
        if action == '0':
            session.close()
            print('Bye, Good Luck! Love from Dominic')
            break
        else:
            try:
                menu_items[action]()
            except KeyError:
                continue


menu()
