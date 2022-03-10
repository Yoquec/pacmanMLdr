import os
import sys

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

def chooseMaps(fileNameCode: int):
    if fileNameCode == 1:
        pass
    elif fileNameCode == 2:
        pass
    elif fileNameCode == 2:
        pass
    else:
        legalMaps = ["oneHunt"]
    raise NotImplementedError

def modifyGamePy(fileName:str):
    raise NotImplementedError

if __name__ == "__main__":
    # check that we are in the correct directory
    if "game.py" not in os.listdir():
        print("You are not in the correct directory!!!\n\nPlease execute this command from the pacman proyect directory.")
        sys.exit(NotADirectoryError)


    #Get the number of games
    nGames = askForInt("How much games do you want to play", "The number of games must be larger than 0!!!", "The number of games must be an integer!!!")
    

    # Get the available maps
    possibleMaps = [i.replace(".lay", "") for i in os.listdir("layouts/")]

    # Ask for the file to write everything in:
    fileNameMsg = """

What file do you want to store the scraped values in?

[1] training_keyboard.arff

[2] test_samemaps_keyboard.arff

[3] test_othermaps_keyboard.arff
"""
    
    fileNameCode = askForInt(fileNameMsg, "The number chosen must be 1, 2 or 3", "The number chosen must be a number!")
    


