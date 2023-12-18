import random
import time

class Snake:
    """
    A snake who slithers through the world, with directed segments.

    ...

    Attributes
    ----------
    length : int
        total length of the snake
    chars : tuple[str]
        characters to represent the
        (head, horizontal segments, vertical segments, tail)
    segments : list[list[int, str]]
        a list of each segment's distance from the head and current direction
    
    Methods
    -------
    turn(direction):
        Changes the heading of the snake.
    grow(length : int = 1):
        Adds legnth to the snake's tail.
    """
    
    def __init__(
            self, length, segments: list[list[int, str]] = [[0, 'E']],
            chars: tuple[str] = ('X','-','|','x')
        ):
        """
        Constructs all of the necessary attributes for the snake.
        
        Parameters
        ----------
        length : int
            the starting length of the snake
        segments : list[list[int, str]], optional
            the starting list of each starting segment's distance from the
            head and current direction (default is one eastbound segment
            [[0, 'E']])
        chars : tuple[str]
            characters to represent the
            (head, horizontal segments, vertical segments, tail) (default is
            ('X','-','|','x'))
        """
        self.length = length
        self.chars = chars
        # create a list of semgments, each with a distance from the snake's
        # head and a direction; ordered starting with the head
        for seg in segments:
            if seg[0] >= self.length - 1:
                raise Exception("Snake segments must begin before the tail")
        self.segments = segments
        
    def __repr__(self):
        return f"Snake of length {self.length} " \
            f"traveling {self.segments[0][1]}"
    
    def turn(self, direction):
        """
        Changes the heading of the snake.

        It adds a new segment with the specified heading at distance -1 from
        the head, so a forward step in the game must immediately follow in
        order to make the new segment the head (at distance 0 from it)

        Paremeters
        ----------
        direction : str
            the direction ('N', E', 'S', or 'W') in which to thurn the snake

        Returns
        -------
        None
        """

        # place a new segment at -1 so that the next step makes it the head
        self.segments.insert(0, [-1, direction])

    def grow(self, length: int = 1):
        """Adds length to the snake's tail"""
        self.length += length



class World:
    """A world containing the snake and food."""

    matrix_moves = {       
        'N' : (-1, 0),      # translates the heading of the segment into
        'S' : (1, 0),       # matrix steps
        'E' : (0, 1),
        'W' : (0, -1)
    }
    
    def __init__(
            self, snake: Snake, pos: list[int] | None = None,
            height: int = 16, width: int = 16, foodchar: str = '*'
            ):
        """
        Initializes the world's attributes.

        By default the snake starts halfway down from the upper wall and 1/4
        from the left wall.
        """
        self.snake = snake
        if pos:
            self.pos = pos
        else:
            i_init = height // 2
            j_init = width // 4
            self.pos = [i_init, j_init]
        if self.pos[1] < self.snake.length - 1:
            raise Exception(f"Snake of length {self.snake.length} is too " /
                            f"long to start at column {self.pos[1]}")
        self.height = height
        self.width = width
        self.foodchar = foodchar
        # populate world
        self.data = [[]]
        self.gen()
        self.insertSnake()
        self.placeFood()

    def __repr__(self):
        self.clearSnake()
        self.insertSnake()
        data = self.data
        s = ''
        s += 'W' * (self.width + 2) + '\n'
        for row in data:
            s += 'W'
            for cell in row:
                s += cell
            s += 'W\n'
        s += 'W' * (self.width + 2)
        return s

    def gen(self):
        """Generate an empty room"""
        self.data = [
            [' ' for cell in range(self.width)]
            for row in range(self.height)
            ]

    def insertSnake(self):
        """Puts the snake in the appropriate cells in self.data"""
        # a 2-d pointer that will move along the snake
        chars = self.snake.chars
        # copy it so changing pointer does not change self.pos
        pointer = [self.pos[0], self.pos[1]]
        segs = self.snake.segments
        for i in range(len(segs)):  # segment indices 
            direction = segs[i][1]
            if direction in ('E', 'W'): char = chars[1]
            else: char = chars[2]
            # the following definition of segment length only works when not
            # on the last segment, because the snake has no defined tail
            if i < len(segs) - 1:
                seg_length = segs[i+1][0] - segs[i][0]
            else:
                seg_length = self.snake.length - segs[i][0]
            for j in range(seg_length):     # for each piece of the seg
                if (
                    pointer[0] not in range(self.height)
                    or pointer[1] not in range(self.width)
                    ):
                    raise Exception("Snake is out of bounds")
                # insert the piece
                self.data[pointer[0]][pointer[1]] = char
                # then update the pointer to move opposite the heading of
                # the segment
                move = self.matrix_moves[direction]
                pointer[0] -= move[0]; pointer[1] -= move[1]
        # do the opposite of the final step of the loops to
        # move the pointer back to the tail;
        # it is 1 move away as it moved after drawing the final piece
        pointer[0] += move[0]; pointer[1] += move[1]
        # the head and tail pieces of the snake are drawn as parts of their
        # segments, so they need to be overwritten
        self.data[pointer[0]][pointer[1]] = chars[3]
        # self.pos is defined to be the head's position
        self.data[self.pos[0]][self.pos[1]] = chars[0]

    def clearSnake(self):
        """Removes the snake from the room, leaving an empty room with food"""
        self.data = [
            [cell if cell not in self.snake.chars else ' ' for cell in row]
            for row in self.data
            ]

    def placeFood(self):
        """
        Inserts one piece of food at a random location not occupied by the
        snake.
        """

        while True:
            i = random.choice(range(self.height))
            j = random.choice(range(self.width))
            # only place and exit once the cell is unoccupied
            if self.data[i][j] == ' ':
                self.data[i][j] = self.foodchar
                break

    def step(self):
        """
        Steps 1 move fowrard, shifting the distance of each segment from
        the head, then moving the head in the direction it is facing.
        """

        if self.snake.segments[0][0] == -1: # if the snake just turned,
            for i in range(2):  # then create the new head, and now the next
                                # statement shifts the old one as well
                self.snake.segments[i][0] += 1
        else:   # shift all of the segments but the head
            for i in range(1, len(self.snake.segments)):
                self.snake.segments[i][0] += 1
        # move the head in the direction it is facing
        move = self.matrix_moves[self.snake.segments[0][1]]
        self.pos[0] += move[0]; self.pos[1] += move[1]

    def onFood(self):
        """Returns True if the snakes's head is on food"""
        if self.data[self.pos[0]][self.pos[1]] == self.foodchar:
            return True
        else: return False

    def loss(self):
        """
        Returns True with losing conditions in the world: if a wall is hit
        or if the snake's own body is hit
        """

        if (
            self.pos[0] not in range(self.height)
            or self.pos[1] not in range(self.width)
            or self.data[self.pos[0]][self.pos[1]] in self.snake.chars[1:]
        ):
            return True
        else: return False

    def run(self, speed: float = 2.0):
        """
        Runs the snake game at the specified speed, the number of times per
        second the world steps
        """

        interval = 1 / speed    # period = frequency ** -1
        key_to_direction = {
            'w' : 'N',
            'a' : 'W',
            's' : 'S',
            'd' : 'E'
        }
        food_eaten = 0
        while not self.loss():  # Maybe change to while True (other check)
            print(self)
            time.sleep(0.5)
            self.step()
            if self.loss(): break
            if self.onFood():
                self.snake.grow()
                food_eaten += 1
                # remove the food that has just been eaten
                self.data[self.pos[0]][self.pos[1]] = ' '
                # Make sure not to place the new food on the cell it was
                # just eaten from
                while self.onFood():
                    self.placeFood()
        print("Game Over")
        print("Your final length:", self.snake.length)
        print("Food Eaten:", food_eaten)

s = Snake(3)
w = World(s)