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
        # Spatial Pooler Variables
        global inhibitionRadius
        
        self.overlap = CustomList(length)
        self.boost = CustomList(length)
        self.maxDutyCycle = CustomList()
        self.minDutyCycle = CustomList()
        self.activeDutyCycle = CustomList()
        self.overlapDutyCycle = CustomList()
        self.potentialSynapses = dict()
        self.connectedSynapses = dict()
        self.columns = range(length)
        self.inputVectors = inputVectors
        
        # Temporal Pooler Variables

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
    
    # Phase 1 of spatial pooler function
    def overlap(self, t):
        for c in self.columns:
            
            self.overlap[c] = 0
            for s in self.connectedSynapses[c]:
                self.overlap[c] = self.overlap[c] + self.input(t, s.sourceInput)
                
            if self.overlap[c] < minOverlap :
                self.overlap[c] = 0
            else :
                self.overlap[c] = self.overlap[c] * self.boost(c)
    
    # Phase 2 of spatial pooler function            
    def inhibition(self, t):
        for c in self.columns:
            
            minLocalActivity = self.kthScore(self.neighbors(c), self.desiredLocalActivity)
            
            if self.overlap[c] > 0 and self.overlap[c] >= minLocalActivity:
                self.activeColumns[t].append(c)
    
    # Phase 3 of spatial pooler function            
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
            
    
    # Phase 1 of temporal pooler function -- Inference alone
    def compute_activeState_IA(self, t):
        for c in self.activeColumns[t]:
            buPredicted = False
            for i in range(cellsPerColumn):
                if predictiveState(c, i, t-1) == True:
                    s = getActiveSegment(c, i, t-1, activeState)
                    if s.sequenceSegment == True:
                        buPredicted = True
                        activeState[c, i, t] = 1
            
            if buPredicted == False:
                for i in range(cellsPerColumn):
                    activeState[c, i, t] = 1
                    
    # Phase 2 of temporal pooler function -- Inference alone
    def compute_predictiveState_IA(self, t):
        for c, i in cells:
            for s in segments(c, i):
                if segmentActive(c, i, s, t):
                    predictiveState[c, i, t] = 1
    
    # Phase 1 of temporal pooler -- combined inference and learning
    def compute_activeState(self, t):
        for c in activeColumns[t]:
            
            buPredicted = False
            IcChosen = False
            for i in range(cellsPerColumn):
                if predictiveState[c, i, t-1] == True:
                    s = getActiveSegment(c, i, t-1, activeState)
                    if s.sequenceSegment == True:
                        buPredicted = True
                        activeState[c, i, t] = 1
                        if segmentActive[s, t-1, learnState]:
                            IcChosen = True
                            learnState[c, i, t] = 1
            
            if buPredicted == False:
                for i in range(cellsPerColumn):
                    activeState[c, i, t] = 1
            
            if IcChosen == False:
                l, s = getBestMatchingCell[c, t-1]
                learnState[c, i, t] = 1
                sUpdate = getSegmentActiveSynapses[c, i, s, t-1, True]
                sUpdate.sequenceSegment = True
                segmentUpdateList.add(sUpdate)
    
    # Phase 2 of temporal pooler -- combined inference and learning
    def compute_predictiveState(self, t):
        for c, i in cells:
            for s in segments[c, i]:
                if segmentActive[s, t, activeState] :
                    predictiveState[c, i, t] = 1
                    
                    activeUpdate = getSegmentActiveSynapses[c, i, s, t, False]
                    segmentUpdateList.add(activeUpdate)
                    
                    predSegment = getBestMatchingSegment(c, i, t-1)
                    predUpdate = getSegmentActiveSynapses(c, i, predSegment, t-1, True)
                    segmentUpdateList.add(predUpdate)
    
    # Phase 3 of temporal pooler function
    def update_synapses():
        for c, i in cells:
            if learnState[s, i, t] == 1 :
                adaptSegments (segmentUpdateList[c, i], True)
                segmentUpdateList[c, i].delete()
            elif predictiveState[c, i, t] == 0 and predictiveState[c, i, t-1] == 1:
              adaptSegments ( segmentUpdateList[c,i], False)
              segmentUpdateList[c, i].delete()  
