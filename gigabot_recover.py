import glob

print("Manually find the height of the print using the extruder head and move axis commands.")

files = glob.glob("*.gcode")
if len(files) == 0:
    print("No files found! Move the .gcode you want to recover to the same folder as this script and run it again.")
    exit()
fileFound = False
homeXYUpdated = False
filamentGcodeFound = False
zHeightfound = False
checkForEndOfZHeight = False

for fileName in files:
    if fileFound:
        exit()
    print("Is \"" + fileName + "\" the file you want to recover? Enter \"y\" or \"n\".")
    fileConfirm = input()

    if fileConfirm.lower() == "y":
        fileFound = True
        recoveredFile = open("recovered_" + fileName, "w")
        print(fileName + "confirmed!")
        print("What z-height do you want to recover from? Enter an integer with no decimal places.")
        zHeight = input()

        if zHeight.isdigit():
            print(zHeight + " confirmed!")
        else:
            print(zHeight + " is not a valid entry. Bye!")
            exit()

        with open(fileName) as file:
            for line in file:
                lastZHeight = ""
                if zHeightfound:
                    recoveredFile.write(line)
                elif line.startswith("G28") and not homeXYUpdated:
                    recoveredFile.write("G28 X Y\n")
                    homeXYUpdated = True
                elif line == "; Filament gcode\n":
                    filamentGcodeFound = True
                elif not filamentGcodeFound:
                    recoveredFile.write(line)
                elif line.startswith("G1 Z" + zHeight):
                    print("Z-Height found!")
                    print("Is this the height you want? y/n")
                    print(line)
                    zHeightInput = input()
                    if zHeightInput.lower() == "y":
                        zHeightfound = True
                        recoveredFile.write(line)
                    elif zHeightInput.lower() == "n":
                        checkForEndOfZHeight = True
                        print("Okay, next!")
                    else:
                        print("That wasn't valid... Have fun starting over!")
                        exit()
                elif checkForEndOfZHeight and line.startswith("G1 Z"):
                    print("No more lines with " + zHeight + " as the height found!")
                    print("Use this line? y/n")
                    print(line)
                    lastZHeightInput = input()
                    if lastZHeightInput.lower() == "y":
                        recoveredFile.write(line)
                        zHeightfound = True
                    elif lastZHeightInput.lower() == "n":
                        print("Okay, next!")
                    else:
                        print("That wasn't valid... Have fun starting over!")
                        exit()

    elif fileConfirm.lower() == "n":
        print(fileName + " is not the file. Next!")
    else:
        print("You didn't enter \"y\" or \"n\"! :(\n I'm done with you...")
        exit()

print("Finished!")
print("It is highly recommended that you manually check this .gcode to ensure this worked!")
print("This .gcode includes a home X Y command, but it will not home Z.")
print("You should set the desired Z height manually and then run this .gcode.")
