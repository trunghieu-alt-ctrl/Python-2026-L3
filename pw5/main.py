import curses
import os
import zipfile
from domains.models import Student, Course, SchoolManagement
from input import get_input
from output import show_message, show_students_list

def load_data(system):
    # Check if students.dat exists upon starting[cite: 3]
    if os.path.exists("students.dat"):
        # Decompress and load data from it[cite: 3]
        with zipfile.ZipFile("students.dat", 'r') as zf:
            zf.extractall()

    if os.path.exists("students.txt"):
        with open("students.txt", "r") as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) == 3:
                    system.students.append(Student(parts[0], parts[1], parts[2]))

    if os.path.exists("courses.txt"):
        with open("courses.txt", "r") as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) == 3:
                    system.courses[parts[0]] = Course(parts[0], parts[1], float(parts[2]))

    if os.path.exists("marks.txt"):
        with open("marks.txt", "r") as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) == 3:
                    target = next((s for s in system.students if s.id == parts[1]), None)
                    if target:
                        target.marks[parts[0]] = float(parts[2])

def compress_data():
    # Compress all files into students.dat before closing using zip deflation[cite: 3]
    files_to_compress = ["students.txt", "courses.txt", "marks.txt"]
    with zipfile.ZipFile("students.dat", 'w', zipfile.ZIP_DEFLATED) as zf:
        for file in files_to_compress:
            if os.path.exists(file):
                zf.write(file)

def main(stdscr):
    system = SchoolManagement()
    load_data(system)
    
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "=== PRACTICAL WORK 5: PERSISTENT INFO ===", curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(2, 0, "1. Add a Student")
        stdscr.addstr(3, 0, "2. Add a Course")
        stdscr.addstr(4, 0, "3. Input Mark")
        stdscr.addstr(5, 0, "4. Show Students sorted by GPA")
        stdscr.addstr(6, 0, "5. Exit and Compress")
        
        choice = get_input(stdscr, "Select an option: ", 8, 0)

        if choice == '1':
            stdscr.clear()
            s_id = get_input(stdscr, "Enter Student ID: ", 2, 0)
            name = get_input(stdscr, "Enter Name: ", 3, 0)
            dob = get_input(stdscr, "Enter DoB: ", 4, 0)
            system.students.append(Student(s_id, name, dob))
            
            # Write student info to students.txt after finishing input[cite: 2]
            with open("students.txt", "a") as f:
                f.write(f"{s_id},{name},{dob}\n")
            show_message(stdscr, 6, 0, "Student added & saved! Press any key...", curses.color_pair(3))

        elif choice == '2':
            stdscr.clear()
            c_id = get_input(stdscr, "Enter Course ID: ", 2, 0)
            name = get_input(stdscr, "Enter Course Name: ", 3, 0)
            try:
                credits = float(get_input(stdscr, "Enter Credits: ", 4, 0))
                system.courses[c_id] = Course(c_id, name, credits)
                
                # Write course info to courses.txt after finishing input[cite: 2]
                with open("courses.txt", "a") as f:
                    f.write(f"{c_id},{name},{credits}\n")
                show_message(stdscr, 6, 0, "Course added & saved! Press any key...", curses.color_pair(3))
            except ValueError:
                pass

        elif choice == '3':
            stdscr.clear()
            s_id = get_input(stdscr, "Enter Student ID: ", 2, 0)
            c_id = get_input(stdscr, "Enter Course ID: ", 3, 0)
            
            target_student = next((s for s in system.students if s.id == s_id), None)
            if target_student and c_id in system.courses:
                try:
                    mark = float(get_input(stdscr, "Enter Mark: ", 4, 0))
                    target_student.add_mark(c_id, mark)
                    
                    # Write marks to marks.txt after finishing input[cite: 2]
                    with open("marks.txt", "a") as f:
                        f.write(f"{c_id},{s_id},{mark}\n")
                    show_message(stdscr, 6, 0, "Mark added & saved! Press any key...", curses.color_pair(3))
                except ValueError:
                    pass

        elif choice == '4':
            show_students_list(stdscr, system, curses.color_pair(2), curses.color_pair(3))

        elif choice == '5':
            compress_data()
            break

if __name__ == "__main__":
    curses.wrapper(main)
