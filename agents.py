import random
import turtle
import vector
import math

PREDATOR_SPEED = 3
PREY_SPEED = 1
PREDATOR_SIGHT_RANGE = 70
PREY_SIGHT_RANGE = 35
PREDATOR_KILL_RANGE = 8
WANDER_COUNTER = 50
PREDATOR_STARVATION = 60
PREDATOR_BIRTH = 120
PREY_BIRTH = 100
FULL_TIME = 30


class Agents:
    def __init__(self, x, y, angle):
        """
        makes sure the xy position isn't alreadyoccupied by another agent 
        if it is then it generates a new random position for the current agent
        """
        while (self._world[x, y] != None):
            x = random.uniform(0, self._world.getx())
            y = random.uniform(0, self._world.gety())
        self._wanderCounter = random.randint(0, 14)
        self._birthCounter = random.randint(0, 100)
        self._angle = angle
        self._x = x
        self._y = y
        self._world[x, y] = self    
        self._turtle = turtle.Turtle()
        self._turtle.speed(0)
        self._turtle.setheading(angle)
        self._turtle.penup()
        self._turtle.goto(x, y)
        self._turtle.resizemode("user")
        self._turtle.shapesize(.6, .6, .6)
        if(isinstance(self, Predator)):
            self._turtle.shape("arrow")
        elif(isinstance(self, Prey)):
            self._turtle.shape("turtle")

    def getx(self):
        """
        returns the x coordinate of the agent
        """
        return self._x

    def gety(self):
        """
        returns the y coordinate of the agent
        """
        return self._y

    def distance(self, x2, y2):
        return math.sqrt(((self.getx() - x2) ** 2) + ((self.gety() - y2) ** 2)) 
        

class Predator(Agents):
    def __init__(self, world, x = -1, y = -1, angle = 700):  
        self._world = world
        if(x == -1):
            x = random.uniform(0, world.getx())
            y = random.uniform(0, world.gety())
        if(angle == 700):
            angle = random.uniform(0, 360)
        Agents.__init__(self, x, y, angle)
        self._starvationCounter = 0
        self._fullCounter = 0

    def wander(self):
        if(self._wanderCounter >= WANDER_COUNTER):
            self._wanderCounter = 0
            self._turtle.setheading(random.uniform(0, 360))
            self._angle = self._turtle.heading() 
        heading = self._turtle.heading()
        wanderVector = vector.Vector(math.cos(math.radians(heading)),
                                     math.sin(math.radians(heading)))
        wanderVector = wanderVector.unitScale()
        return wanderVector

    def hunt(self):
        preyPosition = self.findClosestPreyNeighbor()
        neighbors = self.findNeighbors()
        if neighbors[preyPosition] <= PREDATOR_KILL_RANGE:
            self.kill(preyPosition)
        preyVectorX = preyPosition[0] - self.getx()
        preyVectorY = preyPosition[1] - self.gety()
        preyVector = vector.Vector(preyVectorX, preyVectorY)
        preyVector = preyVector.unitScale()
        return preyVector

    def move(self):
        moveVector = self.wander()

        if(self._fullCounter > 0):
            moveVector = self.wander()
            self._fullCounter -= 1
        elif(self.findClosestPreyNeighbor() != None):
            moveVector = self.hunt()
        else:
            moveVector = self.wander()
            self._wanderCounter += 1
        originalVector = vector.Vector(self.getx(), self.gety())
        moveVector.scale(PREDATOR_SPEED)
        finalVector = moveVector + originalVector
        finalVectorDirection = vector.Vector(finalVector._x - originalVector._x,
                                             finalVector._y - originalVector._y)

        heading = self._turtle.heading()
        #heading 0 is east and 90 is north while atan2 returns 0 as north
        #and 90 and east, so i convert heading to atan2 degrees
        originalVectorDirection = vector.Vector(math.cos(math.radians(heading)),
                                     math.sin(math.radians(heading)))
        #uses atan2 to find the finalvector heading
        newAngle =(math.degrees(math.atan2(finalVectorDirection._x,
                                           finalVectorDirection._y))
                   - (math.degrees(math.atan2(originalVectorDirection._x,
                                           originalVectorDirection._y))))                   
        newAngle = self._angle - newAngle
        self._angle = newAngle
        self._turtle.setheading(self._angle)
        if(finalVector._x >= self._world.gety() or
           finalVector._x <= 0 or
           finalVector._y >= self._world.gety() or
           finalVector._y <= 0):
            self._angle = (self._angle + 180) % 360
            self._turtle.setheading(self._angle)
            
        self._turtle.goto(finalVector._x, finalVector._y)

        del self._world._agents[self.getx(), self.gety()]
        self._x = self._turtle.xcor()
        self._y = self._turtle.ycor()
        self._world._agents[self.getx(), self.gety()] = self

        if(self._starvationCounter >= PREDATOR_STARVATION):
            position = (self.getx(), self.gety())
            self._world._agents[position]._turtle.hideturtle()
            del self._world._agents[position]._turtle
            del self._world._agents[position]

        if(self._birthCounter >= PREDATOR_BIRTH):
            predator = Predator(self._world, self.getx() - 5.1, self.gety()-5.1)
            self._birthCounter = 0

        self._starvationCounter += 1
        self._birthCounter += 1

    def findNeighbors(self):
        """
        parameters: an instance of an agent
        returns a dictionary of agents within a certain distance from the agent
        dictionary key is the position and the value is the distance from self
        agent
        """
        neighbors = {}
        for position in self._world._agents:
            agentx = self._world._agents[position].getx()
            agenty = self._world._agents[position].gety()
            neighborDistance = self.distance(agentx, agenty) 
            if ((neighborDistance <= PREDATOR_SIGHT_RANGE) and
                position != (self.getx(), self.gety())):
                neighbors[(agentx, agenty)] = neighborDistance
        return neighbors

    def findClosestPreyNeighbor(self):
        """
        parameters: an instance of an agent
        returns the position of the closest Prey to the predator agent
        """
        neighbors = self.findNeighbors()
        closestPreyDistance = PREDATOR_SIGHT_RANGE
        closestPrey = None
        for position in neighbors:
            if (isinstance(self._world._agents[position], Prey)):
                if(neighbors[position] <= closestPreyDistance):
                    closestPreyDistance = neighbors[position]
                    closestPrey = position
        return closestPrey

    def kill(self, position):
        self._world._agents[position]._turtle.hideturtle()
        del self._world._agents[position]._turtle
        del self._world._agents[position]
        self._starvationCounter = 0
        self._fullCounter = FULL_TIME

class Prey(Agents):
    def __init__(self, world, x = -1, y = -1, angle = 700):
        self._world = world 
        if(x == -1):
            x = random.uniform(0, world.getx())
            y = random.uniform(0, world.gety())
        if(angle == 700):
            angle = random.uniform(0, 360)
        Agents.__init__(self, x, y, angle)

    def wander(self):
        if(self._wanderCounter >= WANDER_COUNTER):
            self._wanderCounter = 0
            self._turtle.setheading(random.uniform(0, 360))
            self._angle = self._turtle.heading()
        heading = self._turtle.heading()
        wanderVector = vector.Vector(math.cos(math.radians(heading)),
                                     math.sin(math.radians(heading)))
        wanderVector = wanderVector.unitScale()
        return wanderVector

    def flee(self):
        predatorPosition = self.findClosestPredatorNeighbor()
        neighbors = self.findNeighbors()
        predatorVectorX = -(predatorPosition[0] - self.getx())
        predatorVectorY = -(predatorPosition[1] - self.gety())
        predatorVector = vector.Vector(predatorVectorX, predatorVectorY)
        predatorVector = predatorVector.unitScale()
        return predatorVector

    def move(self):
        moveVector = self.wander()
        if(self.findClosestPredatorNeighbor() != None):
            moveVector = self.flee()
        else:
            self._wanderCounter += 1
            moveVector = self.wander()
        originalVector = vector.Vector(self.getx(), self.gety())
        moveVector.scale(PREY_SPEED)
        finalVector = moveVector + originalVector
        finalVectorDirection = vector.Vector(finalVector._x - originalVector._x,
                                             finalVector._y - originalVector._y)

        heading = self._turtle.heading()
        originalVectorDirection = vector.Vector(math.cos(math.radians(heading)),
                                     math.sin(math.radians(heading)))
        newAngle =(math.degrees(math.atan2(finalVectorDirection._x,
                                           finalVectorDirection._y))
                   - (math.degrees(math.atan2(originalVectorDirection._x,
                                           originalVectorDirection._y))))                   
        newAngle = self._angle - newAngle
        self._angle = newAngle
        self._turtle.setheading(self._angle)
        
        if(finalVector._x >= self._world.gety() or
           finalVector._x <= 0 or
           finalVector._y >= self._world.gety() or
           finalVector._y <= 0):
            self._angle = (self._angle + 180) % 360
            self._turtle.setheading(self._angle)

        if finalVector._x >= self._world.gety():
            finalVector.set((2 * self._world.getx()) - finalVector._x,
                            finalVector._y)
        if finalVector._x <= 0:
            finalVector.set(abs(finalVector._x), finalVector._y)
        if finalVector._y >= self._world.gety():
            finalVector.set(finalVector._x,
                            (2 * self._world.gety()) - finalVector._y)
        if finalVector._y <= 0:
            finalVector.set(finalVector._x, abs(finalVector._y))
            
        self._turtle.goto(finalVector._x, finalVector._y)

        del self._world._agents[self.getx(), self.gety()]
        self._x = self._turtle.xcor()
        self._y = self._turtle.ycor()
        self._world._agents[self.getx(), self.gety()] = self

        if(self._birthCounter >= PREY_BIRTH):
            prey = Prey(self._world, self.getx() - 5.2, self.gety() - 5.2)
            self._birthCounter = 0

        self._birthCounter += 1

    def findNeighbors(self):
        """
        parameters: an instance of an agent
        returns a dictionary of agents within a certain distance from the agent
        dictionary key is the position and the value is the distance from self
        agent
        """
        neighbors = {}
        for position in self._world._agents:
            agentx = self._world._agents[position].getx()
            agenty = self._world._agents[position].gety()
            neighborDistance = self.distance(agentx, agenty) 
            if ((neighborDistance <= PREY_SIGHT_RANGE) and
                position != (self.getx(), self.gety())):
                neighbors[(agentx, agenty)] = neighborDistance
        return neighbors

    def findClosestPredatorNeighbor(self):
        """
        parameters: an instance of an agent
        returns the position of the closest Prey to the predator agent
        """
        neighbors = self.findNeighbors()
        closestPredatorDistance = PREY_SIGHT_RANGE
        closestPredator = None
        for position in neighbors:
            if (isinstance(self._world._agents[position], Predator)):
                if(neighbors[position] <= closestPredatorDistance):
                    closestPredatorDistance = neighbors[position]
                    closestPredator = position
        return closestPredator
