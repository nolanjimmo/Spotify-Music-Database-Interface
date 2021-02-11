# CS205 Team 3 Warm Up Project
# Nolan Jimmo
# Greg Levine
# Echo Norcott
# Delaney Sullivan

# main program holds the interface of the program

def main():
    #Change this to be << but this is easier to read while testing
    command = input("Please enter a command: ")

    #splits command into the individual words to see which SQL line to call
    commandList = command.split()
    commandCall = commandList[0]

    #loop for different commands until quit
    while commandCall.lower() != "quit":
        if commandCall.lower() == "artist":
            artistCommandCall(commandList)
        elif commandCall.lower() == "title":
            titleCommandCall(commandList)
        elif commandCall.lower() == "album":
            albumCommandCall(commandList)
        elif commandCall.lower() == "genre":
            genreCommandCall(commandList)
        #this had to be like this due to the split with spaces
        elif commandCall.lower() == "biggest":
            if commandList[1].lower() == "hit":
                biggestHitCommandCall(commandList)
            else:
                print("Sorry, your command is unrecognized")
        elif commandCall.lower() == "help":
            help()
        else:
            print("Sorry, your command is not recognized")
            help()

        command = input("Please enter a command: ")
        commandList = command.split()
        commandCall = commandList[0]
        commandCall.lower()


#different functions for each SQL call
#each only sends the rest of the command, not the keyword
def artistCommandCall(commandList):
    if (commandList[1].lower() == "title"):
        sqlTitle = commandList[2]
        print("You are looking for the artist of the song ... " + sqlTitle)
    elif (commandList[1].lower() == "album"):
        sqlAlbum = commandList[2]
        print("You are looking for the artist of the album ... " + sqlAlbum)
    else:
        print("Your command could not be understood")
        help()
    sqlArtist = commandList[0][6:]
    print("You are looking for an artist named..." + sqlArtist)

def titleCommandCall(commandList):
    if (commandList[1].lower() == "biggest" and commandList[2].lower() == "hit"):
        # print("You are looking for the biggest hit from artist ... " + commandList[3])
        biggestHitCommandCall(commandList[1:])
    sqlTitle = commandList[0][5:]
    print("You are looking for an title named... " + sqlTitle)

def albumCommandCall(commandList):
    if (commandList[1].lower() == "title"):
        sqlTitle = commandList[2]
        print("You are looking for the album of song ... " + sqlTitle)
    elif (commandList[1].lower() == "artist"):
        sqlArtist = commandList[2]
        print ("You are looking for an album by artist ... " + sqlArtist)
    sqlAlbum = commandList[0][5:]
    print("You are looking for an album named... " + sqlAlbum)

def genreCommandCall(commandList):
    if (commandList[1].lower() == "title"):
        sqlTitle = commandList[2]
        print("You are looking for the genre of song ... " + sqlTitle)
    elif (commandList[1].lower() == "artist"):
        sqlArtist = commandList[2]
        print("You are looking for the genre of artist ... " + sqlArtist)
    elif (commandList[1].lower() == "album"):
        sqlAlbum = commandList[2]
        print("You are looking for the genre of the album ... " + sqlAlbum)
    sqlGenre = commandList[0][5:]
    print("You are looking for a genre named..." + sqlGenre)

def biggestHitCommandCall(commandList):
    if (commandList[2].lower() == "artist"):
        sqlArtist = commandList[3]
        print("You are looking for the biggest hit of artist ... " + sqlArtist)
    else:
        sqlArtist = commandList[2]
        print("You are looking for the biggest hit of artist ... " + sqlArtist)
    # sqlBiggestHit = commandList[3][10:]
    # print("You are looking for a biggest hit named..." + sqlBiggestHit)

def help():
    print("You may enter: ")
    print("- Album")
    print("- Artist")
    print("- Biggest Hit")
    print("- Genre")
    print("- Title")



main()
