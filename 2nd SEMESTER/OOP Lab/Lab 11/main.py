from employee import Manager, Worker
from file_operations import add_employee_to_file, list_all_employees, modify_employee_record, remove_employee_from_file # type: ignore

def display_main_menu():
    while True:
        print("\nEmployee Management System")
        print("1. Add New Employee")
        print("2. Display All Employees")
        print("3. Modify Employee Info")
        print("4. Remove Employee")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            emp_type = input("Enter Employee Type (Manager/Worker): ").strip().lower()
            name = input("Enter Name: ")
            age = int(input("Enter Age: "))
            salary = int(input("Enter Salary: "))

            if emp_type == "manager":
                department = input("Enter Department: ")
                manager = Manager(name, age, salary, department)
                add_employee_to_file(manager)
            elif emp_type == "worker":
                hours_worked = int(input("Enter Hours Worked: "))
                worker = Worker(name, age, salary, hours_worked)
                add_employee_to_file(worker)
            else:
                print("Invalid employee type.")

        elif choice == '2':
            list_all_employees()

        elif choice == '3':
            name = input("Enter the employee name to modify: ")
            updated_info = []
            updated_info.append(input("Enter new Name: "))
            updated_info.append(int(input("Enter new Age: ")))
            updated_info.append(float(input("Enter new Salary: ")))
            updated_info.append(input("Enter new Department or N/A: "))
            updated_info.append(int(input("Enter new Hours Worked or N/A: ")))
            modify_employee_record(name, updated_info)

        elif choice == '4':
            name = input("Enter the employee name to remove: ")
            remove_employee_from_file(name)

        elif choice == '5':
            print("Exiting the system...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    display_main_menu()
