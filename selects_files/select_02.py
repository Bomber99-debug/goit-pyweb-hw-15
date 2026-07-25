from sqlalchemy import func

from conf.db import session
from conf.models import Grade, Student, Subject


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