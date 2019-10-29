import world
import agents
import turtle

WIDTH = 200
HEIGHT = 200
RUNTIME = 10000
NUMPREDATOR = 2
NUMPREY = 10

def main():
    worldTurtle = turtle.Turtle()
    screen = worldTurtle.getscreen()
    screen.setworldcoordinates(0, 0, WIDTH, HEIGHT)
    worldTurtle.hideturtle()

    simulationWorld = world.World(WIDTH, HEIGHT)

    for numPredator in range(NUMPREDATOR):
        predator = agents.Predator(simulationWorld)

    for numPrey in range(NUMPREY):
        prey = agents.Prey(simulationWorld)

    runtimeCounter = 0
    while(runtimeCounter <= RUNTIME):
        preyList = []
        predatorList = []
        for position in prey._world._agents:
            if(isinstance(prey._world._agents[position], agents.Prey)):
                preyList.append(position)
            elif(isinstance(prey._world._agents[position], agents.Predator)):
                predatorList.append(position)
        for position in preyList:
            #prey moves first so that when the prey dies they update
            #if we call predator first then when it kill it will produce
            #an error when it tries to move the prey the predator killed
            prey._world._agents[position].move()
            
        for position in predatorList:
            predator._world._agents[position].move()
                
        runtimeCounter += 1
    

    screen.update()

main()
        

