import random, math

class Submarine:

    #create
    def __init__(self):
        self.x = 20
        self.y = 4
        self.depth = 100
        #self.x = 11
        #self.y = 20
        self.course = 270
        #self.depth = 0
        self.torps = random.randint(3,18)
        self.sunk = False
        self.nearMiss = False
        self.firstSalvo = True
        self.surfaceCombat = False
        self.surfaced = False
        self.torps = ((0,0),(0,0),(0,0),(0,0))
        self.torpsRunning = False
        
    #move
    def move(self,de):
        ubMFexpended = 0
        move = True
        badTurn = 'Bad turn input.  UB turns 90, 45, 0, -45, or -90'
        badDepth = 'Bad input.  Enter a number: 0, 100, 200, 300, 400'
        while ubMFexpended < 2 and move != '':
            print('ubMFexpended=',ubMFexpended,' move=',move)
            print(f"Position:{self.x},{self.y} Course:{self.course} Depth:{self.depth}")
            if self.depth == 0 or de.DCattack:
                print(f"UB move.  {2 - ubMFexpended} MF left.  Next move(#MF)?")
            else:
                print(f"UB move.  1 MF left.  Next move(#MF)?")
            move = input()
            if move != '':
                #sanity check input
                try:
                    speed = int(move)
                except:
                    print('Bad MF input.  MF must be integer')
                    continue
                if self.depth == 0 or de.DCattack:
                    if speed + ubMFexpended > 2:
                        print(f"Exceeded MF.  MF expended:{ubMFexpended}")
                        continue
                else:
                    if speed + ubMFexpended > 1:
                        print(f"Exceeded MF.  MF expended:{ubMFexpended}")
                        continue
                if speed + ubMFexpended == 0:
                    print('UB must move at least one square.')
                    continue
                if speed == 0:
                    break
            elif ubMFexpended == 0:
                print('UB must move at least one square.')
                move = True
                continue
            ubMFexpended += 1
            self.y += round(math.sin(math.radians(self.course)))
            self.x += round(math.cos(math.radians(self.course)))
            goodTurn = False
            print('new x=',self.x,'new y=',self.y)
            while not goodTurn:
                print(f"Position: {self.x,self.y} Course: {self.course} Depth:{self.depth}")
                print('Change course (90, 45,0, -45, or -90)?')
                turnInput = input()
                #sanity check input
                try:
                    turn = int(turnInput)
                except:
                    print(badTurn)
                    continue
                if turn not in {-90, -45, 0, 45, 90}:
                    print(badTurn)
                    continue
                goodTurn = True
            self.course += turn
            if self.course < 0:
                self.course = 360 + turn
            elif self.course > 360:
                self.course -= 360
            goodDepth = False
            if not self.surfaced:
                while not goodDepth:
                    print("Change depth (+/-100' enter 0, 100, 200, 300, or 400)?")
                    depthChange = input()
                    if depthChange == '':
                        break
                    try:
                        depth = int(depthChange)
                    except:
                        print(badDepth)
                        continue
                    if depth not in {0, 100, 200, 300, 400}:
                        print(badDepth)
                        continue
                    if abs(self.depth - depth) > 100:
                        print("Can only change depth by +/-100'.")
                        continue
                    self.depth = depth
                    goodDepth = True
                    if self.depth == 0:
                        self.surfaced = True
        choice = True
        while choice:
            print('Fire torpedoes?[y/n]')
            fireTorps = input()
            try:
                if fireTorps[0] == 'y':
                    self.torpsRunning = True
                    while True:
                        print('Number of torps. to launch?(1,2,3,or 4)')
                        numTorps = input()
                        try:
                            number = int(numTorps)
                        except:
                            print('Bad input.  Enter 1,2,3, or 4.')
                            continue
                        if number not in {1,2,3,4}:
                            print('Bad input.  Enter 1,2,3, or 4.')
                            continue
                        for torpedo in range(0,number-1):
                          while True:
                              print(f"Torpedo {torpedo+1} square?(x,y)")
                              square = input()
                    
                    break
                elif fireTorps[0] == 'n':
                    #self.DCattack = False
                    break
                else:
                    print('Bad input.  Enter y or n.')
                    continue
            except:
                print('Bad input.  Enter y or n.')
                continue
            
        print('Returning from UB move')
        return

    #launch torps

    #surface combat
