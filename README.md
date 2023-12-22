# Snake Game

This ASCII terminal-based snake game was written using built-in Python libraries including [curses](https://docs.python.org/3/howto/curses.html) for the terminal display and input handling. The Snake object can be constructed with custom length, segment configuration, and display characters. The World object can be constructed with custom starting snake position, height, width, and food display character, but all of these have defaults.

## Current Bugs

- When the game is running, a keypress will skip the remainder of the time interval, leading to choppy gameplay, especially when there are lots of turns. I plan to address this using the `timeit.timeit()` function to measure how long was taken to press the key, and then using `time.wait()` to wait out the remainder of the interval.

- I have code written to print 'Game Over' along with the final snake length and food eaten, upon death, but as of right now, it is failing to print.