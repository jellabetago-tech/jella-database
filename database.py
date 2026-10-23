import os

import mysql.connector
from mysql.connector import Error

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "jella")


def get_connection():
    """Open a MySQL connection using environment settings or XAMPP defaults."""
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4",
        use_pure=True,
    )


def test_connection():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT 1 FROM student_courses LIMIT 1")
            cursor.fetchone()
            return True, f"Connected to MySQL database '{DB_NAME}'."
        return False, "Could not connect to MySQL."
    except Error as error:
        return False, str(error)
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def get_all_students():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT student_number, full_name, email, course, year_level, section,
                   age, civil_status, address
            FROM student_courses
            ORDER BY student_number
            """
        )
        return cursor.fetchall()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def get_student_by_number(student_number):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT student_number, full_name, email, course, year_level, section,
                   age, civil_status, address
            FROM student_courses
            WHERE student_number = %s
            """,
            (student_number,),
        )
        return cursor.fetchone()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def insert_student(student):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO student_courses
                (student_number, full_name, email, course, year_level, section,
                 age, civil_status, address)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                student["student_number"],
                student["full_name"],
                student["email"],
                student["course"],
                student["year_level"],
                student["section"],
                student["age"],
                student["civil_status"],
                student["address"],
            ),
        )
        connection.commit()
        return cursor.lastrowid
    except Error:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def update_student(student_number, student):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            UPDATE student_courses
            SET full_name = %s, email = %s, course = %s,
                year_level = %s, section = %s, age = %s,
                civil_status = %s, address = %s
            WHERE student_number = %s
            """,
            (
                student["full_name"],
                student["email"],
                student["course"],
                student["year_level"],
                student["section"],
                student["age"],
                student["civil_status"],
                student["address"],
                student_number,
            ),
        )
        connection.commit()
        return cursor.rowcount > 0
    except Error:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def delete_student(student_number):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM student_courses WHERE student_number = %s",
            (student_number,),
        )
        connection.commit()
        return cursor.rowcount > 0
    except Error:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def delete_all_students():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM student_courses")
        connection.commit()
        return cursor.rowcount
    except Error:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()
