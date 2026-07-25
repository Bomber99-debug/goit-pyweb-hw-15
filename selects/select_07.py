from sqlalchemy import and_

from conf.db import session
from conf.models import Grade, Group, Student, Subject


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
