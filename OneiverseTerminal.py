import curses
import time
import random

def main(stdscr):
    curses.curs_set(0)  # Hide the cursor
    stdscr.clear()

    # Get the size of the window
    height, width = stdscr.getmaxyx()

    # Determine the starting point for the center
    text = "Loading Terminal"
    start_row = height // 2
    start_col = (width - len(text)) // 2

    # Print "Loading Terminal" at the center of the screen
    stdscr.addstr(start_row, start_col, text)

    # Determine the starting point for the loading bar
    loading_bar_length = 10
    start_col_bar = (width - loading_bar_length) // 2

    # Display an empty loading bar
    stdscr.addstr(start_row + 1, start_col_bar, "[" + " " * loading_bar_length + "]")
    stdscr.refresh()

    # Fill the loading bar
    for i in range(loading_bar_length):
        # Wait for 1 to 3 seconds
        time.sleep(random.randint(1, 3))
        
        # Replace the correct number of spaces with segments
        stdscr.addstr(start_row + 1, start_col_bar + 1 + i, "#")
        stdscr.refresh()

    stdscr.getch()

curses.wrapper(main)