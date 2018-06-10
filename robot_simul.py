# 6.00.2x Problem Set 2: Simulating robots

import math
import random

#import ps2_visualize
import pylab

##################
## Comment/uncomment the relevant lines, depending on which version of Python you have
##################

# For Python 3.5:
#from ps2_verify_movement35 import testRobotMovement
# If you get a "Bad magic number" ImportError, you are not using Python 3.5 

# For Python 3.6:
from ps2_verify_movement36 import testRobotMovement
# If you get a "Bad magic number" ImportError, you are not using Python 3.6


# === Provided class Position
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

        angle: number representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        angle = float(angle)
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

    def __str__(self):  
        return "(%0.2f, %0.2f)" % (self.x, self.y)


# === Problem 1
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
        self.cleanTiles = []
        self.tileStatus = {}       # Dictionary of tiles, initially dirty
                                   # 0 = dirty, 1 = clean
        
        for w in range(width):
            for h in range(height):
                tile = (w,h)
                self.tileStatus[tile] = 0
                              
    
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        
        x = int(pos.getX())
        y = int(pos.getY())
        tile = (x,y)
        self.tileStatus[tile] = 1

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        try:
            if self.tileStatus[(m,n)] == 1:
                return True
            else:
                return False
        except:
            raise ValueError('tile not found')
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        total = math.floor(self.height)*math.floor(self.width)
        return total

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        clean = 0
        for i in self.tileStatus:
            if self.tileStatus[i] == 1:
                clean += 1
        return clean

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        w = random.randrange(0,self.width)
        h = random.randrange(0,self.height)
        any = Position(w,h)
        return any

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        return 0 <= pos.x < self.width and 0 <= pos.y < self.height


# === Problem 2
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
        self.room = room
        self.speed = speed
        self.pos = room.getRandomPosition()
        self.dir = random.randint(0,359) 
        self.room.cleanTileAtPosition(self.pos)

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.pos
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.dir

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.pos = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        if direction<0 or direction >=360:
            raise ValueError("Direction must 0=< d < 360")
        else:
            self.dir = direction

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        raise NotImplementedError # don't change this!


# === Problem 3
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it *instead* chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        testPos = self.pos.getNewPosition(self.dir, self.speed)
        if self.room.isPositionInRoom(testPos):
            self.room.cleanTileAtPosition(testPos)
            self.pos = testPos
        else:
            self.dir = random.randint(0,359)

# Uncomment this line to see your implementation of StandardRobot in action!
#testRobotMovement(StandardRobot, RectangularRoom)


# === Problem 4
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
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                RandomWalkRobot)
    """

    totalTime = []
    total = 0
    
    for t in range(num_trials):
        anim = ps2_visualize.RobotVisualization(num_robots, width, height)
        r = RectangularRoom(width, height)
        finish = min_coverage * r.getNumTiles()
        robots = []
        for i in range(num_robots):
            i = StandardRobot(r, speed)
            robots.append(i)
        clockTicks = 0        
        while r.getNumCleanedTiles() <= finish:
            clockTicks += 1
            anim.update(r, robots)
            for robot in robots:
                robot.updatePositionAndClean()
        totalTime.append(clockTicks)
        anim.done()

    for time in totalTime:
        total += time
    mean = round(total/len(totalTime),0)

    return mean


# === Problem 5
class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random at the end of each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        self.dir = random.randint(0,359)
        testPos = self.pos.getNewPosition(self.dir, self.speed)
        if self.room.isPositionInRoom(testPos):
            self.room.cleanTileAtPosition(testPos)
            self.pos = testPos
        else:
            self.dir = random.randint(0,359)

##################################################################
# Run simluations with StandardRobot: 
# runSimulation(num_robots, speed, width, height, min_coverage, 
# num_trials, robot_type)            
################################################################# 
            
# print(runSimulation(1, 1.0, 10, 10, 0.75, 10, StandardRobot))
# print(runSimulation(1, 1.0, 10, 10, 0.75, 30, StandardRobot))
# print(runSimulation(1, 1.0, 10, 10, 0.75, 100, StandardRobot))
# print(runSimulation(1, 1.0, 10, 10, 0.75, 1000, StandardRobot))

##################################################################
# Test Cases with different size rooms and different min_coverage
################################################################# 

# print(runSimulation(1, 1.0, 5, 5, 1.0, 30, StandardRobot))
# expected time: 150 ticks.   #mysim time =
# print(runSimulation(1, 1.0, 10, 10, 0.75, 1, StandardRobot))
# expected time: 190 ticks.   #mysim time = 209.0
# print(runSimulation(1, 1.0, 10, 10, 0.90, 1, StandardRobot))
# expected time: 310 ticks.   #mysim time = 308.0
# print(runSimulation(1, 1.0, 20, 20, 0.99, 30, StandardRobot))
# expected time: 3322 ticks.   #mysim time = 2464.0
# print(runSimulation(3, 1.0, 20, 20, 0.99, 1, StandardRobot))
# expected time: 1105 ticks.   #mysim time = 893.0

# Test Cases with different speeds
# print(runSimulation(1, 1.0, 20, 20, 0.75, 30, StandardRobot))
# speed = 1.0, mean time = 680.0
# print(runSimulation(1, 2.0, 20, 20, 0.75, 30, StandardRobot))
# speed = 2.0, mean time = 744.0
# print(runSimulation(1, 10.0, 20, 20, 0.75, 100, StandardRobot))
# speed = 10.0, mean time = 1829.0, 90% clean = 3091.0 (with 100 trials)
# print(runSimulation(1, 0.5, 20, 20, 0.75, 30, StandardRobot))
# speed = 0.5, mean time = 1131.0
# print(runSimulation(1, 0.25, 20, 20, 0.75, 30, StandardRobot))
# speed = 0.25, mean time = 2102.0

# print(runSimulation(1, 1.0, 10, 10, 0.75, 10, RandomWalkRobot))
# print(runSimulation(1, 1.0, 10, 10, 0.75, 100, RandomWalkRobot))
# print(runSimulation(1, 1.0, 10, 10, 0.75, 1000, RandomWalkRobot))
            
# Uncomment this line to see your implementation of StandardRobot in action!
#testRobotMovement(RandomWalkRobot, RectangularRoom)

def showPlot1(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    num_robot_range = range(1, 5)
    times1 = []
    times2 = []
    for num_robots in num_robot_range:
        print("Plotting", num_robots, "robots...")
        times1.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, StandardRobot))
        times2.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, RandomWalkRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()

    
def showPlot2(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    for width in [10, 20, 25, 50]:
        height = 300//width
        print("Plotting cleaning time for a room of width:", width, "by height:", height)
        aspect_ratios.append(float(width) / height)
        times1.append(runSimulation(3, 1.0, width, height, 0.8, 200, StandardRobot))
        times2.append(runSimulation(3, 1.0, width, height, 0.8, 200, RandomWalkRobot))
    pylab.plot(aspect_ratios, times1)
    pylab.plot(aspect_ratios, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()
    

# === Run RandomWalkRobot simulation    
runSimulation(3, 1.0, 20, 20, 0.9, 200, RandomWalkRobot)    

# === Run Multiple Simulations
# Call showPlot1 or showPlot2 to kick off simulation with StandardRobot
# and RandomWalkRobot    
#showPlot1("Impact of Number of Robots on Cleaning Time", "Number of Robots",\
#          "Average Time (Time-Steps)")
#
# 2) Write a function call to showPlot2 that generates an appropriately-labeled
#     plot.
#
#showPlot2("2 Robots Clean 80% of Rooms with Varying Aspect Ratios",\
#          "Room Width-Height Ratio", "Average Time (Time-Steps)")
