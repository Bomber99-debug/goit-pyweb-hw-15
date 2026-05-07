PROGRAM_NAME = "sqlalchemy-alembic-demo"

PROGRAM_DESCRIPTION = (
    "CLI-інструмент для навчального проєкту з SQLAlchemy, Alembic, "
    "PostgreSQL у Docker, фейковими даними та SQL-вибірками."
)

AUTO_HELP = (
    "Запустити повний сценарій: створити Docker-контейнер, "
    "підготувати Alembic, створити й застосувати міграції, "
    "заповнити БД фейковими даними та виконати SQL-вибірки."
)

INIT_DOCKER_HELP = "Створити та запустити Docker-контейнер з PostgreSQL."
CONTAINER_NAME = "Назва Docker-контейнера PostgreSQL."
EDIT_ALEMBIC_HELP = "Підготувати конфігурацію Alembic для роботи з моделями проєкту."
CREATE_MIGRATION_HELP = "Створити нову міграцію Alembic на основі SQLAlchemy-моделей."
UPGRADE_DB_HELP = "Застосувати міграції до бази даних."
INSERT_DB_HELP = "Згенерувати фейкові дані та заповнити ними базу даних."
RUN_QUERIES_HELP = "Запустити навчальні SQL-вибірки та вивести результати."

GROUP_HELP = "Керування групами."
GROUP_CREATE_HELP = "Створити нову групу."
GROUP_DELETE_HELP = "Видалити групу за ID."
GROUP_EDIT_HELP = "Змінити назву групи."

STUDENT_HELP = "Керування студентами."
STUDENT_CREATE_HELP = "Створити нового студента."
STUDENT_DELETE_HELP = "Видалити студента за ID."
STUDENT_EDIT_HELP = "Змінити ім’я та прізвище студента."
STUDENT_EDIT_GROUP_HELP = "Перевести студента в іншу групу."

TEACHER_HELP = "Керування викладачами."
TEACHER_CREATE_HELP = "Створити нового викладача."
TEACHER_DELETE_HELP = "Видалити викладача за ID."
TEACHER_EDIT_HELP = "Змінити ім’я та прізвище викладача."

SUBJECT_HELP = "Керування предметами."
SUBJECT_CREATE_HELP = "Створити новий предмет і прив’язати його до викладача."
SUBJECT_DELETE_HELP = "Видалити предмет за ID."
SUBJECT_EDIT_HELP = "Змінити назву предмета."
SUBJECT_EDIT_TEACHER_HELP = "Змінити викладача для предмета."

GRADE_HELP = "Керування оцінками."
GRADE_CREATE_HELP = "Додати оцінку студенту з певного предмета."
GRADE_DELETE_HELP = "Видалити оцінку за ID."
GRADE_EDIT_HELP = "Змінити оцінку або дату оцінювання."

SELECT_STUDENT_MAX_AVG_GRADE = "Знайти 5 студентів із найбільшим середнім балом з усіх предметів."
SELECT_STUDENT_SUBJECT_AVG_GRADE = "Знайти студента із найвищим середнім балом з певного предмета."
SELECT_GROUP_SUBJECT_AVG_GRADE = "Знайти середній бал у групах з певного предмета."
SELECT_AVG_GRADE = "Знайти середній бал на потоці (по всій таблиці оцінок)."
SELECT_TEACHER_SUBJECT = "Знайти які курси читає певний викладач."
SELECT_STUDENT_GROUP = "Знайти список студентів у певній групі."
SELECT_GROUP_STUDENT_SUBJECT_GRADE = "Знайти оцінки студентів у окремій групі з певного предмета."
SELECT_TEACHER_SUBJECT_AVG_GRADE = "Знайти середній бал, який ставить певний викладач зі своїх предметів."
SELECT_STUDENT_SUBJECT = "Знайти список курсів, які відвідує певний студент."
SELECT_STUDENT_SUBJECT_TEACHER = "Список курсів, які певному студенту читає певний викладач."
SELECT_TEACHER_AVG_GRADE = "Середній бал, який певний викладач ставить певному студентові."
SELECT_GROUP_STUDENT_SUBJECT_DATE = "Оцінки студентів у певній групі з певного предмета на останньому занятті."
