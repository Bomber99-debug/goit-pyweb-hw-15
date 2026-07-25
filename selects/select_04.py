from sqlalchemy import func

from conf.db import session
from conf.models import Grade


# Знайти середній бал на потоці (по всій таблиці оцінок).
def get_avg_grade() -> None:
	avg_grade = (
			session.query(func.round(func.avg(Grade.grade), 2))
			.select_from(Grade)
			.scalar()
	)

	print(f"Average grade: {avg_grade}\n")
