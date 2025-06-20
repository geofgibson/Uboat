import math
import Sub, Destroyer

#Create environment
de=Destroyer.Destroyer()
convoyCollision = False
ub=Sub.Submarine()
gameTurn = 1

#Main run loop

#Check for victory
while ub.sunk == False and de.sunk == False and ub.y != 1:
    if ub.y == 1 and (ub.torps < 3 or ub.depth == 0):
        print('U-Boat In convoy but not victorious.  Must finish surface combat.')
        continue
    print(f"Starting game turn {gameTurn}")
    if ub.torpsRunning:
        print('Torpedoes running.')
    #Calculate DE to UB distance
    deltaX = de.x - ub.x
    deltaY = de.y - ub.y
    deltaShips = math.sqrt(pow(deltaX,2) + pow(deltaY,2))

    if deltaShips >1 or ub.depth == 0:
        print(f"UB:{ub.x},{ub.y} Course:{ub.course} Depth:{ub.depth}")
    elif ub.depth > 0:
        print('UB in sonar blind zone.')
    print(f"DE:{de.x},{de.y} Course:{de.course}")
    
    #DE move .. depth charge throws
    convoyCollision = de.move(convoyCollision,ub)
    #UB move
    ub.move(de)
    
    gameTurn += 1
    print('ub.sunk=',ub.sunk,'de.sunk=',de.sunk,'ub.y=',ub.y)
    #ub.torps = ((20,1),(10,10),(de.x,de.y))
            
    
else:
    if ub.sunk:
        print('UB sunk.')
    elif de.sunk:
        print('DE sunk.')
