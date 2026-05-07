from argparse import Namespace
from cli_parser import build_parser


def dispatch_command(arguments: Namespace):
    import create
    import my_select

    if arguments.auto:
        create.main()
    elif arguments.init_docker:
        create.docker_create_container(arguments.container_name)
    elif arguments.edit_alembic:
        create.edit_setting_alembic()
    elif arguments.create_migration:
        create.create_migrate_db()
    elif arguments.upgrade_db:
        create.application_migrate_db()
    elif arguments.insert_db:
        create.insert_db()
    elif arguments.run_queries:
        create.get_db()

    elif arguments.student_max_avg_grade:
        my_select.get_student_max_avg_grade()
    elif arguments.student_subject_avg_grade:
        my_select.get_student_subject_avg_grade()
    elif arguments.group_subject_avg_grade:
        my_select.get_group_subject_avg_grade()
    elif arguments.avg_grade:
        my_select.get_avg_grade()
    elif arguments.teacher_subject:
        my_select.get_teacher_subject()
    elif arguments.student_group:
        my_select.get_student_group()
    elif arguments.group_student_subject_grade:
        my_select.get_group_student_subject_grade()
    elif arguments.teacher_subject_avg_grade:
        my_select.get_teacher_subject_avg_grade()
    elif arguments.student_subject:
        my_select.get_student_subject()
    elif arguments.student_subject_teacher:
        my_select.get_student_subject_teacher()
    elif arguments.teacher_avg_grade:
        my_select.get_student_teacher_avg_grade()
    elif arguments.group_student_subject_date:
        my_select.get_group_student_subject_date()

    elif arguments.entity is not None:
        from seeds import seed_db
        entity, action = arguments.entity, arguments.action
        match (entity, action):
            case ("group", "create"):
                seed_db.create_group(arguments.title)
            case ("group", "delete"):
                seed_db.remove_group(arguments.id)
            case ("group", "edit"):
                seed_db.update_group(arguments.id, arguments.title)

            case ("student", "create"):
                seed_db.create_student(arguments.first_name, arguments.last_name, arguments.group_id)
            case ("student", "delete"):
                seed_db.remove_student(arguments.id)
            case ("student", "edit"):
                seed_db.update_student(arguments.first_name, arguments.last_name, arguments.id)
            case ("student", "edit_group"):
                seed_db.update_group_student(arguments.group_id, arguments.id)

            case ("teacher", "create"):
                seed_db.create_teacher(arguments.first_name, arguments.last_name)
            case ("teacher", "delete"):
                seed_db.remove_teacher(arguments.id)
            case ("teacher", "edit"):
                seed_db.update_teacher(arguments.first_name, arguments.last_name, arguments.id)

            case ("subject", "create"):
                seed_db.create_subject(arguments.title, arguments.teacher_id)
            case ("subject", "delete"):
                seed_db.remove_subject(arguments.id)
            case ("subject", "edit"):
                seed_db.update_subject(arguments.title, arguments.id)
            case ("subject", "edit_teacher"):
                seed_db.update_teacher_subject(arguments.teacher_id, arguments.id)

            case ("grade", "create"):
                seed_db.create_grade(arguments.student_id, arguments.subject_id, arguments.grade, arguments.grade_date)
            case ("grade", "delete"):
                seed_db.remove_grade(arguments.id)
            case ("grade", "edit"):
                seed_db.update_grade(arguments.id, arguments.grade, arguments.grade_date)
            case _:
                parser.print_help()
    else:
        parser.print_help()


if __name__ == '__main__':
    parser = build_parser()
    args = parser.parse_args()
    dispatch_command(args)
