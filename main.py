import os
import csv
import numpy as np
import matplotlib.pyplot as plt

students = np.empty((0, 4), dtype=object) # Initialize the students ndarray

def display_menu():
    """Show banner and menu options"""
    print("-" * 33)
    print("*** Student Management System ***")
    print("-" * 33)
    print("""Select option below
    1. Add a Student
    2. Search Student
    3. Display Students By Grade
    4. Delete a Student
    5. Load Student Records
    6. Save Student Records
    7. Display Grade Distribution
    8. Display Marks Distribution
    0. Quit""")
    print("-" * 33)

def is_empty_input(input_data):
    """Check for empty user input."""
    return True if input_data == '' else False

def add_student(student_number, student_surname, student_given_name, unit_mark):
    """Add student record to the system."""
    student = np.array([[student_number, student_surname, student_given_name, unit_mark]])
    global students
    students = np.concatenate((students, student), axis=0)

def search_students(search_key):
    """Search student(s) by number or partial name match."""
    search_key = search_key.lower()
    student_surnames = np.char.lower(students[:, 1].astype(str))
    student_given_names = np.char.lower(students[:, 2].astype(str))
    
    matches = np.any([
        np.char.lower(students[:, 0].astype(str)) == search_key,
        np.char.find(student_surnames, search_key) >= 0,
        np.char.find(student_given_names, search_key) >= 0
    ], axis=0)
    
    search_results = students[matches]
    return search_results.tolist()


def student_exists(student_number):
    student_numbers = students[:, 0].astype(str)
    return str(student_number) in student_numbers

def calculate_student_grade(mark):
    if mark >= 80:
        return 'HD'
    elif mark >= 70:
        return 'D'
    elif mark >= 60:
        return 'C'
    elif mark >= 50:
        return 'P'
    else:
        return 'N'

def display_students_by_grade(grade):
    """Display the names of students who achieved the specified grade for the unit."""
    student_marks = students[:, 3].astype(float)
    student_grades = np.vectorize(calculate_student_grade)(student_marks)
    matches = student_grades == grade
    results = students[matches]
    return results.tolist()

def delete_student(student_number):
    """Remove a student record from the system."""
    global students
    student_numbers = students[:, 0].astype(int)
    matches = student_numbers != student_number
    students = students[matches]
    return np.sum(matches) < len(student_numbers)

def file_exists(file_path):
    return True if os.path.exists(file_path) else False

def load_student_records(file_path):
    """
    Load student records from a csv file to existing student records.
    """
    students_loaded = 0  # To count the number of student records loaded
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header row
            for row in reader:
                student_number = row[0]
                student_surname = row[1]
                student_given_name = row[2]
                unit_mark = row[3]
                # If student exists, student_number and mark is empty, skip the record
                if student_number == '' or student_exists(student_number) or unit_mark is None or unit_mark == '':
                    continue
                else:
                    # Add student record to the system
                    add_student(student_number, student_surname, student_given_name, float(unit_mark))
                    students_loaded += 1
            print(f"\nLoaded {students_loaded} student(s) from file {file_path}\n")
    except FileNotFoundError:
        print(f"\nError: could not load student data. File '{file_path}' does not exist\n")
    except Exception as e:
        print(f"Error: {e}")

def save_student_records(file_path):
    try:
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['student_number', 'student_surname', 'student_given_name', 'unit_mark'])
            writer.writerows(students)
        print(f"\nStudent records saved successfully to file '{file_path}'")
    except Exception as e:
        print(f"\nError: {e}")

def calculate_grade_counts():
    grade_counts = {
        'HD': 0,
        'D': 0,
        'C': 0,
        'P': 0, 
        'N': 0
    }

    for student in students:
        mark = float(student[3])
        grade = calculate_student_grade(mark)
        if grade in grade_counts:
            grade_counts[grade] += 1

    return grade_counts

def display_grade_distribution():
    grade_counts = calculate_grade_counts()
    grades = list(grade_counts.keys())
    counts = list(grade_counts.values())

    # Plot the pie chart
    plt.pie(counts, labels=grades, autopct='%1.1f%%')

    # Show title
    plt.title("Students Grade Distribution")

    # Displaying the pie chart
    plt.show()

def calculate_mark_counts():
    marks_counts = {
        '0-29': 0,
        '30-39': 0,
        '40-49': 0, 
        '50-59': 0,
        '60-69': 0, 
        '70-79': 0,
        '80-89': 0, 
        '90-100': 0
    }

    for student in students:
        mark = float(student[3])
        if mark < 30:
            marks_counts['0-29'] += 1
        elif mark < 40:
            marks_counts['30-39'] += 1
        elif mark < 50:
            marks_counts['40-49'] += 1
        elif mark < 60:
            marks_counts['50-59'] += 1
        elif mark < 70:
            marks_counts['60-69'] += 1
        elif mark < 80:
            marks_counts['70-79'] += 1
        elif mark < 90:
            marks_counts['80-89'] += 1
        else:
            marks_counts['90-100'] += 1

    return marks_counts

def display_marks_distribution():
    mark_counts = calculate_mark_counts()
    
    # Calculate the total number of students
    total_students = sum(mark_counts.values()) # len(students)

    # Calculate the percentage of students in each mark range
    mark_ranges = ['0-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '90-100']
    percentages = [(mark_counts.get(mark, 0) / total_students) * 100 for mark in mark_ranges]

    # Add percentage labels on each bar
    for i in range(len(mark_ranges)):
        plt.text(i, percentages[i], f'{percentages[i]:.1f}%', ha='center', va='bottom')

    # Plot the bar chart
    plt.bar(mark_ranges, percentages)
    plt.title('Studens Marks Distribution')
    plt.xlabel('Mark Ranges')
    plt.ylabel('Percentage of Students')

    # Show the chart
    plt.show()

def main():
    os.system("clear")  # Used for clearing screen

    # Load initial student data from the given file
    file_name = "students.csv"
    load_student_records(file_name)

    while True:
        display_menu()
        #print(students)
        choice = input("Enter your choice: ")
        if choice == "1":
            print("Enter student details below.")
            
            # Get student number
            while True:
                try:
                    student_number = int(input("Student Number: "))
                    if student_number <= 0:
                        print("\nError: invalid student number. Try again!\n")
                    elif student_exists(student_number):
                        print(f"\nStudent number '{student_number}' already exists. Try again.\n")
                    else:
                        break
                except ValueError:
                    print("\nError: invalid student number. Try again!\n") 
            
            # Get student surname
            student_surname = input("Student Surname: ")
            
            # Get student given name
            while True:
                student_given_name = input("Student Given Name: ")
                if is_empty_input(student_given_name):
                    print("\nError: given name cannot be empty. Try again.\n")
                else:
                    break
            
            # Get unit mark
            while True:
                try:
                    unit_mark = float(input("Unit Mark: "))
                    if unit_mark >= 0:
                        break
                    else:
                        print("\nError: invalid mark. Try again.\n")
                except ValueError:
                    print("\nError: invalid mark. Try again.\n")
            
            add_student(student_number, student_surname, student_given_name, unit_mark)
            print("\nStudent record added to the system successfully.")
            input("\nPress enter to continue...")
        elif choice == "2":
            while True:
                search_key = input("Enter student number or name: ")
                
                if is_empty_input(search_key):
                    print("\nError: search keyword cannot be blank. Try again!\n")
                else:
                    break
            search_results = search_students(search_key)
            num_results = len(search_results)
            if num_results > 0:
                print(f"\n{num_results} result(s) found.\n")
                print("{:<20} {:<30} {:<10}".format("Student Number", "Student Name", "Unit Mark"))
                print("-" * 65)
                for result in search_results:
                    print("{:<20} {:<30} {:<10}".format(
                        result[0],
                        result[2] + " " + result[1],
                        result[3]
                    ))
                print("-" * 65)
            else:
                print("\nNo students found with matching keyword.")
            input("\nPress enter to continue...")
        elif choice == "3":
            grades_list = ['HD', 'D', 'C', 'P', 'N']
            grade = input("Enter unit grade (HD, D, C, P, N): ").upper()
            
            if grade not in grades_list:
                print(f"\nInvalid grade: {grade}")
            else:
                results = display_students_by_grade(grade)
                num_results = len(results)
                if num_results > 0:
                    print(f"\n{num_results} student(s) achieved a grade of '{grade}'.\n")
                    print("Student Name")
                    print("-" * 25)
                    for student in results:
                        print(f'{student[2]} {student[1]}')
                    print("-" * 25)
                else:
                    print("\nNo student record found.")
            input("\nPress enter to continue...")
        elif choice == "4":
            while True:
                try:
                    student_number = int(input("Enter Student Number: "))
                    break
                except ValueError:
                    print("\nError: invalid student number. Try again!\n")
                    
            if delete_student(student_number):
                print("\nStudent record deleted successfully.")
            else:
                print(f"\nStudent record with number '{student_number}' does not exist.")
            input("\nPress enter to continue...")
        elif choice == "5":
            file_path = input("Enter file path to load student record: ")
            load_student_records(file_path)
            input("\nPress enter to continue...")
        elif choice == "6":
            while True:
                file_path = input("Enter the file path to save student records: ")
                if file_exists(file_path):
                    print("\nFile already exists.\n")
                    response = input("Choose an option: (1) Change filename, (2) Overwrite, (3) Cancel: ").lower()
                    if response == "1":  
                        # Change filename.
                        continue
                    elif response == "2":  
                        # Overwrite existing file
                        save_student_records(file_path)
                        break
                    else:  
                        # Cancel operation if response is 3 or invalid
                        print("\nCancelling Operation!")
                        break
                else:
                    save_student_records(file_path)
                    break
            input("\nPress enter to continue...")
        elif choice == "7":
            display_grade_distribution()
        elif choice == "8":
            display_marks_distribution()
        elif choice == "0":
            print("\nExiting program...\n")
            break
        else:
            input("\nInvalid Choice! Try Again.")

if __name__ == "__main__":
    main()