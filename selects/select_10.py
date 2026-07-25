from sqlalchemy import and_

from conf.db import session
from conf.models import Grade, Student, Subject, Teacher


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
