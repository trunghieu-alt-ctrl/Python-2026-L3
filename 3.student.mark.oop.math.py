import math
import numpy as np
import curses

class Student:
    def __init__(self, student_id, name, dob):
        self.id = student_id
        self.name = name
        self.dob = dob
        self.marks = {} 
        self.gpa = 0.0

    def add_mark(self, course_id, mark):
        # Dùng math.floor() để làm tròn xuống 1 chữ số thập phân
        self.marks[course_id] = math.floor(mark * 10) / 10.0

    def calculate_gpa(self, courses_dict):
        # Tính GPA bằng mảng numpy theo trọng số tín chỉ
        if not self.marks:
            self.gpa = 0.0
            return
        
        marks_list = []
        credits_list = []
        for c_id, mark in self.marks.items():
            if c_id in courses_dict:
                marks_list.append(mark)
                credits_list.append(courses_dict[c_id].credits)
                
        if credits_list:
            marks_arr = np.array(marks_list)
            credits_arr = np.array(credits_list)
            self.gpa = np.average(marks_arr, weights=credits_arr)
        else:
            self.gpa = 0.0

class Course:
    def __init__(self, course_id, name, credits):
        self.id = course_id
        self.name = name
        self.credits = credits

class SchoolManagement:
    def __init__(self):
        self.students = []
        self.courses = {}

    def add_student(self, std):
        self.students.append(std)

    def add_course(self, course):
        self.courses[course.id] = course

    def sort_by_gpa(self):
        for s in self.students:
            s.calculate_gpa(self.courses)
        # Sắp xếp danh sách sinh viên theo GPA giảm dần
        self.students.sort(key=lambda s: s.gpa, reverse=True)

# --- PHẦN GIAO DIỆN CURSES ---
def get_input(stdscr, prompt, y, x):
    stdscr.addstr(y, x, prompt)
    curses.echo()
    result = stdscr.getstr(y, x + len(prompt), 50).decode('utf-8')
    curses.noecho()
    return result

def main(stdscr):
    system = SchoolManagement()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "=== PRACTICAL WORK 3: STUDENT MARK (OOP + MATH + NUMPY + CURSES) ===", curses.color_pair(1) | curses.A_BOLD)
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
            stdscr.addstr(6, 0, "Student added! Press any key...", curses.color_pair(3))
            stdscr.getch()

        elif choice == '2':
            stdscr.clear()
            stdscr.addstr(0, 0, "[ ADD COURSE ]", curses.color_pair(2))
            c_id = get_input(stdscr, "Enter Course ID: ", 2, 0)
            name = get_input(stdscr, "Enter Course Name: ", 3, 0)
            try:
                credits = float(get_input(stdscr, "Enter Credits (e.g., 2, 3, 4): ", 4, 0))
                system.add_course(Course(c_id, name, credits))
                stdscr.addstr(6, 0, "Course added! Press any key...", curses.color_pair(3))
            except ValueError:
                stdscr.addstr(6, 0, "Invalid credit! Press any key...", curses.color_pair(3))
            stdscr.getch()

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
                    stdscr.addstr(6, 0, "Mark added and rounded down! Press any key...", curses.color_pair(3))
                except ValueError:
                    stdscr.addstr(6, 0, "Invalid mark! Press any key...", curses.color_pair(3))
            else:
                stdscr.addstr(6, 0, "Student or Course not found! Press any key...", curses.color_pair(3))
            stdscr.getch()

        elif choice == '4':
            stdscr.clear()
            stdscr.addstr(0, 0, "[ STUDENTS SORTED BY GPA DESCENDING ]", curses.color_pair(2))
            system.sort_by_gpa()
            
            row = 2
            for s in system.students:
                stdscr.addstr(row, 0, f"ID: {s.id} | Name: {s.name} | GPA: {s.gpa:.1f}")
                row += 1
                
            stdscr.addstr(row + 2, 0, "Press any key to return...", curses.color_pair(3))
            stdscr.getch()

        elif choice == '5':
            break

if __name__ == "__main__":
    curses.wrapper(main)