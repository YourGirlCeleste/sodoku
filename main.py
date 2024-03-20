import random
import os
import sys

pictoralConversion = {0:'🟦',1:'1️⃣ ',2:'2️⃣ ',3:'3️⃣ ',4:'4️⃣ ',5:'5️⃣ ',6:'6️⃣ ',7:'7️⃣ ',8:'8️⃣ ',9:'9️⃣ '}
tabCount = 11
blocksToRemove = 30
gameRun = True

map = [
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
]
bigBlocks = [

    [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)],
    [(0,3),(0,4),(0,5),(1,3),(1,4),(1,5),(2,3),(2,4),(2,5)],
    [(0,6),(0,7),(0,8),(1,6),(1,7),(1,8),(2,6),(2,7),(2,8)],
    [(3,0),(3,1),(3,2),(4,0),(4,1),(4,2),(5,0),(5,1),(5,2)],
    [(3,3),(3,4),(3,5),(4,3),(4,4),(4,5),(5,3),(5,4),(5,5)],
    [(3,6),(3,7),(3,8),(4,6),(4,7),(4,8),(5,6),(5,7),(5,8)],
    [(6,0),(6,1),(6,2),(7,0),(7,1),(7,2),(8,0),(8,1),(8,2)],
    [(6,3),(6,4),(6,5),(7,3),(7,4),(7,5),(8,3),(8,4),(8,5)],
    [(6,6),(6,7),(6,8),(7,6),(7,7),(7,8),(8,6),(8,7),(8,8)]
]
startingBlocks = []

errorMsg = ""

def start():

    boardNotFilled = True
    while (boardNotFilled):
        blocksFilled = 0
        # Empty Board
        for block in bigBlocks:
            for coords in block:
                    map[coords[0]][coords[1]] = 0

        # Fill Board
        for block in bigBlocks:

            blockNotFilled = True
            boardTries = 0

            while blockNotFilled:
                boardTries += 1

                if boardTries > 5:
                    break
                # Empty Block
                for coords in block:
                    map[coords[0]][coords[1]] = 0

                # Fill Block
                possibleValues = [1,2,3,4,5,6,7,8,9]
                for coords in block:

                    randomValue = random.choice(possibleValues)
                    timesTried = 0
                    while(not validate(coords[0],coords[1],randomValue) and timesTried < 15):
                        randomValue = random.choice(possibleValues)
                        timesTried += 1

                    if(timesTried < 15):
                        map[coords[0]][coords[1]] = randomValue
                        possibleValues.remove(randomValue)

                    if len(possibleValues) == 0:
                        blockNotFilled = False
                        blocksFilled +=1

            if boardTries > 5:
                break
            elif blocksFilled == 9:
                boardNotFilled = False
    
    # Remove random tiles
    for i in range(blocksToRemove):

        ranX = random.randint(0,8)
        ranY = random.randint(0,8)

        if (ranX,ranY) not in startingBlocks:

            map[ranX][ranY] = 0
            startingBlocks.append((ranX,ranY))
    
def display():
    os.system('cls')

    print('\t'*tabCount, "   1 2 3   4 5 6   7 8 9")
    for n,x in enumerate(map):

        print('\t'*tabCount, f"{n+1} ", end="")

        for j,y in enumerate(x):

            print(pictoralConversion[y],end="")

            if j == 2 or j == 5:

                print(' |',end="")
        print()

        if n == 2 or n == 5:

            print('\t'*tabCount, " ",'-'*23)
    
    print()
    print('\t'*tabCount,errorMsg)

def userInput():
    global errorMsg

    print('\t'*tabCount, end= "")
    inputCoords = list(input("Enter a blocks coords to modify it: "))

    if inputCoords == ['q']:
        sys.exit()

    # Validate Coords
    errorMsg=""
    if len(inputCoords) == 2:

        for x in inputCoords:

            if x.isnumeric():

                if int(x) > 9 or int(x) < 1:

                    errorMsg='out of range'
                    return
                
            else:           
               errorMsg="Not an int"
               return
    else:
        errorMsg='missing or extra number'
        return
    if (int(inputCoords[0])-1,int(inputCoords[1])-1) not in startingBlocks:

        errorMsg="Can't modify starting blocks"
        return


    print('\t'*tabCount, end= "")
    inputValue = input("Enter a number for the block: ")

    # Validate Value
    if(inputValue.isnumeric()):

        if(int(inputValue) < 1 or int(inputValue) > 9):

            errorMsg = "Value out of range"
            return
    else:
        errorMsg = "Value not an int"
        return
    
    # Update map
    map[int(inputCoords[0])-1][int(inputCoords[1])-1] = int(inputValue)

def validate(x,y,value):

    # Row Check
    if value in map[x]:
        return False

    # Col Check
    for row in range(9):

        if value == map[row][y]:
            return False
        
   
    return True

def checkWin():

    # Row Check
    for row in map:

        targetValues = [1,2,3,4,5,6,7,8,9]
        for value in row:
            
            if value in targetValues:
                targetValues.remove(value)
        
        if len(targetValues) != 0:
            return False
    
    # Col Check
    for colVal in range(9):

        targetValues = [1,2,3,4,5,6,7,8,9]
        for rowVal in range(9):
            value = map[rowVal][colVal]
            if value in targetValues:
                targetValues.remove(value)
        
        if len(targetValues) != 0:
            return False
    
    # Big Block Check
    for block in bigBlocks:

        targetValues = [1,2,3,4,5,6,7,8,9]
        for coords in block:
            value = map[coords[0]][coords[1]]
            if value in targetValues:
                targetValues.remove(value)
        
        if len(targetValues) != 0:
            return False
    
    return True


start()
while gameRun:
    display()
    userInput()
    
    if checkWin():

        print('\t'*tabCount,"--YOU WIN--")
        gameRun = False

sys.exit()
