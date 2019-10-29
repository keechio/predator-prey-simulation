
class World:

    def __init__(self, x = 600, y = 400):
        """
        initialization function for world        
        parameters: self, x representing width, y representing height
        variables: width, height, and list of agents 
        """
        self._x = x
        self._y = y
        self._agents = {}

    def getx(self):
        """
        returns the x boundary of world
        """
        return self._x

    def gety(self):
        """
        returns the y boundary of world
        """
        return self._y

    def __getitem__(self, position):
        """
        returns the agent at position if there is a agent there, else it returns
        none
        operator overloaded so method is called by world[position]
        """
        if position in self._agents:
            return self._agents[position]
        return None

    def __setitem__(self, position, agent):
        """
        sets the agent at given position
        operator overloaded so method is called by world[position] = agent
        """
        self._agents[position] = agent

    def __delitem__(self, position):
        """
        deletes agent at given position
        """
        if position in self._agents:
            del self._agents[position]
        
