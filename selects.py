from selects_files import (
    select_01,
    select_02,
    select_03,
    select_04,
    select_05,
    select_06,
    select_07,
    select_08,
    select_09,
    select_10,
    select_11,
    select_12,
)


def main():
    print("1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів.")
    select_01.get_student_max_avg_grade()

    print("2. Знайти студента із найвищим середнім балом з певного предмета.")
    select_02.get_student_subject_avg_grade()

    print("3. Знайти середній бал у групах з певного предмета.")
    select_03.get_group_subject_avg_grade()

    print("4. Знайти середній бал на потоці (по всій таблиці оцінок).")
    select_04.get_avg_grade()

    print("5. Знайти які курси читає певний викладач.")
    select_05.get_teacher_subject()

    print("6. Знайти список студентів у певній групі.")
    select_06.get_student_group()

    print("7. Знайти оцінки студентів у окремій групі з певного предмета.")
    select_07.get_group_student_subject_grade()

    print("8. Знайти середній бал, який ставить певний викладач зі своїх предметів.")
    select_08.get_teacher_subject_avg_grade()

    print("9. Знайти список курсів, які відвідує певний студент.")
    select_09.get_student_subject()

    print("10. Список курсів, які певному студенту читає певний викладач.")
    select_10.get_student_subject_teacher()

    print("11. Середній бал, який певний викладач ставить певному студентові.")
    select_11.get_student_teacher_avg_grade()

    print(
        "12. Оцінки студентів у певній групі з певного предмета на останньому занятті."
    )
    select_12.get_group_student_subject_date()


if __name__ == "__main__":
    main()
