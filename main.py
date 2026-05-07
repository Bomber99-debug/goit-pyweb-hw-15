from argparse import Namespace
from cli_parser import build_parser

import create
import my_select
from seeds import seed_db

def dispatch_command(args: Namespace):
    if args.auto:
        create.main()
    elif args.init_docker:
        create.docker_create_container()
    elif args.edit_alembic:
        create.edit_setting_alembic(args.container_name)
    elif args.create_migration:
        create.create_migrate_db()
    elif args.upgrade_db:
        create.application_migrate_db()
    elif args.insert_db:
        create.insert_db()
    elif args.run_queries:
        create.get_db()

    elif args.student_max_avg_grade:
        my_select.get_student_max_avg_grade()
    elif args.student_subject_avg_grade:
        my_select.get_student_subject_avg_grade()
    elif args.group_subject_avg_grade:
        my_select.get_group_subject_avg_grade()
    elif args.avg_grade:
        my_select.get_avg_grade()
    elif args.teacher_subject:
        my_select.get_teacher_subject()
    elif args.student_group:
        my_select.get_student_group()
    elif args.group_student_subject_grade:
        my_select.get_group_student_subject_grade()
    elif args.teacher_subject_avg_grade:
        my_select.get_teacher_subject_avg_grade()
    elif args.student_subject:
        my_select.get_student_subject()
    elif args.student_subject_teacher:
        my_select.get_student_subject_teacher()
    elif args.teacher_avg_grade:
        my_select.get_student_teacher_avg_grade()
    elif args.group_student_subject_date:
        my_select.get_group_student_subject_date()

    elif args.entity is not None:
        entity, action = args.entity, args.action
        match (entity, action):
            case ("group", "create"):
                seed_db.create_group(args.title)
            case ("group", "delete"):
                seed_db.remove_group(args.id)
            case ("group", "edit"):
                seed_db.update_group(args.id, args.title)

            case ("student", "create"):
                seed_db.create_student(args.first_name, args.last_name)
            case ("student", "delete"):
                seed_db.remove_student(args.id)
            case ("student", "edit"):
                seed_db.update_student(args.first_name, args.last_name, args.id)
            case ("student", "edit_group"):
                seed_db.update_group_student(args.group_id, args.id)

            case ("teacher", "create"):
                seed_db.create_teacher(args.first_name, args.last_name)
            case ("teacher", "delete"):
                seed_db.remove_teacher(args.id)
            case ("teacher", "edit"):
                seed_db.update_teacher(args.first_name, args.last_name, args.id)

            case ("subject", "create"):
                seed_db.create_subject(args.title, args.teacher_id)
            case ("subject", "delete"):
                seed_db.remove_subject(args.id)
            case ("subject", "edit"):
                seed_db.update_subject(args.title, args.id)
            case ("subject", "edit_teacher"):
                seed_db.update_teacher_subject(args.teacher_id, args.id)

            case ("grade", "create"):
                seed_db.create_grade(args.student_id, args.subject_id, args.grade, args.grade_date)
            case ("grade", "delete"):
                seed_db.remove_grade(args.id)
            case ("grade", "edit"):
                seed_db.update_grade(args.id, args.grade, args.grade_date)
            case _:
                parser.print_help()
    else:
        parser.print_help()


if __name__ == '__main__':
    parser = build_parser()
    args = parser.parse_args()
    dispatch_command(args)
