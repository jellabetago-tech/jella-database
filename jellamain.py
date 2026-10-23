import database
import student


def main():
    connected, message = database.test_connection()
    if not connected:
        print(f"Could not connect to XAMPP MySQL: {message}")
        print("Make sure MySQL is running and schema.sql has been imported.")
        return
    print(message)

    print("\n=== STUDENT COURSE SYSTEM ===")
    while True:
        print("\n[1] Add a student")
        print("[2] View all students")
        print("[3] Search for a student")
        print("[4] Edit a student")
        print("[5] Delete a student")
        print("[6] Delete all students")
        print("[0] Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            student.add_student()
        elif choice == "2":
            student.show_students()
        elif choice == "3":
            student.search_student()
        elif choice == "4":
            student.edit_student()
        elif choice == "5":
            student.remove_student()
        elif choice == "6":
            student.remove_all_students()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Select 1, 2, 3, 4, 5, 6, or 0.")


if __name__ == "__main__":
    main()
