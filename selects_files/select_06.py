
from conf.db import session
from conf.models import Group, Student


# Знайти список студентів у певній групі.
def get_student_group(group_id: int = 2) -> None:
	students = (
			session.query(
					Student.id.label("student_id"),
					Student.fullname,
					Group.id.label("group_id"),
					Group.group_title,
					)
			.select_from(Group)
			.join(Student)
			.filter(Group.id == group_id)
			.all()
	)

	output = f"{'group':<12} | {'fullname':<24}\n{'-' * 42}\n"
	for student in students:
		output += f"{student.group_title:<12} | {student.fullname:<24}\n"

	print(output)
