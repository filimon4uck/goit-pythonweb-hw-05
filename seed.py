import argparse
import sys
from entity.models import Teacher, Group, Student, Subject, Grade
from conf.db import SessionLocal


def create_teacher(first_name, last_name, email, phone=None):
    session = SessionLocal()
    try:
        teacher = Teacher(
            first_name=first_name, last_name=last_name, email=email, phone=phone
        )
        session.add(teacher)
        session.commit()
        print(f"Teacher '{first_name} {last_name}' created successfully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()


def list_teachers():
    session = SessionLocal()
    try:
        teachers = session.query(Teacher).all()
        if not teachers:
            print("No teachers found.")
        for teacher in teachers:
            print(
                f"Teacher ID: {teacher.id}, Name: {teacher.first_name} {teacher.last_name}"
            )
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()


def update_teacher(id, first_name, last_name, email, phone=None):
    session = SessionLocal()
    try:
        teacher = session.query(Teacher).get(id)
        if teacher:
            teacher.first_name = first_name
            teacher.last_name = last_name
            teacher.email = email
            teacher.phone = phone
            session.commit()
            print(f"Teacher with ID {id} updated to {first_name} {last_name}.")
        else:
            print(f"Teacher with ID {id} not found.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()


def remove_teacher(id):
    session = SessionLocal()
    try:
        teacher = session.query(Teacher).get(id)
        if teacher:
            session.delete(teacher)
            session.commit()
            print(f"Teacher with ID {id} removed successfully.")
        else:
            print(f"Teacher with ID {id} not found.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()


# Створення групи
def create_group(name):
    session = SessionLocal()
    try:
        group = Group(name=name)
        session.add(group)
        session.commit()
        print(f"Group '{name}' created successfully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()


def list_groups():
    session = SessionLocal()
    try:
        groups = session.query(Group).all()
        if not groups:
            print("No groups found.")
        for group in groups:
            print(f"Group ID: {group.id}, Name: {group.name}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()


def update_group(id, name):
    session = SessionLocal()
    try:
        group = session.query(Group).get(id)
        if group:
            group.name = name
            session.commit()
            print(f"Group with ID {id} updated to {name}.")
        else:
            print(f"Group with ID {id} not found.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()


def remove_group(id):
    session = SessionLocal()
    try:
        group = session.query(Group).get(id)
        if group:
            session.delete(group)
            session.commit()
            print(f"Group with ID {id} removed successfully.")
        else:
            print(f"Group with ID {id} not found.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()


def main():
    while True:
        try:
            parser = argparse.ArgumentParser(description="Manage database operations")
            parser.add_argument(
                "-a",
                "--action",
                required=True,
                choices=["create", "list", "update", "remove"],
                help="Action to perform",
            )
            parser.add_argument(
                "-m",
                "--model",
                required=True,
                choices=["Teacher", "Group", "Student", "Subject", "Grade"],
                help="Model to operate on",
            )
            parser.add_argument("-n", "--name", help="Name for the model")
            parser.add_argument("-id", "--id", type=int, help="ID of the model")
            parser.add_argument(
                "-f", "--first_name", help="First name for teacher or student"
            )
            parser.add_argument(
                "-l", "--last_name", help="Last name for teacher or student"
            )
            parser.add_argument("-e", "--email", help="Email for teacher or student")
            parser.add_argument(
                "-p", "--phone", help="Phone number for teacher or student"
            )
            parser.add_argument(
                "-g", "--group_id", type=int, help="Group ID for student"
            )
            parser.add_argument(
                "-t", "--teacher_id", type=int, help="Teacher ID for subject"
            )
            parser.add_argument(
                "-sub", "--subject_id", type=int, help="Subject ID for grade"
            )
            parser.add_argument(
                "-gr", "--grade", type=int, help="Grade for the student"
            )

            args = parser.parse_args()

            # Використовуємо match для вибору дій
            match args.model:
                case "Teacher":
                    match args.action:
                        case "create":
                            if args.first_name and args.last_name and args.email:
                                create_teacher(
                                    args.first_name,
                                    args.last_name,
                                    args.email,
                                    args.phone,
                                )
                            else:
                                print(
                                    "Error: Teacher first_name, last_name, and email are required for creation"
                                )
                        case "list":
                            list_teachers()
                        case "update":
                            if (
                                args.id
                                and args.first_name
                                and args.last_name
                                and args.email
                            ):
                                update_teacher(
                                    args.id,
                                    args.first_name,
                                    args.last_name,
                                    args.email,
                                    args.phone,
                                )
                            else:
                                print(
                                    "Error: Teacher ID, first_name, last_name, and email are required for updating"
                                )
                        case "remove":
                            if args.id:
                                remove_teacher(args.id)
                            else:
                                print("Error: Teacher ID is required for removal")
                case "Group":
                    match args.action:
                        case "create":
                            if args.name:
                                create_group(args.name)
                            else:
                                print("Error: Group name is required for creation")
                        case "list":
                            list_groups()
                        case "update":
                            if args.id and args.name:
                                update_group(args.id, args.name)
                            else:
                                print(
                                    "Error: Group ID and name are required for updating"
                                )
                        case "remove":
                            if args.id:
                                remove_group(args.id)
                            else:
                                print("Error: Group ID is required for removal")
                case _:
                    print("Error: Unsupported model.")

            break  # After performing the operation, exit the loop

        except KeyboardInterrupt:
            print("\nProgram terminated by user (Ctrl+C). Exiting...")
            sys.exit(0)  # Exit the program on Ctrl+C
        except Exception as e:
            print(f"Unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
