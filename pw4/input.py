import curses

def get_input(stdscr, prompt, y, x):
    stdscr.addstr(y, x, prompt)
    curses.echo()
    result = stdscr.getstr(y, x + len(prompt), 50).decode('utf-8')
    curses.noecho()
    return result