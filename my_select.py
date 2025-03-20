from sqlalchemy import select, func, desc, Numeric, cast
from sqlalchemy.orm import Session
from conf.db import SessionLocal
from entity.models import Student, Grade, Subject, Teacher, Group


# Знайти 5 студентів із найбільшим середнім балом з усіх предметів
def select_1(session: Session):
    query = (
        select(Student, func.avg(Grade.grade).label("avg_grade"))
        .join(Grade)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(5)
    )
    return session.execute(query).all()


# Знайти студента із найвищим середнім балом з певного предмета
def select_2(session: Session, subject_id: int):
    query = (
        select(Student, func.avg(Grade.grade).label("avg_grade"))
        .join(Grade)
        .where(Grade.subject_id == subject_id)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(1)
    )
    return session.execute(query).all()


# Знайти середній бал у групах з певного предмета
def select_3(session: Session, subject_id: int):
    query = (
        select(
            Group.name,
            func.round(cast(func.avg(Grade.grade), Numeric), 2).label("avg_grade"),
        )
        .join(Student, Student.group_id == Group.id)
        .join(Grade, Grade.student_id == Student.id)
        .join(Subject, Grade.subject_id == Subject.id)
        .where(Subject.id == subject_id)
        .group_by(Group.id)
    )
    return session.execute(query).all()


# Знайти середній бал на потоці (по всій таблиці оцінок)
def select_4(session: Session):
    query = select(
        func.round(func.avg(Grade.grade).cast(Numeric), 2).label("avg_grade")
    )
    return session.execute(query).scalar()


# Знайти які курси читає певний викладач
def select_5(session: Session, teacher_id: int):
    query = select(Subject.name).where(Subject.teacher_id == teacher_id)
    return session.execute(query).all()


# Знайти список студентів у певній групі
def select_6(session: Session, group_id: int):
    query = select(Student).where(Student.group_id == group_id)
    return session.execute(query).all()


# Знайти оцінки студентів у окремій групі з певного предмета
def select_7(session: Session, group_id: int, subject_id: int):
    query = (
        select(Student.full_name, Grade.grade, Grade.date_received)
        .join(Grade)
        .where(Grade.subject_id == subject_id, Student.group_id == group_id)
    )
    return session.execute(query).all()


# Знайти середній бал, який ставить певний викладач зі своїх предметів
def select_8(session: Session, teacher_id: int):
    query = (
        select(func.avg(Grade.grade).label("avg_grade"))
        .join(Subject, Grade.subject_id == Subject.id)
        .join(Teacher, Teacher.id == Subject.teacher_id)
        .where(Teacher.id == teacher_id)
    )
    return session.execute(query).scalar()


# Знайти список курсів, які відвідує певний студент
def select_9(session: Session, student_id: int):
    query = select(Subject.name).join(Grade).where(Grade.student_id == student_id)
    return session.execute(query).all()


# Список курсів, які певному студенту читає певний викладач
def select_10(session: Session, student_id: int, teacher_id: int):
    query = (
        select(Subject.name)
        .join(Grade, Grade.subject_id == Subject.id)
        .join(Teacher, Teacher.id == Subject.teacher_id)
        .where(Grade.student_id == student_id, Teacher.id == teacher_id)
    )
    return session.execute(query).all()


# Додатковий запит: Середній бал, який певний викладач ставить певному студентові
def select_11(session: Session, student_id: int, teacher_id: int):
    return (
        session.query(
            func.round(func.avg(Grade.grade).cast(Numeric), 2).label("avg_grade")
        )
        .join(Subject, Grade.subject_id == Subject.id)
        .join(Teacher, Teacher.id == Subject.teacher_id)
        .filter(Grade.student_id == student_id, Teacher.id == teacher_id)
        .scalar()
    )


# Додатковий запит: Оцінки студентів у певній групі з певного предмета на останньому занятті
def select_12(session: Session, group_id: int, subject_id: int):
    subquery = (
        select(func.max(Grade.date_received))
        .join(Student, Student.id == Grade.student_id)
        .where(Student.group_id == group_id, Grade.subject_id == subject_id)
        .scalar_subquery()
    )

    query = (
        select(Student.full_name, Grade.grade, Grade.date_received)
        .join(Grade)
        .where(
            Student.group_id == group_id,
            Grade.subject_id == subject_id,
            Grade.date_received == subquery,
        )
    )
    return session.execute(query).all()


if __name__ == "__main__":
    session: Session = SessionLocal()

    result_1 = select_1(session)
    result_2 = select_2(session, 1)
    result_3 = select_3(session, 1)
    result_4 = select_4(session)
    result_5 = select_5(session, 1)
    result_6 = select_6(session, 1)
    result_7 = select_7(session, 1, 1)
    result_8 = select_8(session, 2)
    result_9 = select_9(session, 1)
    result_10 = select_10(session, 5, 2)
    result_11 = select_11(session, 5, 5)
    result_12 = select_12(session, 1, 1)

    # Виведення результатів
    print("5 студентів із найбільшим середнім балом з усіх предметів:", result_1)
    print("Студент із найвищим середнім балом з певного предмета:", result_2)
    print("Середній бал у групах по предмету:", result_3)
    print("Середній бал на потоці:", result_4)
    print("Курси, які читає викладач:", result_5)
    print("Список студентів у групі:", result_6)
    print("Оцінки студентів у групі з предмета:", result_7)
    print("Середній бал викладача зі своїх предметів:", result_8)
    print("Список курсів студента:", result_9)
    print("Курси студента, які читає викладач:", result_10)
    print("Середній бал викладача для конкретного студента:", result_11)
    print("Оцінки студентів у групі на останньому занятті:", result_12)
