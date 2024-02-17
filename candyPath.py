#===================================================================================================================#
# By:           Cade Collison                                                                                       #
# Date:         11/16/2023                                                                                          #
# Assignment:   Assignment 6 [candyRealm.py]                                                                        #
# Course:       COM S 127 Section 2                                                                                 #
# Description:  This Python script is written to emulate the children's game "Candyland". It consists of functions  #
#               that execute one or more specific tasks to ensure the game runs smoothly. The path is created to    #
#               set each games colors along with start at the beginning and goal at the end. The player area        #
#               consists of open tiles for the player's pieces to occupy. In order for the player to move their     #
#               piece they must draw a card that has an index in the path larger than the player's current index.   #
#               If the card they drew has an index that is equal to the player's index nothing happens to the       #
#               current player's piece, the current player's turn ends and the next players turn begins. To         #
#               determine if the current player can move forward, there is a window created at the start of their   #
#               turn that takes that starts with the tile that is one tile ahead of the player's current index and  #
#               ends at the "Goal" tile. The script checks to see if that tile can be moved to and does so if it    #
#               respronds in the affirmative. At the end of each player's turn, the script checks for any pieces in #
#               the "Goal" tile and returns the player's number as well as ending the game loop. For real players   #
#               and "AI bots", there will be a message printed under another message annoucing that their turn is   #
#               up in which that message states the actions that the current player took.                           #
# Citations:    PyPi                                                                                                #
#                   URL - https://pypi.org/project/colorama/                                                        #
#                   Author - N/A                                                                                    #
#                   Publish Date - N/A                                                                              #
#                   Date Accessed - 12/01/2023                                                                      #
#                   Citation - “Colorama.” PyPI, pypi.org/project/colorama/. Accessed 1 Dec. 2023.                  #
#===================================================================================================================#

""" [Changes from candyRealm-4.py to candyPath.py (final submission)]:
#===================================================================================================================#
#     ++ Removed parameter of getBotQty, "playerQty" as it serves no functionality to the function.                 #
#     ++ movePiece:                                                                                                 #
#         ++ Added functionality to the function to move a piece one "tile" at a time. I implemented recursion to   #
#            repeatedly move the player's x-coordinate one coordinate to the right until the player's piece reaches #
#            the the base case where the player's piece reaches mX-coordinate or the index of the card that that    #
#            player drew.                                                                                           #
#         ++ Added a 1 second delay to in-between each recursion with the "time.sleep()" command.                   #
#         ++ Added "path" parameter to mvePiece in order to to satisfy the printBoard "path" parameter.             #
#     ++ playGame:                                                                                                  #
#         ++ Added a new variable "botSpeed" that prompts the player to adjust how fast they'd like each AI bot to  #
#            make their decision of they set the quantity of bots to be 1 or more. This variable is passed into the #
#            "AIplayerTurn" function where a new command has been written to delay the AI's decision by however long#
#            the variable is.                                                                                       #
#===================================================================================================================#
"""

from os import system as sys
import time
import random
from colorama import Back
import secrets

# colorama.init(autoreset=True)

# "Colored Output - print(Back.GREEN + 'and with a green background')". [PyPi]
layColors = {
    'R' : {"fore": Back.RED,     "full": "Red"},
    'G' : {"fore": Back.GREEN,   "full": "Green"},
    'Y' : {"fore": Back.YELLOW,  "full": "Yellow"},
    'B' : {"fore": Back.BLUE,    "full": "Blue"},
    'M' : {"fore": Back.MAGENTA, "full": "Magenta"},
    'C' : {"fore": Back.CYAN,    "full": "Cyan"},
    'Start' : {"fore": Back.RESET},
    'Goal' : {"fore": Back.RESET}
}

def printTitleMaterial():
    """Prints the title material for the game, including the student's name, class, and section number.
    """
    print("Candy Path!")
    print()

    print("By: Cade Collison")
    print("[COM S 127 2]")
    print()

def initialChoice():
    """Gets the player's initial choice at the start of the script."""
    validOptions = ['p','i','q'] # List of the only acceptable possibilities
    while True:
        choice = input("Select an option:\n  [P]lay Game\n  [I]nstructions\n  [Q]uit\n\t-> ").lower()
        while len(choice) == 0 or choice not in validOptions:
            print("  ## ERROR ##: Invalid option, please try again...")
            choice = input("Select an option:\n  [P]lay Game\n  [I]nstructions\n  [Q]uit\n\t-> ").lower()
        break
    return choice

def setPlayerQty():
    """Gets the number of players to play the game from the user."""
    while True:
        try:
            playerQty = int(input("Enter number of players:\n\t-> "))
            # Fixed while loop from "playerQty < 0" in candyRealm-3.py to "playerQty < 1"
            while playerQty < 1: # Making sure at least one play is playing
                # Rewrote error message saying only 1-4 players were allowed in candyRealm-3.py
                print("  ## ERROR ##: 1+ players allowed.")
                playerQty = int(input("Enter number of players):\n\t-> "))
            break
        except ValueError as VE:
            print(f"## ERROR ##: {VE}")
            continue
    return playerQty

def getBotQty():
    """Gets the number of AI bots that will play the game from the user."""
    while True:
        try:
            botQty = int(input("Enter number of AI bots to play with:\n\t-> "))
            while botQty < 0: # Making sure the player doesn't enter a negative number or bots to play
                print("  ## ERROR ##: AI bot count can't be 0.")
                botQty = int(input("Enter number of AI bots to play with:\n\t-> "))
            break
        except ValueError as VE:
            print(f"## ERROR ##: {VE}")
            continue
    return botQty

def getPathColorQty():
    """Gets the number of unique colors that will be randomly applied to each tile of the path from the user."""
    while True:
        try:
            uniqueColors = int(input("How many unique colors will the path contain (3 - 6)?:\n\t-> "))
            while uniqueColors < 3 or uniqueColors > 6: # Making sure the player pick 3 or higher so the colorCooldown works and 6 or less since there are only 6 colors
                print("  ## ERROR ##: There must be between 3 and 6 unique colors, please try again...")
                uniqueColors = int(input("How many unique colors will the path contain (3 - 6)?:\n\t-> "))
            break
        except ValueError as VE:
            print(f"## ERROR ##: {VE}")
            continue
    return uniqueColors
    
def getPathLength(colorQty):
    """Gets the number of tiles that will have random colors on them from the user."""
    while True:
        try:
            maxPathLength = int(input("How many blocks will the path contain (adjust to fit yout terminal)?:\n\t-> "))
            while maxPathLength < colorQty: # Making sure the number of colored tiles will be greater than the number of colors that will be in the path
                print("  ## ERROR ##: There must be more path tiles than uniqur colors, please try again...")
                maxPathLength = int(input("How many blocks will the path contain (adjust to fit yout terminal)?:\n\t-> "))
            break
        except ValueError as VE:
            print(f"## ERROR ##: {VE}")
            continue
    return maxPathLength
    
def generatePath(colorQty: int, pathLength: int) -> list:
    """Generates a game path that begins with "Start", the tiles for maxPathLength, and end with "Goal"."""
    colors = ['R','G','Y','B','M','C']
    
    gameColors = []
    # This loop will add a random color to the game path and add that color to the cooldown
    for i in range(colorQty):
        tempColor = secrets.choice(colors)
        gameColors.append(tempColor)
        colors.remove(tempColor)
        
    path = []
    path.append("Start")
    colorCooldown = []
    # This for loop adds two colors and to the path and list of colors to cooldown
    for i in range(2):
        tempBlock = secrets.choice(gameColors)
        path.append(f" {tempBlock}  ") # 5 long
        gameColors.remove(tempBlock)
        colorCooldown.append(tempBlock)
    # Ths for loop iterates through the available colors, chooses one to add to path, adds it to the cooldown list, 
    # and adds the color that has "cooled down" the longest to the available colors
    for i in range(pathLength - 2):
        tempBlock = secrets.choice(gameColors)
        path.append(f" {tempBlock}  ") # 5 long
        gameColors.append(colorCooldown.pop())
        gameColors.remove(tempBlock)
        colorCooldown.append(tempBlock)
    path.append("Goal")
            
    return path

def generatePlayerArea(path, playerQty: int):
    """Generates the the player area that the players' pieces will be "placed" and can move around in."""
    playerArea = []
    # This loop will add a list for into playerArea for every player
    for p in range(playerQty):
        playerArea.append([])
    
    # This loop will insert each players' "piece" in the first tile
    for i in range(len(playerArea)):
        playerArea[i].append(f"  {i+1} ")
        # This loop will add the appropriate amount of tiles to each player's list 
        for j in range(len(path)-2): 
            playerArea[i].append('    ') # 5 long
        playerArea[i].append(Back.RESET + '    ')
        
    return playerArea

def getPlayerIndex(playerArea, playerNum):
    """Returns the index of a player as an "x-axis"."""
    # These loops check each element inside of each list and return the index of the player
    for y in range(len(playerArea)):
        for x in range(len(playerArea[y])):
            if playerArea[y][x].strip() == str(playerNum):
                return x
            
def getColorIndex(path, color):
    """Returns the index of a color as an "x-axis"."""
    # These loops check each color in the path and return the index of the color
    for c in range(len(path)):
        if path[c].strip() == color:
            return c
    return -1 # May return -1 since the color may not be in the possibiltiyPath in playerTurn()

def movePiece(msg, playerArea, path, pX, pY, mX, mY):
    """Moves the piece at index pX, pY to mX, mY"""
    # pX and pY represent x and y coordinates of the piece that will be moved
    # mX and mY represent x and y coordinates of the position in the playing area that the piece will be moved to
    sys("clear")
    print(msg)
    if mX == pX:
        return playerArea
    playerArea[mY][pX+1] = playerArea[pY][pX]
    playerArea[pY][pX] = '    '
    printBoard(path, playerArea)
    time.sleep(1)
    return movePiece(msg, playerArea, path, pX+1, pY, mX, mY)

def printBoard(path: list, playerArea: list):
    """Prints out the board including the player area and the the borders around it."""
    print()
    print(f"{Back.WHITE + ('-') * (((len(path))*5)+1)}{Back.RESET}")
    for i in range(len(playerArea)):
        for j in range(len(path)):
            print(layColors[path[j].strip()]["fore"] + f"{playerArea[i][j]}", end=" ")
        print()
    print(f"{Back.WHITE + ('-') * (((len(path))*5)+1)}{Back.RESET}")
    print(f"Start {'     ' * (len(path)-2)} Goal")
    print()
    
def generateDeck(path):
    """Generates a deck of 52 random colored cards."""
    deck = [secrets.choice(path[1:len(path)-1]).strip() for card in range(52)]
    return deck

def drawCard(deck):
    """Draws a card from the top of a deck and then moves it to the bottom."""
    card = deck[0] # Top of deck
    deck.remove(card)
    deck.append(card) # Places it back at the bottom
    return card, deck

def checkWinner(playerArea, playerNum, path):
    """Checks if a winner has been found. The way it determines this is if it finds a player in the last index of the list or the "Goal" tile and returns that player number."""
    return getPlayerIndex(playerArea, playerNum) == len(path) - 1

def playerTurn(playerNum, deck, playerArea, path):
    """Operates as the players turn where they are presented with three options."""
    choiceOptions = ['d','s','p']
    
    print(f"-- Player {playerNum}\'s Turn --")
    choice = input("Would you like to [d]raw a card, [s]huffle the deck, or [p]ass your turn?:\n\t-> ")
    
    while choice not in choiceOptions:
        print("\t\t## ERROR ##: Invalid choice! Try again...\n")
        choice = input("Would you like to [d]raw a card, [s]huffle the deck, or [p]ass your turn?:\n\t-> ")
        
    if choice == 'd':
        card = drawCard(deck)[0]
        msg = f"\tPlayer {playerNum} drew: " + layColors[card]["full"]
        playerIndex = getPlayerIndex(playerArea, playerNum)
        
        if playerIndex == len(path)-2: # The last colored tile
            movePiece(msg, playerArea, path, playerIndex, playerNum-1, len(playerArea[0])-1, playerNum-1)
        else:
            possibilityPath = [color.strip() for color in path[playerIndex+1:]]
            cardIndex = getColorIndex(possibilityPath, card)
            
            if (cardIndex+1)+playerIndex > playerIndex:
                movePiece(msg, playerArea, path, playerIndex, playerNum-1, playerIndex+(cardIndex+1), playerNum-1)
            else: print(f"\tPlayer {playerNum} could not move.")
            
    elif choice == 's':
        sys("clear")
        printBoard(path, playerArea)
        deck = generateDeck(path)
        print("The deck has been re-shuffled to:\n")
        choice = input("Would you like to [d]raw a card or [p]ass your turn?:\n\t-> ")
        
        while choice not in choiceOptions or choice == 's':
            print("\t\t## ERROR ##: Invalid choice! Try again...\n")
            choice = input("Would you like to [d]raw a card or [p]ass your turn?:\n\t-> ")
            
        if choice == 'd':
            card = drawCard(deck)[0]
            msg = f"\tPlayer {playerNum} drew: " + layColors[card]["full"]
            playerIndex = getPlayerIndex(playerArea, playerNum)
            
            if playerIndex == len(path)-2: # The last colored tile
                movePiece(msg, playerArea, path, playerIndex, playerNum-1, len(playerArea[0])-1, playerNum-1)
            else:
                possibilityPath = [color.strip() for color in path[playerIndex+1:]]
                cardIndex = getColorIndex(possibilityPath, card)
                
                if (cardIndex+1)+playerIndex > playerIndex:
                    movePiece(msg, playerArea, path, playerIndex, playerNum-1, playerIndex+(cardIndex+1), playerNum-1)
                else: print(f"\t\tPlayer {playerNum} could not move.")
                
        elif choice == 'p':
            sys("clear")
            for i in range(5):
                print(f"\t\tPlayer {playerNum} turn passed")
                print("#" * i, end="")
                print("-" * (5-i))
                time.sleep(.5)
                sys("clear")
            sys("clear")
            
    elif choice == 'p':
        sys("clear")
        for i in range(5):
            print(f"\t\tPlayer {playerNum} turn passed")
            print("#" * i, end="")
            print("-" * (5-i))
            time.sleep(.5)
            sys("clear")
        sys("clear")
        
    return deck

def AIplayerTurn(playerNum, deck, playerArea, path, botSpeed):
    """Operates as the AI bots' decision-making procces."""
    choiceOptions = ['d','s']
    print(f"-- Player {playerNum}\'s Turn --")
    playerIndex = getPlayerIndex(playerArea, playerNum)
    card = drawCard(deck)[0]
    
    if playerIndex == len(path)-2: # The last colored tile
        msg = f"\tPlayer {playerNum} drew:" + layColors[card]["full"]
        movePiece(msg, playerArea, path, playerIndex, playerNum-1, len(playerArea[0])-1, playerNum-1)
    else:
        decisionLink = [random.choice(choiceOptions)]
        possibilityPath = [color.strip() for color in path[playerIndex+1:]]
        cardIndex = getColorIndex(possibilityPath, card)
        print(f"\tPlayer {playerNum} is making their decision...")
        time.sleep(botSpeed)
        
        # I improved decision making for AI from candyRealm-3.py
        if decisionLink[0] == 'd':
            msg = f"\tPlayer {playerNum} drew: " + layColors[card]["full"]
            
            if (cardIndex+1)+playerIndex > playerIndex:
                movePiece(msg, playerArea, path, playerIndex, playerNum-1, playerIndex+(cardIndex+1), playerNum-1)
            else:
                for i in range(5):
                    print(f"\t\tPlayer {playerNum} could not move.")
                    print("#" * i, end="")
                    print("-" * (5-i))
                    time.sleep(.5)
                    sys("clear")
                sys("clear")
            
        elif decisionLink[0] == 's':
            print(f"\t\tPlayer {playerNum} shuffled the deck")
            print(f"\t\tPlayer {playerNum} is making their decision...")
            time.sleep(botSpeed)
            # If AI selects 's' then they automatically draw a card instead of possibly opting to pass their turn
            if (cardIndex+1)+playerIndex > playerIndex:    
                msg = f"\tPlayer {playerNum} drew: " + layColors[card]["full"]
                movePiece(msg, playerArea, path, playerIndex, playerNum-1, playerIndex+(cardIndex+1), playerNum-1)
            else:
                for i in range(5):
                    print(f"\t\tPlayer {playerNum} could not move.")
                    print("#" * i, end="")
                    print("-" * (5-i))
                    time.sleep(.5)
                    sys("clear")
                sys("clear")
                
        else:
            for i in range(5):
                print(f"\tPlayer {playerNum} turn passed")
                print("#" * i, end="")
                print("-" * (5-i))
                time.sleep(.5)
                sys("clear")
            sys("clear")
            
    return deck
    
def playGame():
    """The main operating systme for the game. Initializes game variables and runs a while loop for setting up the game.
        In the while loop, it runs a for loop for the amount of players in the game and AI bots if there are any."""
    # gameplay variables
    path = []
    deck = []
    playerWinner = False
    AIWinner = False
    
    while not playerWinner and not AIWinner: # Loop until either a player or bot wins
        print(" === Setting Rules === ")
        playerQty = setPlayerQty()
        botQty = getBotQty()
        if botQty > 0:
            while True:
                try:
                    botSpeed = float(input("Enter how fast you'd like the bot(s) to make thier decision in seconds:\n\t-> "))
                    while botSpeed <= 0:
                        print("  ## ERROR ##: AI bot speed must be greater than 0, please try again...")
                        botSpeed = float(input("Enter how fast you'd like the bot(s) to make thier decision in seconds:\n\t-> "))
                    break
                except Exception as E:
                    print(f"  ## ERROR ##: {E}, please try again...")
                    continue
        totalPlayerQty = playerQty + botQty
        colorQty = getPathColorQty()
        pathLength = getPathLength(colorQty)
        
        path = generatePath(colorQty, pathLength)
        deck = generateDeck(path)
        playerArea = generatePlayerArea(path, totalPlayerQty)
        sys("clear")
        printBoard(path, playerArea)
        
        while True: # Loop until a winner is found in "Goal" tile
            for i in range(1, playerQty + 1):
                deck = playerTurn(i, deck, playerArea, path)
                printBoard(path, playerArea)
                playerWinner = checkWinner(playerArea, i, path)
                if playerWinner:
                    print(f"Player {i} Wins!!!")
                    print()
                    break
            if playerWinner:
                break

            for b in range(playerQty + 1, totalPlayerQty + 1):
                print()
                deck = AIplayerTurn(b, deck, playerArea, path, botSpeed)
                printBoard(path, playerArea)
                AIWinner = checkWinner(playerArea, b, path)
                if AIWinner:
                    print(f"Player {b} Wins!!!")
                    print()
                    break
            if AIWinner:
                break
        
def printInstructions():
    """Displays the instructions for Candy Path."""
    print("""
#=================================================================================================================================================================#
# Candy Path Instructions                                                                                                                                        #
#                                                                                                                                                                 #
#   Make your way down the colorful Candy Path and race to the end of the road!                                                                                  #
#                                                                                                                                                                 #
#   ++ Setting Up The Game                                                                                                                                        #
#       - Enter the amount of players that will play (1+ players)                                                                                                 #
#       - Enter the amount of AI bots to play with (0+ bots)                                                                                                      #
#       - Enter the amount of unique colors to randomly be placed on the path (3-6 colors)                                                                        #
#       - Enter the amount of colored tiles to be placed on the path (adjust to preference)                                                                       #
#                                                                                                                                                                 #
#   ++ Player Turn                                                                                                                                                #
#       - At any given turn for any player, that player will have three initial options for how they wish to proceed.                                             #
#           - The player can draw a card from the deck and move to card tile they drew if it is in-between the player and the goal.                               #
#           - The player can shuffle the deck where they can then:                                                                                                #
#               - Draw a card from the deck and move to card tile they drew if it is in-between the player and the goal.                                          #
#               - Pass their current turn                                                                                                                         #
#           - The player can pass up their current turn                                                                                                           #
#                                                                                                                                                                 #
#   ++ How To Win :)                                                                                                                                              #
#       - If a player is on the last colored tile and it is their turn to draw a card, once that player draws a card, they advance to the "Goal" tile and win!!!  #
#=================================================================================================================================================================#
         """)

def main():
    """This function is where all the fun happens!"""
    sys("clear")
    printTitleMaterial()
    
    running = True
    
    initialOptions = {
        'p' : playGame,
        'i' : printInstructions,
        'q' : quit
    }
    
    while running:
        choice = initialChoice()
        sys("clear")
        initialOptions[choice]()    


if __name__ == "__main__":
    main()