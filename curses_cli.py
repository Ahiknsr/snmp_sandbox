import curses

class curses_cli:
    def setup(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(1)

    def draw_ui(self, pdus):
        self.stdscr.border(0)
        self.stdscr.addstr(2, 5, "OSL PDU management!")
        current_col = 5
        self.stdscr.refresh()
        for pdu in pdus:
            self.stdscr.addstr( current_col, 5, pdu)
            current_col += 3 + len(pdu)
        self.stdscr.getch()

    def cleanup(self):
        curses.nocbreak()
        self.stdscr.keypad(0)
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
