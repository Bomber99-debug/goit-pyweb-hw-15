from argparse import ArgumentParser, Namespace
from cli_parser import build_parser
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

def dispatch_command(arguments: Namespace, parser: ArgumentParser) -> None:
    import create
    import selects_files

    if arguments.auto:
        print("Запуск повного сценарію проєкту...")
        create.main()

    elif arguments.init_docker:
        print(f"Створення Docker-контейнера: {arguments.container_name}")
        create.docker_create_container(arguments.container_name)

    elif arguments.edit_alembic:
        print("Підготовка Alembic...")
        create.init_migrate_db()

    elif arguments.create_migration:
        print("Створення нової міграції...")
        create.create_migrate_db()

    elif arguments.upgrade_db:
        print("Застосування міграцій до бази даних...")
        create.application_migrate_db()

    elif arguments.insert_db:
        print("Заповнення бази даних фейковими даними...")
        create.insert_db()

    elif arguments.run_queries:
        print("Запуск усіх SQL-вибірок...")
        create.get_db()

    elif arguments.student_max_avg_grade:
        print("Вибірка: 5 студентів із найбільшим середнім балом.")
        select_01.get_student_max_avg_grade()

    elif arguments.student_subject_avg_grade:
        print("Вибірка: студент із найвищим середнім балом з предмета.")
        select_02.get_student_subject_avg_grade()

    elif arguments.group_subject_avg_grade:
        print("Вибірка: середній бал у групах з предмета.")
        select_03.get_group_subject_avg_grade()

    elif arguments.avg_grade:
        print("Вибірка: середній бал на потоці.")
        select_04.get_avg_grade()

    elif arguments.teacher_subject:
        print("Вибірка: предмети певного викладача.")
        select_05.get_teacher_subject()

    elif arguments.student_group:
        print("Вибірка: студенти певної групи.")
        select_06.get_student_group()

    elif arguments.group_student_subject_grade:
        print("Вибірка: оцінки студентів групи з предмета.")
        select_07.get_group_student_subject_grade()

    elif arguments.teacher_subject_avg_grade:
        print("Вибірка: середній бал викладача з його предметів.")
        select_08.get_teacher_subject_avg_grade()

    elif arguments.student_subject:
        print("Вибірка: предмети певного студента.")
        select_09.get_student_subject()

    elif arguments.student_subject_teacher:
        print("Вибірка: предмети студента у певного викладача.")
        select_10.get_student_subject_teacher()

    elif arguments.teacher_avg_grade:
        print("Вибірка: середній бал викладача певному студенту.")
        select_11.get_student_teacher_avg_grade()

    elif arguments.group_student_subject_date:
        print("Вибірка: оцінки групи з предмета на останньому занятті.")
        select_12.get_group_student_subject_date()

    elif arguments.entity is not None:
        from seeds import seed_db

        entity, action = arguments.entity, arguments.action

        match (entity, action):
            case ("group", "create"):
                print(f"Створення групи: {arguments.title}")
                seed_db.create_group(arguments.title)

            case ("group", "delete"):
                print(f"Видалення групи з ID: {arguments.id}")
                seed_db.remove_group(arguments.id)

            case ("group", "edit"):
                print(f"Оновлення групи з ID: {arguments.id}")
                seed_db.update_group(arguments.id, arguments.title)

            case ("student", "create"):
                print(
                    f"Створення студента: "
                    f"{arguments.first_name} {arguments.last_name}, "
                    f"group_id={arguments.group_id}"
                )
                seed_db.create_student(
                    arguments.first_name,
                    arguments.last_name,
                    arguments.group_id,
                )

            case ("student", "delete"):
                print(f"Видалення студента з ID: {arguments.id}")
                seed_db.remove_student(arguments.id)

            case ("student", "edit"):
                print(f"Оновлення студента з ID: {arguments.id}")
                seed_db.update_student(
                    arguments.first_name,
                    arguments.last_name,
                    arguments.id,
                )

            case ("student", "edit_group"):
                print(
                    f"Зміна групи студента ID={arguments.id} "
                    f"на group_id={arguments.group_id}"
                )
                seed_db.update_group_student(arguments.group_id, arguments.id)

            case ("teacher", "create"):
                print(
                    f"Створення викладача: "
                    f"{arguments.first_name} {arguments.last_name}"
                )
                seed_db.create_teacher(arguments.first_name, arguments.last_name)

            case ("teacher", "delete"):
                print(f"Видалення викладача з ID: {arguments.id}")
                seed_db.remove_teacher(arguments.id)

            case ("teacher", "edit"):
                print(f"Оновлення викладача з ID: {arguments.id}")
                seed_db.update_teacher(
                    arguments.first_name,
                    arguments.last_name,
                    arguments.id,
                )

            case ("subject", "create"):
                print(
                    f"Створення предмета: {arguments.title}, "
                    f"teacher_id={arguments.teacher_id}"
                )
                seed_db.create_subject(arguments.title, arguments.teacher_id)

            case ("subject", "delete"):
                print(f"Видалення предмета з ID: {arguments.id}")
                seed_db.remove_subject(arguments.id)

            case ("subject", "edit"):
                print(f"Оновлення предмета з ID: {arguments.id}")
                seed_db.update_subject(arguments.title, arguments.id)

            case ("subject", "edit_teacher"):
                print(
                    f"Зміна викладача для предмета ID={arguments.id} "
                    f"на teacher_id={arguments.teacher_id}"
                )
                seed_db.update_teacher_subject(arguments.teacher_id, arguments.id)

            case ("grade", "create"):
                print(
                    f"Створення оцінки: student_id={arguments.student_id}, "
                    f"subject_id={arguments.subject_id}, "
                    f"grade={arguments.grade}, "
                    f"date={arguments.grade_date}"
                )
                seed_db.create_grade(
                    arguments.student_id,
                    arguments.subject_id,
                    arguments.grade,
                    arguments.grade_date,
                )

            case ("grade", "delete"):
                print(f"Видалення оцінки з ID: {arguments.id}")
                seed_db.remove_grade(arguments.id)

            case ("grade", "edit"):
                print(f"Оновлення оцінки з ID: {arguments.id}")
                seed_db.update_grade(
                    arguments.id,
                    arguments.grade,
                    arguments.grade_date,
                )

            case _:
                parser.print_help()

    else:
        parser.print_help()


if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()

    dispatch_command(args, parser)