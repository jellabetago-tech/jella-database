import mysql.connector

import database


def ask_required(prompt, max_length):
    while True:
        value = input(prompt).strip()
        if not value:
            print("This field is required.")
        elif len(value) > max_length:
            print(f"Do not exceed {max_length} characters.")
        else:
            return value


def is_valid_email(email):
    email_name, separator, email_domain = email.partition("@")
    return bool(separator and email_name and "." in email_domain)


def ask_year_level(prompt="Year level (1-4): "):
    while True:
        year_level = input(prompt).strip()
        if year_level in {"1", "2", "3", "4"}:
            return int(year_level)
        print("Choose a year level from 1 to 4.")


def ask_age(prompt="Age: "):
    while True:
        age = input(prompt).strip()
        if age.isdigit() and 1 <= int(age) <= 120:
            return int(age)
        print("Enter a valid age (1-120).")


def ask_civil_status(prompt="Are you single? (y/n): "):
    while True:
        answer = input(prompt).strip().lower()
        if answer in {"y", "yes"}:
            return "Single"
        if answer in {"n", "no"}:
            return "Not Single"
        print("Answer yes (y) or no (n).")


def get_student_details():
    student = {
        "student_number": ask_required("Student number: ", 30),
        "full_name": ask_required("Full name: ", 150),
        "email": ask_required("Email: ", 120),
        "course": ask_required("Course/program: ", 120),
    }

    if not is_valid_email(student["email"]):
        print("Invalid email address.")
        return None

    student["year_level"] = ask_year_level()
    student["section"] = ask_required("Section: ", 30)
    student["age"] = ask_age()
    student["civil_status"] = ask_civil_status()
    student["address"] = ask_required("Address: ", 255)
    return student


def display_student(student):
    civil_status = {
        "Hindi Single": "Not Single",
    }.get(student["civil_status"], student["civil_status"])
    print(
        f"\nStudent number: {student['student_number']}\n"
        f"Full name:      {student['full_name']}\n"
        f"Email:          {student['email']}\n"
        f"Course:         {student['course']}\n"
        f"Year level:     {student['year_level']}\n"
        f"Section:        {student['section']}\n"
        f"Age:            {student['age']}\n"
        f"Civil status:   {civil_status}\n"
        f"Address:        {student['address']}"
    )


def add_student():
    print("\n--- Add a student ---")
    details = get_student_details()
    if details is None:
        return

    try:
        student_id = database.insert_student(details)
        print(f"Student record saved successfully. ID: {student_id}")
    except mysql.connector.IntegrityError:
        print("A record with that student number already exists.")
    except mysql.connector.Error as error:
        print(f"Could not save the record: {error}")


def show_students():
    try:
        students = database.get_all_students()
    except mysql.connector.Error as error:
        print(f"Could not retrieve student records: {error}")
        return

    print("\n--- Enrolled students ---")
    if not students:
        print("There are no student records yet.")
        return

    for student in students:
        display_student(student)


def search_student():
    student_number = ask_required("Student number to search for: ", 30)
    try:
        student = database.get_student_by_number(student_number)
    except mysql.connector.Error as error:
        print(f"Could not search for the record: {error}")
        return

    if student is None:
        print("No student has that student number.")
        return

    display_student(student)


def edit_student():
    student_number = ask_required("Student number to edit: ", 30)
    try:
        current = database.get_student_by_number(student_number)
    except mysql.connector.Error as error:
        print(f"Could not retrieve the record: {error}")
        return

    if current is None:
        print("No student has that student number.")
        return

    print("\nLeave a field blank to keep its current value.")
    updated = {}
    for field, label, limit in (
        ("full_name", "Full name", 150),
        ("email", "Email", 120),
        ("course", "Course/program", 120),
        ("section", "Section", 30),
        ("address", "Address", 255),
    ):
        value = input(f"{label} [{current[field]}]: ").strip()
        if len(value) > limit:
            print(f"Do not exceed {limit} characters. No changes were made.")
            return
        updated[field] = value or current[field]

    if not is_valid_email(updated["email"]):
        print("Invalid email address. No changes were made.")
        return

    year_level = input(f"Year level (1-4) [{current['year_level']}]: ").strip()
    if year_level:
        if year_level not in {"1", "2", "3", "4"}:
            print("Choose a year level from 1 to 4. No changes were made.")
            return
        updated["year_level"] = int(year_level)
    else:
        updated["year_level"] = current["year_level"]

    age = input(f"Age [{current['age']}]: ").strip()
    if age:
        if not age.isdigit() or not 1 <= int(age) <= 120:
            print("Enter a valid age (1-120). No changes were made.")
            return
        updated["age"] = int(age)
    else:
        updated["age"] = current["age"]

    current_civil_status = {
        "Hindi Single": "Not Single",
    }.get(current["civil_status"], current["civil_status"])
    civil_status = input(
        f"Are you single? (y/n) [{current_civil_status}]: "
    ).strip().lower()
    if civil_status:
        if civil_status in {"y", "yes"}:
            updated["civil_status"] = "Single"
        elif civil_status in {"n", "no"}:
            updated["civil_status"] = "Not Single"
        else:
            print("Answer yes (y) or no (n). No changes were made.")
            return
    else:
        updated["civil_status"] = current["civil_status"]

    try:
        updated_record = database.update_student(student_number, updated)
    except mysql.connector.Error as error:
        print(f"Could not update the record: {error}")
        return

    if updated_record:
        print("Student record updated successfully.")
    else:
        print("No student record was changed.")


def remove_student():
    student_number = ask_required("Student number to delete: ", 30)
    try:
        current = database.get_student_by_number(student_number)
    except mysql.connector.Error as error:
        print(f"Could not retrieve the record: {error}")
        return

    if current is None:
        print("No student has that student number.")
        return

    display_student(current)
    confirmation = input("Are you sure you want to delete this record? (y/n): ").strip().lower()
    if confirmation not in {"y", "yes"}:
        print("Deletion canceled.")
        return

    try:
        deleted = database.delete_student(student_number)
    except mysql.connector.Error as error:
        print(f"Could not delete the record: {error}")
        return

    if deleted:
        print("Student record deleted successfully.")
    else:
        print("There is no student record to delete.")


def remove_all_students():
    confirmation = input(
        "Are you sure you want to delete ALL student records? (y/n): "
    ).strip().lower()
    if confirmation not in {"y", "yes"}:
        print("Deletion of all records canceled.")
        return

    try:
        deleted_count = database.delete_all_students()
    except mysql.connector.Error as error:
        print(f"Could not delete student records: {error}")
        return

    if deleted_count:
        print(f"Deleted {deleted_count} student records successfully.")
    else:
        print("There are no student records to delete.")
