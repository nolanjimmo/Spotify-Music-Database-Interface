# CS205 Team 3 Warm Up Project
# Nolan Jimmo
# Greg Levine
# Echo Norcott
# Delaney Sullivan

# main program holds the interface of the program
import sqlite3
from sqlite3 import Error

def main():
    cursor = createConnection()
    doubleCommandQuery('artists', 'genre', "Alesso", cursor)
    doubleCommandQuery('songs', 'artist' , 'Under Control', cursor)
    doubleCommandQuery('artists', 'title', 'Swedish House Mafia', cursor)

    #Change this to be << but this is easier to read while testing
    command = input("Please enter a command: ")

    #splits command into the individual words to see which SQL line to call
    commandList = command.split()
    commandCall = commandList[0]

    #loop for different commands until quit
    while commandCall != "quit":
        if commandCall == "artist":
            artistCommandCall(command)
        elif commandCall == "title":
            titleCommandCall(command)
        elif commandCall == "album":
            albumCommandCall(command)
        elif commandCall == "genre":
            genreCommandCall(command)
        #this had to be like this due to the split with spaces
        elif commandCall == "biggest":
            if commandList[1] == "hit":
                biggestHitCommandCall(command)
            else:
                print("Sorry, your command is unrecognized")
        elif commandCall == "help":
            help()
        else:
            print("Sorry, your command is not recognized")
            help()

        command = input("Please enter a command: ")
        commandList = command.split()
        commandCall = commandList[0]


##########Database Interaction#########################

#alternate way to access the database using a single and double command query
#I am going to comment out the connection to the database right now so we don't get any messy errors when we run for now
def createConnection():
    connection = None
    try:
        connection = sqlite3.connect('SongsArtistsDB.db')
    except Error as e:
        print(e)
    finally:
        if connection:
            return connection.cursor()

def doubleCommandQuery(command1, command2, desiredData, curs):
    if command1 == "artists" and command2 != "title" and command2 != "album":
        curs.execute("SELECT %s FROM %s WHERE name = '%s'" % (command2, command1, desiredData))
    elif command1 == "songs":
        curs.execute("SELECT %s FROM %s WHERE title = '%s'" % (command2, command1, desiredData))
    else:
        if command2 == "title":
            curs.execute("SELECT title FROM songs INNER JOIN artists ON songs.artist = artists.name WHERE "
                         "songs.artist = '%s'" % desiredData)

    rows = curs.fetchall()
    for row in rows:
        print(row[0])


#different functions for each SQL call
#each only sends the rest of the command, not the keyword
def artistCommandCall(fullCommand):
    sqlArtist = fullCommand[6:]
    print("You are looking for an artist named..." + sqlArtist)

def titleCommandCall(fullCommand):
    sqlTitle = fullCommand[5:]
    print("You are looking for an title named..." + sqlTitle)

def albumCommandCall(fullCommand):
    sqlAlbum = fullCommand[5:]
    print("You are looking for an album named..." + sqlAlbum)

def genreCommandCall(fullCommand):
    sqlGenre = fullCommand[5:]
    print("You are looking for a genre named..." + sqlGenre)

def biggestHitCommandCall(fullCommand):
    sqlBiggestHit = fullCommand[10:]
    print("You are looking for a biggest hit named..." + sqlBiggestHit)

def help():
    print("You may enter: ")
    print("- Album")
    print("- Artist")
    print("- Biggest Hit")
    print("- Genre")
    print("- Title")



main()
