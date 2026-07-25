
from conf.db import session
from conf.models import Subject, Teacher


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
