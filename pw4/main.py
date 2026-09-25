import curses
from domains.models import Student, Course, SchoolManagement
from input import get_input
from output import show_message, show_students_list

def main(stdscr):
    system = SchoolManagement()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "=== PRACTICAL WORK 4: MODULARIZATION ===", curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(2, 0, "1. Add a Student")
        stdscr.addstr(3, 0, "2. Add a Course (with credits)")
        stdscr.addstr(4, 0, "3. Input Mark for a Student")
        stdscr.addstr(5, 0, "4. Show Students sorted by GPA")
        stdscr.addstr(6, 0, "5. Exit")
        
        choice = get_input(stdscr, "Select an option: ", 8, 0)

        if choice == '1':
            stdscr.clear()
            stdscr.addstr(0, 0, "[ ADD STUDENT ]", curses.color_pair(2))
            s_id = get_input(stdscr, "Enter Student ID: ", 2, 0)
            name = get_input(stdscr, "Enter Name: ", 3, 0)
            dob = get_input(stdscr, "Enter DoB: ", 4, 0)
            system.add_student(Student(s_id, name, dob))
            show_message(stdscr, 6, 0, "Student added! Press any key...", curses.color_pair(3))

        elif choice == '2':
            stdscr.clear()
            stdscr.addstr(0, 0, "[ ADD COURSE ]", curses.color_pair(2))
            c_id = get_input(stdscr, "Enter Course ID: ", 2, 0)
            name = get_input(stdscr, "Enter Course Name: ", 3, 0)
            try:
                credits = float(get_input(stdscr, "Enter Credits (e.g., 2, 3, 4): ", 4, 0))
                system.add_course(Course(c_id, name, credits))
                show_message(stdscr, 6, 0, "Course added! Press any key...", curses.color_pair(3))
            except ValueError:
                show_message(stdscr, 6, 0, "Invalid credit! Press any key...", curses.color_pair(3))

        elif choice == '3':
            stdscr.clear()
            stdscr.addstr(0, 0, "[ INPUT MARK ]", curses.color_pair(2))
            s_id = get_input(stdscr, "Enter Student ID: ", 2, 0)
            c_id = get_input(stdscr, "Enter Course ID: ", 3, 0)
            
            target_student = next((s for s in system.students if s.id == s_id), None)
            if target_student and c_id in system.courses:
                try:
                    mark = float(get_input(stdscr, "Enter Mark: ", 4, 0))
                    target_student.add_mark(c_id, mark)
                    show_message(stdscr, 6, 0, "Mark added and rounded down! Press any key...", curses.color_pair(3))
                except ValueError:
                    show_message(stdscr, 6, 0, "Invalid mark! Press any key...", curses.color_pair(3))
            else:
                show_message(stdscr, 6, 0, "Student or Course not found! Press any key...", curses.color_pair(3))

        elif choice == '4':
            show_students_list(stdscr, system, curses.color_pair(2), curses.color_pair(3))

        elif choice == '5':
            break

if __name__ == "__main__":
    curses.wrapper(main)