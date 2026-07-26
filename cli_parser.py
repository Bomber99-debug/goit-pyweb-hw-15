import argparse
from datetime import date

from cli_help import (
    ACTION_HELP,
    AUTO_HELP,
    CONTAINER_NAME,
    CREATE_MIGRATION_HELP,
    EDIT_ALEMBIC_HELP,
    GRADE_CREATE_HELP,
    GRADE_DATE_HELP,
    GRADE_DELETE_HELP,
    GRADE_EDIT_HELP,
    GRADE_HELP,
    GRADE_VALUE_HELP,
    GROUP_CREATE_HELP,
    GROUP_DELETE_HELP,
    GROUP_EDIT_HELP,
    GROUP_HELP,
    GROUP_ID_HELP,
    ID_HELP,
    INIT_DOCKER_HELP,
    INSERT_DB_HELP,
    MODEL_HELP,
    NAME_HELP,
    PROGRAM_DESCRIPTION,
    PROGRAM_EPILOG,
    PROGRAM_NAME,
    RUN_QUERIES_HELP,
    SELECT_AVG_GRADE,
    SELECT_GROUP_STUDENT_SUBJECT_DATE,
    SELECT_GROUP_STUDENT_SUBJECT_GRADE,
    SELECT_GROUP_SUBJECT_AVG_GRADE,
    SELECT_STUDENT_GROUP,
    SELECT_STUDENT_MAX_AVG_GRADE,
    SELECT_STUDENT_SUBJECT,
    SELECT_STUDENT_SUBJECT_AVG_GRADE,
    SELECT_STUDENT_SUBJECT_TEACHER,
    SELECT_TEACHER_AVG_GRADE,
    SELECT_TEACHER_SUBJECT,
    SELECT_TEACHER_SUBJECT_AVG_GRADE,
    STUDENT_CREATE_HELP,
    STUDENT_DELETE_HELP,
    STUDENT_EDIT_GROUP_HELP,
    STUDENT_EDIT_HELP,
    STUDENT_HELP,
    STUDENT_ID_HELP,
    SUBJECT_CREATE_HELP,
    SUBJECT_DELETE_HELP,
    SUBJECT_EDIT_HELP,
    SUBJECT_EDIT_TEACHER_HELP,
    SUBJECT_HELP,
    SUBJECT_ID_HELP,
    TEACHER_CREATE_HELP,
    TEACHER_DELETE_HELP,
    TEACHER_EDIT_HELP,
    TEACHER_HELP,
    TEACHER_ID_HELP,
    UPGRADE_DB_HELP,
)


def normalize_model(value: str) -> str:
    """
    Перетворює назву моделі з формату Teacher
    у внутрішній формат teacher.
    """

    model = value.strip().lower()

    available_models = {
        "group",
        "student",
        "teacher",
        "subject",
        "grade",
    }

    if model not in available_models:
        available = ", ".join(sorted(available_models))

        raise argparse.ArgumentTypeError(
            f"Невідома модель: {value}. Доступні моделі: {available}"
        )

    return model


def normalize_action(value: str) -> str:
    """
    Перетворює назви операцій із завдання на назви,
    які вже використовуються у dispatch_command.
    """

    actions = {
        "create": "create",
        "list": "list",
        "update": "edit",
        "remove": "delete",
        # Залишаємо підтримку старих назв операцій.
        "edit": "edit",
        "delete": "delete",
    }

    action = value.strip().lower()

    if action not in actions:
        available = "create, list, update, remove"

        raise argparse.ArgumentTypeError(
            f"Невідома операція: {value}. Доступні операції: {available}"
        )

    return actions[action]


class NameAction(argparse.Action):
    """
    Обробляє універсальний аргумент --name.

    Для Group і Subject повне значення використовується як title.
    Для Student і Teacher значення розділяється
    на first_name та last_name.
    """

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: str,
        option_string: str | None = None,
    ) -> None:
        full_name = values.strip()

        if not full_name:
            raise argparse.ArgumentError(
                self,
                "Значення --name не може бути порожнім.",
            )

        name_parts = full_name.split(maxsplit=1)

        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) == 2 else ""

        setattr(namespace, self.dest, full_name)
        setattr(namespace, "title", full_name)
        setattr(namespace, "first_name", first_name)
        setattr(namespace, "last_name", last_name)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=PROGRAM_NAME,
        description=PROGRAM_DESCRIPTION,
        epilog=PROGRAM_EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Команди підготовки та запуску проєкту
    # ---------------------------------------------------------------------
    parser.add_argument(
        "-A",
        "--auto",
        action="store_true",
        help=AUTO_HELP,
    )

    parser.add_argument(
        "-D",
        "--init-docker",
        action="store_true",
        help=INIT_DOCKER_HELP,
    )

    parser.add_argument(
        "-C",
        "--container-name",
        type=str,
        default="dev-pyweb-15",
        help=CONTAINER_NAME,
    )

    parser.add_argument(
        "-E",
        "--edit-alembic",
        action="store_true",
        help=EDIT_ALEMBIC_HELP,
    )

    parser.add_argument(
        "-M",
        "--create-migration",
        action="store_true",
        help=CREATE_MIGRATION_HELP,
    )

    parser.add_argument(
        "-U",
        "--upgrade-db",
        action="store_true",
        help=UPGRADE_DB_HELP,
    )

    parser.add_argument(
        "-I",
        "--insert-db",
        action="store_true",
        help=INSERT_DB_HELP,
    )

    parser.add_argument(
        "-Q",
        "--run-queries",
        action="store_true",
        help=RUN_QUERIES_HELP,
    )

    # CRUD у форматі, який вимагається в домашньому завданні.
    # ---------------------------------------------------------------------
    # Приклад:
    # py main.py --action create --model Teacher --name "Boris Jonson"
    parser.add_argument(
        "-a",
        "--action",
        type=normalize_action,
        help=ACTION_HELP,
    )

    parser.add_argument(
        "-m",
        "--model",
        dest="entity",
        type=normalize_model,
        help=MODEL_HELP,
    )

    parser.add_argument(
        "-n",
        "--name",
        action=NameAction,
        help=NAME_HELP,
    )

    parser.add_argument(
        "--id",
        type=int,
        help=ID_HELP,
    )

    parser.add_argument(
        "--group-id",
        type=int,
        help=GROUP_ID_HELP,
    )

    parser.add_argument(
        "--teacher-id",
        type=int,
        help=TEACHER_ID_HELP,
    )

    parser.add_argument(
        "--student-id",
        type=int,
        help=STUDENT_ID_HELP,
    )

    parser.add_argument(
        "--subject-id",
        type=int,
        help=SUBJECT_ID_HELP,
    )

    parser.add_argument(
        "--grade",
        type=int,
        help=GRADE_VALUE_HELP,
    )

    parser.add_argument(
        "--date",
        "--grade-date",
        dest="grade_date",
        type=date.fromisoformat,
        help=GRADE_DATE_HELP,
    )

    # Ці значення потрібні main.py
    # для універсального CRUD-формату.
    parser.set_defaults(
        title=None,
        first_name=None,
        last_name=None,
    )

    # Старий формат із підкомандами залишається доступним.
    # Наприклад: py main.py teacher create Boris Jonson
    commands = parser.add_subparsers(dest="entity")

    # Models
    # ---------------------------------------------------------------------
    # Group
    group_parser = commands.add_parser(
        "group",
        help=GROUP_HELP,
    )

    group_actions = group_parser.add_subparsers(
        dest="action",
        required=True,
    )

    create_group = group_actions.add_parser(
        "create",
        help=GROUP_CREATE_HELP,
    )
    create_group.add_argument(
        "title",
        type=str,
    )

    delete_group = group_actions.add_parser(
        "delete",
        help=GROUP_DELETE_HELP,
    )
    delete_group.add_argument(
        "id",
        type=int,
    )

    edit_group = group_actions.add_parser(
        "edit",
        help=GROUP_EDIT_HELP,
    )
    edit_group.add_argument(
        "id",
        type=int,
    )
    edit_group.add_argument(
        "title",
        type=str,
    )

    # Student
    student_parser = commands.add_parser(
        "student",
        help=STUDENT_HELP,
    )

    student_actions = student_parser.add_subparsers(
        dest="action",
        required=True,
    )

    create_student = student_actions.add_parser(
        "create",
        help=STUDENT_CREATE_HELP,
    )
    create_student.add_argument(
        "first_name",
        type=str,
    )
    create_student.add_argument(
        "last_name",
        type=str,
    )
    create_student.add_argument(
        "group_id",
        type=int,
    )

    delete_student = student_actions.add_parser(
        "delete",
        help=STUDENT_DELETE_HELP,
    )
    delete_student.add_argument(
        "id",
        type=int,
    )

    edit_student = student_actions.add_parser(
        "edit",
        help=STUDENT_EDIT_HELP,
    )
    edit_student.add_argument(
        "id",
        type=int,
    )
    edit_student.add_argument(
        "first_name",
        type=str,
    )
    edit_student.add_argument(
        "last_name",
        type=str,
    )

    edit_student_group = student_actions.add_parser(
        "edit_group",
        help=STUDENT_EDIT_GROUP_HELP,
    )
    edit_student_group.add_argument(
        "id",
        type=int,
    )
    edit_student_group.add_argument(
        "group_id",
        type=int,
    )

    # Teacher
    teacher_parser = commands.add_parser(
        "teacher",
        help=TEACHER_HELP,
    )

    teacher_actions = teacher_parser.add_subparsers(
        dest="action",
        required=True,
    )

    create_teacher = teacher_actions.add_parser(
        "create",
        help=TEACHER_CREATE_HELP,
    )
    create_teacher.add_argument(
        "first_name",
        type=str,
    )
    create_teacher.add_argument(
        "last_name",
        type=str,
    )

    delete_teacher = teacher_actions.add_parser(
        "delete",
        help=TEACHER_DELETE_HELP,
    )
    delete_teacher.add_argument(
        "id",
        type=int,
    )

    edit_teacher = teacher_actions.add_parser(
        "edit",
        help=TEACHER_EDIT_HELP,
    )
    edit_teacher.add_argument(
        "id",
        type=int,
    )
    edit_teacher.add_argument(
        "first_name",
        type=str,
    )
    edit_teacher.add_argument(
        "last_name",
        type=str,
    )

    # Subject
    subject_parser = commands.add_parser(
        "subject",
        help=SUBJECT_HELP,
    )

    subject_actions = subject_parser.add_subparsers(
        dest="action",
        required=True,
    )

    create_subject = subject_actions.add_parser(
        "create",
        help=SUBJECT_CREATE_HELP,
    )
    create_subject.add_argument(
        "title",
        type=str,
    )
    create_subject.add_argument(
        "teacher_id",
        type=int,
    )

    delete_subject = subject_actions.add_parser(
        "delete",
        help=SUBJECT_DELETE_HELP,
    )
    delete_subject.add_argument(
        "id",
        type=int,
    )

    edit_subject = subject_actions.add_parser(
        "edit",
        help=SUBJECT_EDIT_HELP,
    )
    edit_subject.add_argument(
        "id",
        type=int,
    )
    edit_subject.add_argument(
        "title",
        type=str,
    )

    edit_subject_teacher = subject_actions.add_parser(
        "edit_teacher",
        help=SUBJECT_EDIT_TEACHER_HELP,
    )
    edit_subject_teacher.add_argument(
        "id",
        type=int,
    )
    edit_subject_teacher.add_argument(
        "teacher_id",
        type=int,
    )

    # Grade
    grade_parser = commands.add_parser(
        "grade",
        help=GRADE_HELP,
    )

    grade_actions = grade_parser.add_subparsers(
        dest="action",
        required=True,
    )

    create_grade = grade_actions.add_parser(
        "create",
        help=GRADE_CREATE_HELP,
    )
    create_grade.add_argument(
        "student_id",
        type=int,
    )
    create_grade.add_argument(
        "subject_id",
        type=int,
    )
    create_grade.add_argument(
        "grade",
        type=int,
    )
    create_grade.add_argument(
        "grade_date",
        type=date.fromisoformat,
    )

    delete_grade = grade_actions.add_parser(
        "delete",
        help=GRADE_DELETE_HELP,
    )
    delete_grade.add_argument(
        "id",
        type=int,
    )

    edit_grade = grade_actions.add_parser(
        "edit",
        help=GRADE_EDIT_HELP,
    )
    edit_grade.add_argument(
        "id",
        type=int,
    )
    edit_grade.add_argument(
        "grade",
        type=int,
    )
    edit_grade.add_argument(
        "grade_date",
        type=date.fromisoformat,
    )

    # Select
    # ---------------------------------------------------------------------

    # Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
    parser.add_argument(
        "--student-max-avg-grade",
        "--student_max_avg_grade",
        dest="student_max_avg_grade",
        action="store_true",
        help=SELECT_STUDENT_MAX_AVG_GRADE,
    )

    # Знайти студента із найвищим середнім балом з певного предмета.
    parser.add_argument(
        "--student-subject-avg-grade",
        "--student_subject_avg_grade",
        dest="student_subject_avg_grade",
        action="store_true",
        help=SELECT_STUDENT_SUBJECT_AVG_GRADE,
    )

    # Знайти середній бал у групах з певного предмета.
    parser.add_argument(
        "--group-subject-avg-grade",
        "--group_subject_avg_grade",
        dest="group_subject_avg_grade",
        action="store_true",
        help=SELECT_GROUP_SUBJECT_AVG_GRADE,
    )

    # Знайти середній бал на потоці (по всій таблиці оцінок).
    parser.add_argument(
        "--avg-grade",
        "--avg_grade",
        dest="avg_grade",
        action="store_true",
        help=SELECT_AVG_GRADE,
    )

    # Знайти які курси читає певний викладач.
    parser.add_argument(
        "--teacher-subject",
        "--teacher_subject",
        dest="teacher_subject",
        action="store_true",
        help=SELECT_TEACHER_SUBJECT,
    )

    # Знайти список студентів у певній групі.
    parser.add_argument(
        "--student-group",
        "--student_group",
        dest="student_group",
        action="store_true",
        help=SELECT_STUDENT_GROUP,
    )

    # Знайти оцінки студентів у окремій групі з певного предмета.
    parser.add_argument(
        "--group-student-subject-grade",
        "--group_student_subject_grade",
        dest="group_student_subject_grade",
        action="store_true",
        help=SELECT_GROUP_STUDENT_SUBJECT_GRADE,
    )

    # Знайти середній бал, який ставить певний викладач зі своїх предметів.
    parser.add_argument(
        "--teacher-subject-avg-grade",
        "--teacher_subject_avg_grade",
        dest="teacher_subject_avg_grade",
        action="store_true",
        help=SELECT_TEACHER_SUBJECT_AVG_GRADE,
    )

    # Знайти список курсів, які відвідує певний студент.
    parser.add_argument(
        "--student-subject",
        "--student_subject",
        dest="student_subject",
        action="store_true",
        help=SELECT_STUDENT_SUBJECT,
    )

    # Список курсів, які певному студенту читає певний викладач.
    parser.add_argument(
        "--student-subject-teacher",
        "--student_subject_teacher",
        dest="student_subject_teacher",
        action="store_true",
        help=SELECT_STUDENT_SUBJECT_TEACHER,
    )

    # Середній бал, який певний викладач ставить певному студентові.
    parser.add_argument(
        "--teacher-avg-grade",
        "--teacher_avg_grade",
        dest="teacher_avg_grade",
        action="store_true",
        help=SELECT_TEACHER_AVG_GRADE,
    )

    # Оцінки студентів у певній групі з певного предмета на останньому занятті.
    parser.add_argument(
        "--group-student-subject-date",
        "--group_student_subject_date",
        dest="group_student_subject_date",
        action="store_true",
        help=SELECT_GROUP_STUDENT_SUBJECT_DATE,
    )

    return parser
