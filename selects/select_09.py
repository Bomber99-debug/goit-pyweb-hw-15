
from conf.db import session
from conf.models import Grade, Student, Subject


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
