
# Literate Bowling Kata
# Thomas Perl <m@thp.io>; 2012-10-21

# "Literate programming" style using the text from Wikipedia:
# http://en.wikipedia.org/wiki/Bowling#Scoring

ALL_PINS = 10
FRAMES = 10

# In ten pin bowling, matches consist of each player bowling a "game".

class Game:
    def __init__(self, frames):
        # Each game is divided into ten "frames".
        self.frames = list(frames)
        self.connect_frames()

    def connect_frames(self):
        # That's the only "dirty" method here - connecting frames via their
        # position in the list. The last frame's frame_next is None
        for index, frame in enumerate(self.frames[:-1]):
            frame.next_frame = self.frames[index+1]

    def get_score(self):
        # The game's score is the sum of the scores for all frames
        return sum(frame.get_score() for frame in self.frames[:FRAMES])

# A frame allows a bowler two chances to knock down all ten pins.
class Roll:
    def __init__(self, frame, knocked_down):
        self.frame = frame
        self.knocked_down = knocked_down

    @property
    def next_roll(self):
        if self == self.frame.first_roll and not self.frame.strike:
            return self.frame.second_roll
        else:
            return self.frame.next_frame.first_roll

class Frame:
    def __init__(self, first_roll, second_roll=0):
        self.first_roll = Roll(self, first_roll)
        self.second_roll = Roll(self, second_roll)
        self.next_frame = None

    @property
    def strike(self):
        # A "strike" is scored when a player knocks down all pins on the first
        # roll in the frame.
        return self.first_roll.knocked_down == ALL_PINS

    @property
    def spare(self):
        # A "spare" is scored when all pins are knocked down using both rolls
        # in the frame.
        return not self.strike and (self.first_roll.knocked_down +
                self.second_roll.knocked_down) == ALL_PINS

    def get_score(self):
        # The number of pins knocked over in each frame is recorded, a running
        # total is made as each frame progresses, and the player with the
        # highest score in his/her game wins the match.
        score = self.first_roll.knocked_down
        score += self.second_roll.knocked_down

        # Scores can be greater than the actual number of pins knocked over if
        # strikes or spares are bowled.

        # A "strike" [...]
        if self.strike:
            # Rather than a score of 10 for the frame, the player's score will
            # be 10 plus the total pins knocked down on the next two rolls in
            # the next frame(s).
            score += self.next_frame.first_roll.knocked_down
            score += self.next_frame.first_roll.next_roll.knocked_down

        # A "spare" [...]
        if self.spare:
            # The player's score for that frame will be 10 plus the number of
            # pins knocked down on the first roll in the next frame.
            score += self.next_frame.first_roll.knocked_down

        return score

def parse_input(line):
    # Parses the format from http://pyug.at/PythonDojo/KataBowling and
    # yields Frame objects
    line = list(line)
    while line:
        first = line.pop(0)
        if first == 'X':
            yield Frame(10)
            continue
        if line:
            second = line.pop(0)
        else:
            second = 0

        if first == '-':
            first = 0
        else:
            first = int(first)

        if second == '/':
            second = ALL_PINS - first
        elif second == '-':
            second = 0
        else:
            second = int(second)

        yield Frame(first, second)


# A player who rolls a spare or strike in the last frame is given one or two
# more rolls to score additional points, respectively.
frames = [Frame(10), Frame(10), Frame(10), Frame(10), Frame(10),
          Frame(10), Frame(10), Frame(10), Frame(10), Frame(10),
          Frame(10), Frame(10)]
game = Game(frames)
print 'score:', game.get_score()

# from http://pyug.at/PythonDojo/KataBowling
TEST_CASES = (
    ('XXXXXXXXXXXX', 300),
    ('9-9-9-9-9-9-9-9-9-9-', 90),
    ('5/5/5/5/5/5/5/5/5/5/5', 150),
    ('X7/729/XXX236/7/3', 168),
    ('--------------------', 0),
    ('-1273/X5/7/3454--X7-', 113),
    ('X7/9-X-88/-6XXX81', 167),
)

for line, score in TEST_CASES:
    assert Game(parse_input(line)).get_score() == score

