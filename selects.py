import selects_files


def main():
	print("1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів.")
	selects_files.get_student_max_avg_grade()

	print("2. Знайти студента із найвищим середнім балом з певного предмета.")
	selects_files.get_student_subject_avg_grade()

	print("3. Знайти середній бал у групах з певного предмета.")
	selects_files.get_group_subject_avg_grade()

	print("4. Знайти середній бал на потоці (по всій таблиці оцінок).")
	selects_files.get_avg_grade()

	print("5. Знайти які курси читає певний викладач.")
	selects_files.get_teacher_subject()

	print("6. Знайти список студентів у певній групі.")
	selects_files.get_student_group()

	print("7. Знайти оцінки студентів у окремій групі з певного предмета.")
	selects_files.get_group_student_subject_grade()

	print("8. Знайти середній бал, який ставить певний викладач зі своїх предметів.")
	selects_files.get_teacher_subject_avg_grade()

	print("9. Знайти список курсів, які відвідує певний студент.")
	selects_files.get_student_subject()

	print("10. Список курсів, які певному студенту читає певний викладач.")
	selects_files.get_student_subject_teacher()

	print("11. Середній бал, який певний викладач ставить певному студентові.")
	selects_files.get_student_teacher_avg_grade()

	print("12. Оцінки студентів у певній групі з певного предмета на останньому занятті.")
	selects_files.get_group_student_subject_date()


if __name__ == '__main__':
	main()
