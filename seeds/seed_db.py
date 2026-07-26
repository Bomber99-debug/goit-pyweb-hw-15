from datetime import date
from random import randint

from sqlalchemy.exc import SQLAlchemyError

from conf.db import session
from conf.models import Grade, Group, Student, Subject, Teacher

from .fake_data import fake

GROUPS = 3
STUDENTS = randint(30, 50)
TEACHERS = randint(3, 5)
SUBJECTS = randint(5, 8)


# Group
def insert_groups(number_groups: int):
    num = 0
    for _ in range(number_groups):
        group = Group(
            group_title=fake.groups()
        )
        session.add(group)
        num += 1
    print(f"Груп створено: {num}")


def create_group(group_title: str) -> None:
    group = Group(
        group_title=group_title
    )
    session.add(group)
    session.commit()


def remove_group(group_id: int):
    group = session.query(Group).filter_by(id=group_id).first()
    session.delete(group)
    session.commit()


def update_group(group_id: int, title: str):
    group = session.query(Group).filter_by(id=group_id).first()
    group.group_title = title
    session.commit()


# Student
def insert_students(number_student: int) -> None:
    num = 0
    for _ in range(number_student):
        student = Student(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            group_id=randint(1, GROUPS)
        )
        session.add(student)
        num += 1
    print(f"Студентів створено: {num}")


def create_student(first_name: str, last_name: str, group_id: int):
    student = Student(
        first_name=first_name,
        last_name=last_name,
        group_id=group_id
    )
    session.add(student)
    session.commit()


def remove_student(student_id: int):
    student = session.query(Student).filter_by(id=student_id).first()
    session.delete(student)
    session.commit()


def update_student(first_name: str, last_name: str, student_id: int):
    student = session.query(Student).filter_by(id=student_id).first()
    student.first_name = first_name
    student.last_name = last_name
    session.commit()


def update_group_student(group_id: int, student_id: int):
    student = session.query(Student).filter_by(id=student_id).first()
    student.group_id = group_id
    session.commit()


# Teacher
def insert_teachers(number_teacher: int) -> None:
    num = 0
    for _ in range(number_teacher):
        teacher = Teacher(
            first_name=fake.first_name(),
            last_name=fake.last_name()
        )
        session.add(teacher)
        num += 1
    print(f"Вчителів створено: {num}")


def create_teacher(first_name: str, last_name: str):
    teacher = Teacher(
        first_name=first_name,
        last_name=last_name,
    )
    session.add(teacher)
    session.commit()


def remove_teacher(teacher_id: int):
    teacher = session.query(Teacher).filter_by(id=teacher_id).first()
    session.delete(teacher)
    session.commit()


def update_teacher(first_name: str, last_name: str, teacher_id: int):
    teacher = session.query(Teacher).filter_by(id=teacher_id).first()
    teacher.first_name = first_name
    teacher.last_name = last_name
    session.commit()


# Subject
def insert_subjects(number_subjects: int) -> None:
    num = 0
    for _ in range(number_subjects):
        subject = Subject(
            title=fake.subjects(),
            teacher_id=randint(1, TEACHERS)
        )
        session.add(subject)
        num += 1
    print(f"Предметів створено: {num}")


def create_subject(title: str, teacher_id: int):
    subject = Subject(
        title=title,
        teacher_id=teacher_id,
    )
    session.add(subject)
    session.commit()


def remove_subject(subject_id: int):
    subject = session.query(Subject).filter_by(id=subject_id).first()
    session.delete(subject)
    session.commit()


def update_subject(title: str, subject_id: int):
    subject = session.query(Subject).filter_by(id=subject_id).first()
    subject.title = title
    session.commit()


def update_teacher_subject(teacher_id: int, subject_id: int):
    subject = session.query(Subject).filter_by(id=subject_id).first()
    subject.teacher_id = teacher_id
    session.commit()


# Grade
def insert_grades() -> None:
    num = 0
    students = session.query(Student).all()

    for _ in range(2):
        for number, student in enumerate(students):
            grade = Grade(
                student_id=number + 1,
                subject_id=randint(1, SUBJECTS),
                grade=randint(1, 12),
                date=fake.date_between(start_date='-5y')
            )
            session.add(grade)
            num += 1
    print(f"Оцінок створено: {num}")


def create_grade(student_id: int, subject_id: int, grade: int, grade_date: date):
    grade = Grade(
        student_id=student_id,
        subject_id=subject_id,
        grade=grade,
        date=grade_date
    )
    session.add(grade)
    session.commit()


def remove_grade(grade_id: int):
    grade = session.query(Grade).filter_by(id=grade_id).first()
    session.delete(grade)
    session.commit()


def update_grade(grade_id: int, grade_grade: int, grade_date: date):
    grade = session.query(Grade).filter_by(id=grade_id).first()
    grade.grade = grade_grade
    grade.date = grade_date
    session.commit()


def main() -> None:
    try:
        print('Генерацію фейковий груп')
        insert_groups(GROUPS)
        print('Генерація фейкових вчителів')
        insert_teachers(TEACHERS)
        print('Запис в БД')
        session.commit()

        print('Генерація фейкових студентів')
        insert_students(STUDENTS)
        print('Генерація фейкових предметів')
        insert_subjects(SUBJECTS)
        print('Запис в БД')
        session.commit()

        print('Генерація фейкових оцінок')
        insert_grades()
        print('Запис в БД')
        session.commit()
    except SQLAlchemyError as err:
        print(err)
        session.rollback()
    finally:
        session.close()


if __name__ == '__main__':
    main()
