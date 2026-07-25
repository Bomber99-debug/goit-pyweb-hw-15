from sqlalchemy import func

from conf.db import session
from conf.models import Grade, Group, Student, Subject


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