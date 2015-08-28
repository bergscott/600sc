# Problem Set 6: Simulating robots
# Name:
# Collaborators:
# Time:

import math
import random

import ps6_visualize
import pylab

# === Provided classes

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)
    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'

# === Problems 1

class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.width = width
        self.height = height
        self.clean_tiles = {} 
    
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        xy = (int(pos.getX()), int(pos.getY()))
        if not xy in self.clean_tiles:
            self.clean_tiles[xy] = 0

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        return (m, n) in self.clean_tiles
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.width * self.height

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        return len(self.clean_tiles.keys())

    def getPercentCleaned(self):
        """
        Return a float representing a percentage of the room that is cleaned.

        returns: a float (0 <= result <= 1.0)
        """
        return float(self.getNumCleanedTiles()) / self.getNumTiles()

    def getCleanedTiles(self):
        """
        Return a sorted list of clean tiles in the room.

        returns: a list of tuples of (int, int)
        """
        clean_tiles = self.clean_tiles.keys()
        clean_tiles.sort()
        return clean_tiles

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        x = random.uniform(0, self.width)
        y = random.uniform(0, self.height)
        return Position(x, y)

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        return 0 <= pos.getX() < self.width and 0 <= pos.getY() < self.height

def unit_test(result, expected):
    if result == expected:
        print "Test Passed!"
    else:
        raise AssertionError('result, ' + str(result) + \
                ', does not match expected value, ' + str(expected))

class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        #set initial attributes
        self.position = room.getRandomPosition()
        self.direction = random.uniform(0, 360)
        self.speed = speed
        self.room = room
        #clean tile at robot's initial position
        self.room.cleanTileAtPosition(self.position)

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.position
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.position = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction = direction

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        raise NotImplementedError

# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current 
    direction; when it hits a wall, it chooses a new direction randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        def move_bot(self, room, speed):
            # base case
            if speed <= 1.0:
                temp_pos = self.position.getNewPosition(self.direction, speed)
                # check that temp_pos is within confines of room
                if room.isPositionInRoom(temp_pos):
                    # update robot position and clean tile (DONE)
                    self.setRobotPosition(temp_pos)
                    room.cleanTileAtPosition(self.position)
                else:
                    # change direction and try again (recurse)
                    self.setRobotDirection(random.uniform(0, 360))
                    move_bot(self, room, speed)
            # recursive case: move in steps of 1.0 unit
            else: 
                temp_pos = self.position.getNewPosition(self.direction, 1.0)
                # check that temp_pos is within confines of room
                if room.isPositionInRoom(temp_pos): 
                    # update robot position, clean tile, and recurse with
                    # speed - 1.0
                    self.setRobotPosition(temp_pos)
                    room.cleanTileAtPosition(self.position)
                    move_bot(self, room, speed - 1.0)
                else:          
                    # change direction and try again (recurse)
                    self.setRobotDirection(random.uniform(0, 360))
                    move_bot(self, room, speed)
        move_bot(self, self.room, self.speed)

# def test_room():
#     r1 = RectangularRoom(10, 10)
#     p1 = Position(2.3, 4.4)
#     bot1 = StandardRobot(r1, 3.0)
#     unit_test(r1.isPositionInRoom(bot1.getRobotPosition()), True)
#     unit_test(r1.getNumCleanedTiles(), 1)
#     r1.cleanTileAtPosition(p1)
#     unit_test((2, 4) in r1.getCleanedTiles(), True)
#     unit_test(r1.getNumTiles(), 100)
#     print str(bot1.getRobotPosition())
#     print str(r1.getCleanedTiles())
#     for i in range(10):
#         bot1.updatePositionAndClean()
#         print 'position: ' + str(bot1.getRobotPosition())
#         print 'direction: ' + str(bot1.getRobotDirection())
#         print 'cleaned tiles: ' + str(r1.getCleanedTiles())
#         print str(float(r1.getNumCleanedTiles()) / r1.getNumTiles() * 100) + \
#                 ' percent cleaned.'
# 
# test_room()

# === Problem 3

def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    """
    total_time = 0
    for t in xrange(num_trials):
        # anim = ps6_visualize.RobotVisualization(num_robots, width, height)
        room = RectangularRoom(width, height)
        robots = get_robots(num_robots, speed, room, robot_type)
        time_steps = 0
        while room.getPercentCleaned() < min_coverage:
            time_steps += 1
            move_robots(robots)
            # anim.update(room, robots)
        # anim.done()
        # print str(min_coverage * 100) + '% of ' + str(room.getNumTiles()) + \
        #         '-tile room was cleaned in ' + str(time_steps) + ' time steps.'
        total_time += time_steps
    return float(total_time) / num_trials

def get_robots(n, speed, room, robot_type):
    """
    Returns a list of n robots with speed, speed, in room, room. Robots, when
    created, are given random starting positions and directions. robot_type
    specifies the type of robots created
    
    n: an int (n > 0)
    speed: a float (speed > 0)
    room: a RectangularRoom
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                RandomWalkRobot)
    """
    robots = []
    for r in xrange(n):
        robots.append(robot_type(room, speed))
    return robots

def move_robots(robots):
    """
    Moves each robot in robots according to their speed and direction and cleans
    the tiles at each robot's position.
    
    robots: a list of Robot (or subclass of Robot)
    """
    for r in robots:
        r.updatePositionAndClean()

# === Problem 4
#
# 1) How long does it take to clean 80% of a 20*20 room with each of 1-10 robots?
# 
# 2) How long does it take two robots to clean 80% of rooms with dimensions 
#	 20*20, 25*16, 40*10, 50*8, 80*5, and 100*4?

def showPlot1():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """ 
    avgs = []
    for n in xrange(1, 11):
        avg = runSimulation(n, 1.0, 20, 20, .80, 250, StandardRobot)
        avgs.append(avg)
    pylab.plot(range(1, 11), avgs)
    pylab.ylabel('Average Time')
    pylab.xlabel('Number of Robots')
    pylab.title('Dependence of time to clean 80% of a 20x20 room on number of' \
            + ' robots\n')
    pylab.show()

def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    dimensions = ((20, 20), (25, 16), (40, 10), (50, 8), (80, 5), (100, 4))
    ratios = [float(d[0]) / d[1] for d in dimensions]
    avgs = []
    for d in dimensions:
        avg = runSimulation(2, 1.0, d[0], d[1], .80, 250, StandardRobot)
        avgs.append(avg)
    pylab.plot(ratios, avgs)
    pylab.ylabel('Mean Time')
    pylab.xlabel('Ratio of Width to Height of Room')
    pylab.title('Time to clean 80% of a 400-unit area room with 2 robots,\n' +
            'for various ratios of room width to height')
    pylab.show()
    
# === Problem 5

class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random after each time-step.
    """
    raise NotImplementedError


# === Problem 6

# For the parameters tested below (cleaning 80% of a 20x20 square room),
# RandomWalkRobots take approximately twice as long to clean the same room as
# StandardRobots do.
def showPlot3():
    """
    Produces a plot comparing the two robot strategies.
    """
    raise NotImplementedError



