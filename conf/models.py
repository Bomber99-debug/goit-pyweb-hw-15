from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    group_title = Column(String(150))
    students = relationship("Student", back_populates="group")


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(150))
    last_name = Column(String(150))
    group_id = Column(Integer, ForeignKey('groups.id', onupdate="CASCADE"))
    group = relationship("Group", back_populates="students")
    grades = relationship("Grade", back_populates="student")

    @hybrid_property
    def fullname(self):
        return self.first_name + " " + self.last_name


class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(150))
    last_name = Column(String(150))
    subjects = relationship("Subject", back_populates="teacher")

    @hybrid_property
    def fullname(self):
        return self.first_name + " " + self.last_name


class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True)
    title = Column(String(150))
    teacher_id = Column(Integer, ForeignKey('teachers.id', onupdate="CASCADE"))
    teacher = relationship("Teacher", back_populates="subjects")
    grades = relationship("Grade", back_populates="subject")


class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id", onupdate="CASCADE", ondelete="CASCADE"))
    subject_id = Column(Integer, ForeignKey("subjects.id", onupdate="CASCADE", ondelete="CASCADE"))
    grade = Column(Integer)
    date = Column(Date)
    subject = relationship("Subject", back_populates="grades")
    student = relationship("Student", back_populates="grades")
