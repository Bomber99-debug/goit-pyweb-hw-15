from sqlalchemy import func

from conf.db import session
from conf.models import Grade, Subject, Teacher


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
