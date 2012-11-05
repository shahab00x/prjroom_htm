from random import Random

minOverlap = 10
connectedPerm = .5
permanenceInc = .05
inhibitionRadius = 10

class CustomList(list):
    def __init__(self, length=0):
        self.l = [0]*length
    def __call__(self):
        return self.l
    def __getitem__(self, c):
        return self.l[c]
    def __setitem__(self, c, v):
        self.l[c] = v
    
class Synapse:
    def __init__(self, sourceInput):
        self.permanence = Random().random()/5. - .1 + connectedPerm
        self.sourceInput = sourceInput

class HTM:
    def __init__(self, inputVectors, length=20000, depth=1):
        global inhibitionRadius
        
        self.overlap = CustomList(length)
        self.potentialSynapses = dict()
        self.connectedSynapses = dict()
        self.columns = [i for i in range(length)]
        self.inputVectors = inputVectors
        self.boost = CustomList()
        self.maxDutyCycle = CustomList()
        self.minDutyCycle = CustomList()
        self.activeDutyCycle = CustomList()
        self.overlapDutyCycle = CustomList()
        
    def input(self, t, j):
        return self.inputVectors[t][j] == True
    
    def boostFunction(self,activeDutyCycle, minDutyCycle):
        # Fill here
        pass
    
    def updateActiveDutyCycle(self, c):
        # Fill here
        pass
    
    def updateOverlapDutyCycle(self, c):
        # Fill here
        pass
    
    def increasePermanences(self, c, inc):
        # Fill here
        pass
    
    def averageReceptiveFieldSize(self):
        # Fill here
        pass
    
    def overlap(self, t):
        for c in self.columns:
            
            self.overlap[c] = 0
            for s in self.connectedSynapses[c]:
                self.overlap[c] = self.overlap[c] + self.input(t, s.sourceInput)
                
            if self.overlap[c] < minOverlap :
                self.overlap[c] = 0
            else :
                self.overlap[c] = self.overlap[c] * self.boost(c)
                
    def inhibition(self, t):
        for c in self.columns:
            
            minLocalActivity = self.kthScore(self.neighbors(c), self.desiredLocalActivity)
            
            if self.overlap[c] > 0 and self.overlap[c] >= minLocalActivity:
                self.activeColumns[t].append(c)
                
    def learning(self, t):
        for c in self.activeColumns[t]:
            for s in self.potentialSynapses[c]:
                if self.active(s) :
                    s.permanence += permanenceInc
                    s.permanence = min(1.0, s.permanence)
                else:
                    s.permanence -= permanenceInc
                    s.permanence = max(0.0, s.permanence)
            
        for c in self.columns:
            self.minDutyCycle[c] = 0.01 * self.maxDutyCycle( self.neighbors(c))
            self.activeDutyCycle[c] = self.updateActiveDutyCycle(c)
            self.boost[c] = self.boostFunction(self.activeDutyCycle[c], self.minDutyCycle[c])
            
            self.overlapDutyCycle[c] = self.updateOverlapDutyCycle(c)
            if self.overlapDutyCycle[c] < self.minDutyCycle[c]:
                self.increasePermanences(c, 0.1*connectedPerm)
        
        inhibitionRadius = self.averageReceptiveFieldSize()
            
            
        