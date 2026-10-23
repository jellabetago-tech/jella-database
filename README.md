# Student Course System

A Python command-line application for managing student course records with MySQL/MariaDB in XAMPP.

## Files

| File | Purpose |
| --- | --- |
| `schema.sql` | Creates the `jonard` database and `student_courses` table. |
| `requirements.txt` | Lists the Python packages required by the project. |
| `database.py` | Provides the MySQL connection and database queries. |
| `student.py` | Handles student input, validation, and CRUD operations. |
| `jellamain.py` | Main application entry point. |
| `mainjud_ni.py` | Compatibility entry point for the command shown below. |

## Requirements and setup

1. Start **MySQL** in the XAMPP Control Panel.
2. Open `http://localhost/phpmyadmin`, select **Import**, and import `schema.sql`. You can also run the SQL file using the MySQL command line.
3. Open a terminal in the project folder and install the package:

   ```powershell
   python -m pip install -r requirements.txt
   ```

4. Start the application:

   ```powershell
   python jellamain.py
   ```

   You can also run `python mainjud_ni.py`.

On startup, the application tests the connection and checks whether the `student_courses` table is available.

## MySQL settings

The default XAMPP settings are `localhost`, port `3306`, user `root`, no password, and database `jonard`. To use different settings, set environment variables before starting the application. For example, in PowerShell:

```powershell
$env:DB_HOST = "localhost"
$env:DB_PORT = "3306"
$env:DB_USER = "root"
$env:DB_PASSWORD = "your-password"
$env:DB_NAME = "jonard"
python jellamain.py
```

If you change `DB_NAME`, update the database name in `schema.sql` before importing it.

## Menu (CRUD)

- `1` — Add a student (Create)
- `2` — View all student records (Read)
- `3` — Search by student number (Read)
- `4` — Edit a record (Update). Leave a field blank to keep its current value.
- `5` — Delete a record (Delete). Confirmation is required.
- `6` — Delete all student records. Confirmation is required.
- `0` — Exit

The student number must be unique. Each record contains a student number, full name, email, course/program, year level, section, age, civil status (Single or Not Single), and address.

If the `student_courses` table already exists, run this SQL in phpMyAdmin's **SQL** tab to add the new columns:

```sql
USE jonard;
ALTER TABLE student_courses
    ADD COLUMN age TINYINT UNSIGNED NOT NULL DEFAULT 0 AFTER section,
    ADD COLUMN civil_status VARCHAR(20) NOT NULL DEFAULT 'Single' AFTER age,
    ADD COLUMN address VARCHAR(255) NOT NULL DEFAULT '' AFTER civil_status;
```
