from sqlalchemy import and_, func

from conf.db import session
from conf.models import Grade, Student, Subject, Teacher


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
