import curses

class curses_cli:
    def setup(stdscr):
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(1)

    def draw_ui(stdscr,pdus):
        stdscr.border(0)
        stdscr.addstr(2, 5, "OSL PDU management!")
        current_col = 5
        stdscr.refresh()
        for pdu in pdus:
            stdscr.addstr( current_col, 5, pdu)
            current_col += 3 + len(pdu)
        stdscr.getch()

    def cleanup(stdscr):
        curses.nocbreak()
        stdscr.keypad(0)
        curses.echo()
        curses.endwin()

"""
if __name__ == '__main__':
    stdscr = curses.initscr()
    start(stdscr)
    pdus = ('pdu-b210-dell03.osuosl.oob', 'pdu-b210-dell13.osuosl.oob','pdu-b210-dell03.osuosl.oob', 'pdu-b210-dell13.osuosl.oob')
    draw_ui(stdscr, pdus)
    stop(stdscr)
"""
