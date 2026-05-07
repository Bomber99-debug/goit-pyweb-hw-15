from sqlalchemy import and_, func

from conf.db import session
from conf.models import Grade, Group, Student, Subject, Teacher


# Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
def get_student_max_avg_grade() -> None:
    avg_grade = func.round(func.avg(Grade.grade), 2).label("avg_grade")

    students = (
        session.query(Student.fullname, avg_grade)
        .order_by(avg_grade.desc())
        .join(Grade)
        .group_by(Student.id, Student.fullname)
        .limit(5)
    )

    output = f"{'fullname':<24} | {'avg grade'}\n{'-' * 38}\n"
    for student in students:
        output += f"{student.fullname:<24} | {student.avg_grade}\n"

    print(output)


# Знайти студента із найвищим середнім балом з певного предмета.
def get_student_subject_avg_grade(subject_id: int = 3) -> None:
    avg_grade = func.round(func.avg(Grade.grade), 2).label("avg_grade")

    subquery = (
        session.query(
            Student.fullname,
            Subject.id.label("subject_id"),
            Subject.title,
            avg_grade,
        )
        .select_from(Grade)
        .join(Student)
        .join(Subject)
        .group_by(Student.id, Student.fullname, Subject.id, Subject.title)
        .filter(Subject.id == subject_id)
        .subquery()
    )

    max_avg_grade = session.query(func.max(subquery.c.avg_grade)).scalar()

    students = (
        session.query(
            subquery.c.fullname,
            subquery.c.subject_id,
            subquery.c.title,
            subquery.c.avg_grade,
        )
        .filter(subquery.c.avg_grade == max_avg_grade)
    )

    output = f"{'fullname':<24} | {'subject':<26} | {'avg grade'}\n{'-' * 68}\n"
    for student in students:
        output += (
            f"{student.fullname:<24} | "
            f"{student.title:<26} | "
            f"{student.avg_grade}\n"
        )

    print(output)


# Знайти середній бал у групах з певного предмета.
def get_group_subject_avg_grade(subject_id: int = 3) -> None:
    avg_grade = func.round(func.avg(Grade.grade), 2).label("avg_grade")

    subquery = (
        session.query(
            Group.group_title,
            Subject.id.label("subject_id"),
            Subject.title,
            avg_grade,
        )
        .select_from(Group)
        .join(Group.students)
        .join(Student.grades)
        .join(Grade.subject)
        .group_by(Group.id, Group.group_title, Subject.id, Subject.title)
        .subquery()
    )

    groups = (
        session.query(
            subquery.c.group_title,
            subquery.c.subject_id,
            subquery.c.title,
            subquery.c.avg_grade,
        )
        .filter(subquery.c.subject_id == subject_id)
    )

    output = f"{'group':<12} | {'subject':<26} | {'avg grade'}\n{'-' * 55}\n"
    for group in groups:
        output += (
            f"{group.group_title:<12} | "
            f"{group.title:<26} | "
            f"{group.avg_grade}\n"
        )

    print(output)


# Знайти середній бал на потоці (по всій таблиці оцінок).
def get_avg_grade() -> None:
    avg_grade = (
        session.query(func.round(func.avg(Grade.grade), 2))
        .select_from(Grade)
        .scalar()
    )

    print(f"Average grade: {avg_grade}\n")


# Знайти які курси читає певний викладач.
def get_teacher_subject(teacher_id: int = 3) -> None:
    teacher_subjects = (
        session.query(
            Teacher.id.label("teacher_id"),
            Teacher.fullname,
            Subject.id.label("subject_id"),
            Subject.title,
        )
        .select_from(Teacher)
        .join(Subject)
        .filter(Teacher.id == teacher_id)
        .all()
    )

    output = f"{'teacher':<24} | {'subject':<26}\n{'-' * 55}\n"
    for subject in teacher_subjects:
        output += f"{subject.fullname:<24} | {subject.title:<26}\n"

    print(output)


# Знайти список студентів у певній групі.
def get_student_group(group_id: int = 2) -> None:
    students = (
        session.query(
            Student.id.label("student_id"),
            Student.fullname,
            Group.id.label("group_id"),
            Group.group_title,
        )
        .select_from(Group)
        .join(Student)
        .filter(Group.id == group_id)
        .all()
    )

    output = f"{'group':<12} | {'fullname':<24}\n{'-' * 42}\n"
    for student in students:
        output += f"{student.group_title:<12} | {student.fullname:<24}\n"

    print(output)


# Знайти оцінки студентів у окремій групі з певного предмета.
def get_group_student_subject_grade(group_id: int = 2, subject_id: int = 3) -> None:
    students = (
        session.query(
            Group.id.label("group_id"),
            Group.group_title,
            Student.id.label("student_id"),
            Student.fullname,
            Grade.id.label("grade_id"),
            Grade.grade,
            Subject.id.label("subject_id"),
            Subject.title,
        )
        .select_from(Group)
        .join(Student)
        .join(Grade)
        .join(Subject)
        .filter(and_(Group.id == group_id), Subject.id == subject_id)
        .all()
    )

    output = (
        f"{'group':<12} | {'fullname':<24} | {'subject':<26} | {'grade'}\n"
        f"{'-' * 78}\n"
    )
    for student in students:
        output += (
            f"{student.group_title:<12} | "
            f"{student.fullname:<24} | "
            f"{student.title:<26} | "
            f"{student.grade}\n"
        )

    print(output)


# Знайти середній бал, який ставить певний викладач зі своїх предметів.
def get_teacher_subject_avg_grade(teacher_id: int = 3) -> None:
    avg_grade = func.round(func.avg(Grade.grade), 2).label("avg_grade")

    teacher_subjects = (
        session.query(
            Teacher.id.label("teacher_id"),
            Teacher.fullname,
            Subject.id.label("subject_id"),
            Subject.title,
            avg_grade,
        )
        .select_from(Teacher)
        .join(Subject)
        .join(Grade)
        .group_by(Teacher.id, Teacher.fullname, Subject.id, Subject.title)
        .filter(Teacher.id == teacher_id)
        .all()
    )

    output = f"{'teacher':<24} | {'subject':<26} | {'avg grade'}\n{'-' * 68}\n"
    for subject in teacher_subjects:
        output += (
            f"{subject.fullname:<24} | "
            f"{subject.title:<26} | "
            f"{subject.avg_grade}\n"
        )

    print(output)


# Знайти список курсів, які відвідує певний студент.
def get_student_subject(student_id: int = 15) -> None:
    student_subjects = (
        session.query(
            Student.id.label("student_id"),
            Student.fullname,
            Subject.id.label("subject_id"),
            Subject.title,
        )
        .select_from(Grade)
        .join(Student)
        .join(Subject)
        .filter(Student.id == student_id)
        .all()
    )

    output = f"{'student':<24} | {'subject':<26}\n{'-' * 55}\n"
    for subject in student_subjects:
        output += f"{subject.fullname:<24} | {subject.title:<26}\n"

    print(output)


# Список курсів, які певному студенту читає певний викладач.
def get_student_subject_teacher(student_id: int = 15, teacher_id: int = 3) -> None:
    student_teacher_subjects = (
        session.query(
            Student.id.label("student_id"),
            Student.fullname.label("student_fullname"),
            Subject.id.label("subject_id"),
            Subject.title,
            Teacher.id.label("teacher_id"),
            Teacher.fullname.label("teacher_fullname"),
        )
        .select_from(Grade)
        .join(Student)
        .join(Subject)
        .join(Teacher)
        .filter(and_(Teacher.id == teacher_id), Student.id == student_id)
        .all()
    )

    output = (
        f"{'student':<24} | {'teacher':<24} | {'subject':<26}\n"
        f"{'-' * 82}\n"
    )
    for item in student_teacher_subjects:
        output += (
            f"{item.student_fullname:<24} | "
            f"{item.teacher_fullname:<24} | "
            f"{item.title:<26}\n"
        )

    print(output)


# Середній бал, який певний викладач ставить певному студентові.
def get_student_teacher_avg_grade(student_id: int = 15, teacher_id: int = 3) -> None:
    avg_grade = func.round(func.avg(Grade.grade), 2).label("avg_grade")

    student_teacher_avg_grades = (
        session.query(
            Student.id.label("student_id"),
            Student.fullname.label("student_fullname"),
            Teacher.id.label("teacher_id"),
            Teacher.fullname.label("teacher_fullname"),
            avg_grade,
        )
        .select_from(Grade)
        .join(Student)
        .join(Subject)
        .join(Teacher)
        .group_by(Teacher.id, Teacher.fullname, Student.id, Student.fullname)
        .filter(and_(Teacher.id == teacher_id), Student.id == student_id)
        .all()
    )

    output = (
        f"{'student':<24} | {'teacher':<24} | {'avg grade'}\n"
        f"{'-' * 68}\n"
    )
    for item in student_teacher_avg_grades:
        output += (
            f"{item.student_fullname:<24} | "
            f"{item.teacher_fullname:<24} | "
            f"{item.avg_grade}\n"
        )

    print(output)


# Оцінки студентів у певній групі з певного предмета на останньому занятті.
def get_group_student_subject_date(group_id: int = 2, subject_id: int = 4) -> None:
    subquery = (
        session.query(
            Group.id.label("group_id"),
            Group.group_title,
            Student.id.label("student_id"),
            Student.fullname,
            Subject.id.label("subject_id"),
            Subject.title,
            Grade.grade,
            Grade.date,
        )
        .select_from(Group)
        .join(Student)
        .join(Grade)
        .join(Subject)
        .filter(and_(Group.id == group_id), Subject.id == subject_id)
        .subquery()
    )

    max_date = session.query(func.max(subquery.c.date)).scalar_subquery()

    grades = (
        session.query(
            subquery.c.group_title,
            subquery.c.fullname,
            subquery.c.title,
            subquery.c.grade,
            subquery.c.date,
        )
        .filter(subquery.c.date == max_date)
        .all()
    )

    output = (
        f"{'group':<12} | {'student':<24} | {'subject':<26} | "
        f"{'grade':<6} | date\n"
        f"{'-' * 90}\n"
    )

    for grade in grades:
        output += (
            f"{grade.group_title:<12} | "
            f"{grade.fullname:<24} | "
            f"{grade.title:<26} | "
            f"{grade.grade:<6} | "
            f"{str(grade.date)}\n"
        )

    print(output)


def main():
    print("1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів.")
    get_student_max_avg_grade()

    print("2. Знайти студента із найвищим середнім балом з певного предмета.")
    get_student_subject_avg_grade()

    print("3. Знайти середній бал у групах з певного предмета.")
    get_group_subject_avg_grade()

    print("4. Знайти середній бал на потоці (по всій таблиці оцінок).")
    get_avg_grade()

    print("5. Знайти які курси читає певний викладач.")
    get_teacher_subject()

    print("6. Знайти список студентів у певній групі.")
    get_student_group()

    print("7. Знайти оцінки студентів у окремій групі з певного предмета.")
    get_group_student_subject_grade()

    print("8. Знайти середній бал, який ставить певний викладач зі своїх предметів.")
    get_teacher_subject_avg_grade()

    print("9. Знайти список курсів, які відвідує певний студент.")
    get_student_subject()

    print("10. Список курсів, які певному студенту читає певний викладач.")
    get_student_subject_teacher()

    print("11. Середній бал, який певний викладач ставить певному студентові.")
    get_student_teacher_avg_grade()

    print("12. Оцінки студентів у певній групі з певного предмета на останньому занятті.")
    get_group_student_subject_date()

if __name__ == '__main__':
    main()