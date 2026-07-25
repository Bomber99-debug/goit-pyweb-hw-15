from sqlalchemy import func

from conf.db import session
from conf.models import Grade, Student


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