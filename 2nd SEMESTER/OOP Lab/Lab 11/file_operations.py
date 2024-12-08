# file_operations.py
import csv
from employee import Manager, Worker

def add_employee_to_file(employee, filename="employees.csv"):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if isinstance(employee, Manager):
            writer.writerow([employee.get_name(), employee.get_age(), employee.get_salary(), employee.get_department(), "N/A"])
        elif isinstance(employee, Worker):
            writer.writerow([employee.get_name(), employee.get_age(), employee.get_salary(), "N/A", employee.get_hours_worked()])


def list_all_employees(filename="employees.csv"):
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)


def modify_employee_record(name, updated_info, filename="employees.csv"):
    rows = []
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        for row in rows:
            if row[0] == name:
                writer.writerow(updated_info)
            else:
                writer.writerow(row)


def remove_employee_from_file(name, filename="employees.csv"):
    rows = []
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        for row in rows:
            if row[0] != name:
                writer.writerow(row)
