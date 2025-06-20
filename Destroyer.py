import random, math

class Destroyer:
    
    #create
    def __init__(self):
        self.x = 19
        self.y = 2
        self.course = 0
        self.depthCharge = random.randint(3,18)
        self.sunk = False
        self.DCattack = False
        self.surfaceCombat = False
        self.DIW = False
        
    #move 
    def move(self,convoyCollision,ub):
        badTurn = 'Bad turn input.  DE turns 45, 0, or -45'
        badDrop = 'Invalid input.  Enter two digits, e.g. 100,200.  Return to skip.'
        deMFexpended = 0
        speed = 0
        move = True
        while convoyCollision:
            print(f"Course:{self.course} Enter new course.")
            newCourse = int(input())
            try:
                if newCourse > 225:
                    print('Must turn away from convoy.')
                    continue
            except:
                print('Bad input.  Must enter course to turn away from convoy.')
                continue
            self.course = round(newCourse)
            convoyCollision = False
            return convoyCollision
        convoyCollision = False
        while deMFexpended < 4 and move != '' and not self.DIW:
            #Check for torpedo hits
            if (self.x,self.y) in ub.torps:
                for torp in ub.torps:
                    if (self.x,self.y) == torp:
                        dieRoll = random.randint(1,6)
                    if dieRoll < 3:
                        self.sunk = True
                        return
                    else:
                        print('Torpedo miss.')
            print(f"Position:{self.x},{self.y} Course:{self.course}")
            print(f"DE move.  {4 - deMFexpended} MF left.  Next move(#MF)?")
            move = input()
            if move != '':
                #sanity check input
                try:
                    speed = int(move)
                except:
                    print('Bad MF input.  MF must be integer')
                    continue
                if speed + deMFexpended > 4:
                    print(f"Exceeded MF.  MF expended:{deMFexpended}")
                    continue
                if speed + deMFexpended == 0:
                    if move != '':
                        print('DE must move at least one square.')
                        continue
                if speed == 0:
                    break
                #Sane move, now loop through each square
                for count in range(speed):
                    #Check for DC dropping
                    if self.DCattack:
                        dropped = -1
                        while dropped < 0:
                            print('depth=',ub.depth)
                            print(self.depthCharge,'DCs remain.  DCs drop at 100 ft. depths.  Return to skip.  Up to two valid depths to drop(#,#)?')
                            DCsdropped = input()
                            if DCsdropped == '':
                                break
                            dcText = DCsdropped.split(",")
                            try:
                                dcOne = int(dcText[0])
                                dcTwo = int(dcText[1])
                            except IndexError:
                                print(badDrop)
                                continue
                            except:
                                print('DC one=',dcText[0],'DC two=',dcText[1])
                                print(badDrop)
                                continue
                            if dcOne == False and dcTwo == False:
                                print(badDrop)
                                dropped = -1
                                continue
                            if dcOne != False and dcTwo != False:
                                dropped = 2
                            else:
                                dropped = 1
                            if self.depthCharge - dropped < 0:
                                print(f"Too many DCs.  Only {self.depthCharge} remain.")
                                dropped = -1
                                continue
                            else:
                                self.depthCharge -= dropped
                            #check if DCs hit
                            if self.x == ub.x and self.y == ub.y:
                                if ub.depth == dcOne or ub.depth == dcTwo:
                                    ub.sunk = True
                                elif abs(ub.depth - dcOne) < 200:
                                    ub.nearMiss = True
                                elif dcTwo != 0 and abs(ub.depth - dcTwo) < 200:
                                    ub.nearMiss = True
                    
                        print(dropped,'DCs dropped.')
    
                    deMFexpended += 1
                    self.y += round(math.sin(math.radians(self.course)))
                    self.x += round(math.cos(math.radians(self.course)))
                    #need to check for ramming
                    #Calculate course delta
                    courseDelta = abs(self.course-ub.course)
                    print(f"Course delta={courseDelta}")
                    #Calculate DE to UB distance
                    deltaX = self.x - ub.x
                    deltaY = self.y - ub.y
                    deltaShips = math.sqrt(pow(deltaX,2) + pow(deltaY,2))
                    print('distance=',deltaShips)
                    if deltaShips == 0 and courseDelta == 90:
                        ub.sunk = True
                        print('DE rammed UB.  DE dead-in-water.')
                    goodTurn = False
                    while not goodTurn:
                        print(f"Position: {self.x,self.y} Course: {self.course}")
                        print('Change course (45,0, or -45)?')
                        turnInput = input()
                        #sanity check input
                        try:
                            turn = int(turnInput)
                        except:
                            print(badTurn)
                            continue
                        if turn not in {-45, 0, 45}:
                            print(badTurn)
                            continue
                        goodTurn = True
                    self.course += turn
                    if self.course < 0:
                        self.course = 360 + turn
                    elif self.course > 360:
                        self.course -= 360
                    if self.y < 2:
                        convoyCollision = True
                        print('Potential convoy collision.  Must turn away.')
                        self.y -= round(math.sin(math.radians(self.course)))
                        self.x -= round(math.cos(math.radians(self.course)))
                        break
                    
            elif speed + deMFexpended == 0:
                print('Test two for zero move')
                print('DE must move at least one square.')
                move = True
                continue 
                          
        #Cycled through moves, now check for further DC drops and surface combat
        
        choice = True
        while choice:
            if ub.depth != 0:
                print('Attack with depth charge?[y/n]')
                attackChoice = input()
                try:
                    if attackChoice[0] == 'y':
                        self.DCattack = True
                        break
                    elif attackChoice[0] == 'n':
                        self.DCattack = False
                        break
                    else:
                        print('Bad input.  Enter y or n.')
                        continue
                except:
                    print('Bad input.  Enter y or n.')
                    continue
            else:
                break
        
        print('distance=',deltaShips)
        if deltaShips <= 6 and ub.depth == 0:
            choice = True
            while choice:
                print('Would you like to surface attack?[y/n]')
                attackChoice = input()
                try:
                    if attackChoice[0] == 'y':
                        self.surfaceCombat = True
                        ub.surfaceCombat = True
                        if deltaShips <= 1:
                            if ub.firstSalvo:
                                print('Ships too close.  First salvo advantage lost.  No fire.')
                                ub.firstSalvo = False
                                break
                            dieRoll = random.randint(1,6)
                            if dieRoll <= 3:
                                self.sunk = True
                                break
                            else:
                                print('Miss.')
                                break
                        if ub.firstSalvo:
                            print('First salvo attack.')
                            dieRoll = random.randint(1,6)
                            if dieRoll <= 3:
                                ub.sunk = True
                                break
                            else:
                                print('Miss.')
                                break
                        else:
                            #running gun fight even
                            dieRoll = random.randint(1,6)
                            match dieRoll:
                                case 5:
                                    self.sunk = True
                                case 2:
                                    ub.sunk = True
                                case _:
                                    print('Miss.')
                        break
                    elif attackChoice[0] == 'n':
                        break
                except Exception as e:
                    print('Bad input.  Enter y or n.')
                    continue
            
        #Announce DC near miss
        if ub.nearMiss:
            print('Near miss.')
            
        return convoyCollision
    

    
