from sqlalchemy import and_, func

from conf.db import session
from conf.models import Grade, Group, Student, Subject


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
