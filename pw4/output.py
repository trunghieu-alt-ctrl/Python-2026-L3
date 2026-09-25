import curses

def show_message(stdscr, y, x, msg, color_pair):
    stdscr.addstr(y, x, msg, color_pair)
    stdscr.getch()

def show_students_list(stdscr, system, color_pair_header, color_pair_prompt):
    stdscr.clear()
    stdscr.addstr(0, 0, "[ STUDENTS SORTED BY GPA DESCENDING ]", color_pair_header)
    system.sort_by_gpa()
    
    row = 2
    for s in system.students:
        stdscr.addstr(row, 0, f"ID: {s.id} | Name: {s.name} | GPA: {s.gpa:.1f}")
        row += 1
        
    stdscr.addstr(row + 2, 0, "Press any key to return...", color_pair_prompt)
    stdscr.getch()