Predator and Prey Simulation
by Joshua Tang

The Predator and Prey Simulation models the population changes 
between Predator's and Prey as time passes. 

The program has 4 files, world, vector, agents, and simulationRun.
The world class creates a x by y canvas and keeps track of all the
agents. The vector class is just to calculate vectors to determine
each agents movement. The agent class creates each agent and has
two subclasses, one being prey and the other predator. 
simulationRun is the file that runs all the other ones and 
contains the main function that runs the program. 
World creates a world turtle that creates the world. Each agent
has a turtle and variables some specific to the subclass. Both
subclasses have two movement methods. They both have wander which
just makes them walk around. The predator will hunt when it is 
hungry and it sees prey. The prey will flee when it sees a 
predator. All functions are based on ticks. One move command is 
one tick. one move command is a vector with magnitude 1 multiplied
by the speed of the agent. 
What is adjustable are the variables of agents and simulationRun.
simulationRun
Width - how many units in the width of the canvas
Heigh - how many units in the height of the canvas
runtime - how many ticks to run for
numpredator - starting number of predator agents
numprey - starting number of prey agents
agents 
predatorspeed - move vector of predator multiplied by 
predatorspeed(predator should be faster then prey)
preyspeed - move vector of prey multiplied by preyspeed
preadatorsightrange - radius of what agents the predator sees, 
will only pursue prey within sight range
preysightrange - radius of what agents the prey sees, runs away
when a predator enters that radius
wandercounter - how many ticks until the agent gets a random 
heading while wandering, used to prevent an agent from getting 
stuck in a cornor
predatorstarvation - how many ticks until the predator starves, 
or gets deleted 
predatorbirth - how many ticks until the predator produces another
predator
preybirth - how many ticks until the prey produces another prey
fulltime - how many ticks after a predator has eaten until it 
seeks out another prey. Prevents one predator from jumping from 
prey to prey and killing all the prey.

I did not include any user input features while the program is 
running. User input could be added at the beginning like number 
of predator or size of the world. But it makes more sense that
the person adjusts the variables directly in the program so you 
don't have to type certain variables over and over again. 
Everything else should work. The current variable values either
skew the simulation towards too many predators or too many prey.
Values need to be adjusted. The program is also very laggy when 
there are too many agents.