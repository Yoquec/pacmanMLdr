import os
import sys
from typing import List
import random

def askForInt(prompt:str , errorMsgAssert: str="", errorMsgVal: str="") -> int:
    setv = False
    while not setv:
        try:
            outInt = int(input(f"{prompt}: "))
            # Exit the loop
            assert(outInt > 0)
            setv = True

        except AssertionError as e:
            print(f"ERROR!, {errorMsgAssert}\n{e}\n\n")

        except ValueError as e:
            print(f"ERROR!, {errorMsgVal}\n{e}\n\n")

    return outInt

def choosePossibleMaps() -> List[str]:
    legalMaps = [i.replace(".lay", "") for i in os.listdir("layouts") if i != "minimaxClassic.lay"]

    return legalMaps


def modifyGamePy(fileName:str) -> None:
    newLine = f'        CSV_FILE_NAME = "{fileName}"\n'

    nLine, contents = getCsvNameDeclarationLine()

    if nLine:
        contents[nLine] = newLine
        
        with open("game.py", "w") as file:
            [file.write(i) for i in contents]

    else:
        raise FileNotFoundError("Wasn't able to find the line containing the declaration of CSV_FILE_NAME")

def fileNameCodeToFileName(fileNameCode:int, isKeyboardGame: bool) -> str:
    if isKeyboardGame:
        fileName = ["training_keyboard.arff", "test_samemaps_keyboard.arff", "test_othermaps_keyboard.arff"][fileNameCode - 1]
    else:
        fileName = ["training_tutorial1.arff", "test_samemaps_tutorial1.arff", "test_othermaps_tutorial1.arff"][fileNameCode - 1]

    return fileName


def createKeyboardGame(nGames: int):
    # Get the possibleMaps
    possibleMaps = choosePossibleMaps()

    # modify game.py file to store the what we need in the correct file
    # modifyGamePy(fileNameCodeToFileName(fileNameCode, True))

    for i in range(nGames):
        currentMap = random.choice(possibleMaps)
        staticGhost = random.randint(0,4)

        if staticGhost:
            exeStr = f"python3 busters.py -g RandomGhost -l {currentMap}"
        else:
            exeStr = f"python3 busters.py -l {currentMap}"

        os.system(exeStr)

def createAutoGame(nGames: int):
    # Get the possibleMaps
    possibleMaps = choosePossibleMaps()

    # modify game.py file to store the what we need in the correct file
    # modifyGamePy(fileNameCodeToFileName(fileNameCode, False))

    for i in range(nGames):
        currentMap = random.choice(possibleMaps)
        staticGhost = random.randint(0,4)

        if staticGhost:
            exeStr = f"python3 busters.py -p BasicAgentAA -g RandomGhost -l {currentMap}"
        else:
            exeStr = f"python3 busters.py -p BasicAgentAA -l {currentMap}"

        os.system(exeStr)

def getCsvNameDeclarationLine():
    with open("game.py", "r") as file:
        lines = file.readlines()
        for i in range(len(lines)):
            line = lines[i]
            if "CSV_FILE_NAME" in line and "=" in line:
                nLine = i
                break

        else:
            nLine = None

        return nLine, lines
 

if __name__ == "__main__":
    # check that we are in the correct directory
    if "game.py" not in os.listdir():
        print("You are not in the correct directory!!!\n\nPlease execute this command from the pacman proyect directory.")
        sys.exit(NotADirectoryError)

    isKeyboardGame = askForInt(
            "Do you want to play yourself with the keyboard??\n\n[1] Yes\n\n[2] No \n\n",
            "Please pick a either 1 or 2",
            "Please choose a number either 1 or 2"
            )

    #Get the number of games
    nGames = askForInt("How much games do you want to play", "The number of games must be larger than 0!!!", "The number of games must be an integer!!!")
    

    if isKeyboardGame == 1:
        createKeyboardGame(nGames)
    else:
        createAutoGame(nGames)
