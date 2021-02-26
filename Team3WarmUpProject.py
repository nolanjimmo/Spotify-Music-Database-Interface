# CS205 Team 3 Warm Up Project
# Nolan Jimmo
# Greg Levine
# Echo Norcott
# Delaney Sullivan

# main program holds the interface of the program
import sqlite3
from sqlite3 import Error

##### Branch Differences Explanation######
# I realized that it was going to be really difficult to find a universal sql query structure that we could just plug
# the command1, command2 and desiredData variables into. So for this version I decided to make the decision structure
# within the doubleCommandQuery function, and then just call that function straight from the input validation loop
# that we had previously. I realize this pretty much completely skips over all of the commandCall functions, but it does
# the same thing we intended it to do in less code and to me is a little bit more intuitive to follow if someone else
# where to jump in and work on this in the future. Please let me know if this isn't intuitive at all to you guys and we
# can do it another way!

# the way I have it set up, the queries have to look like this:
# artist, title, album or genre as command1
# then any of the others as command2
# the third user input entry is the name of the first command that they are referencing (Zedd if the first command is
# artist, or Greyhound if the first command is title, and so on)
# when genre is the first command the system will list all of the command2 items that are in that genre (aka all titles
# or albums that are in that genre)
#Examples:
# artists, genre, Alesso
# title, artists, Under Control

# Essentially, the first command is the data that the user specifies, and the second command is what they want in return
# I also had to change to the command "biggest hit" to "biggesthit" because column names in the database don't have
# spaces and I wanted to use the command given by the user as the actual syntax in the SQL in this case.

# There is also a createConnection() function that is basically a loadData() function I just haven't done anything
# with putting it in to the input validation loop or anything yet.


def main():
    cursor = createConnection()
    ##### These are just some test queries that will run automatically to show functionality, but try your own#####
    #doubleCommandQuery('artist', 'genre', "Alesso", cursor)
    #doubleCommandQuery('title', 'artist', 'Under Control', cursor)
    #doubleCommandQuery('artist', 'title', 'Swedish House Mafia', cursor)
    #doubleCommandQuery('artist', 'biggesthit', 'Alesso', cursor)
    #doubleCommandQuery('album', 'artist', 'Clarity', cursor)

    #Change this to be << but this is easier to read while testing
    command = input("Please enter a command: ")

    #splits command into the individual words to see which SQL line to call
    commandList = command.split()
    commandCall = commandList[0]
    commandCall2 = commandList[1]

    #loop for different commands until quit
    while commandCall.lower() != "quit":
        if (commandCall.lower() == "artist" or commandCall.lower() == "title" or commandCall.lower() == "album"
            or commandCall.lower() == "genre") and (commandCall2.lower() == "artist" or commandCall2.lower() == "title" or commandCall2.lower() == "album"
                                                    or commandCall2.lower() == "genre") and (commandCall.lower() != commandCall2.lower()):
            doubleCommandQuery(commandList[0], commandList[1], commandList[2], cursor)
        elif commandCall.lower() == "help":
            help()
        else:
            print("Sorry, your command is not recognized")
            help()

        command = input("Please enter a command: ")
        commandList = command.split()
        commandCall = commandList[0]
        commandCall.lower()


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
    if command1 == "artist" and (command2 == "genre" or command2 == "biggesthit"):
        curs.execute("SELECT %s FROM artists WHERE name = '%s'" % (command2, desiredData))
    elif command1 == "artist" and (command2 == "title" or command2 == "album"):
        curs.execute("SELECT %s FROM %s WHERE artist = '%s'" % (command2, "songs", desiredData))
    elif command1 == "title" and command2 == "artists":
        curs.execute("SELECT %s FROM %s WHERE title = '%s'" % ('artist', 'songs', desiredData))
    elif command1 == "title" and command2 == "album":
        curs.execute("SELECT %s FROM %s WHERE title = '%s'" % (command2, 'songs', desiredData))
    elif command1 == "title" and command2 == "genre":
        curs.execute("SELECT artists.%s FROM artists INNER JOIN songs ON songs.artist = artists.name "
                     "WHERE songs.title = '%s'" % (command2, desiredData))
    elif command1 == "genre" and command2 == "artists":
        curs.execute("SELECT %s FROM %s WHERE genre = '%s'" % ('name', command2, desiredData))
    elif command1 == "genre" and (command2 == "title" or command2 == "album"):
        curs.execute("SELECT %s FROM songs INNER JOIN artists ON songs.artist = artists.name "
                     "WHERE artists.genre = '%s'" % (command2, desiredData))
    elif command1 == "album" and (command2 == "artist" or command2 == "genre"):
        curs.execute("SELECT %s FROM songs WHERE album = '%s'" % (command2, desiredData))
    else:
        print("Command sequence invalid")

    rows = curs.fetchall()
    for row in rows:
        print(row[0])


def help():
    print("You may enter: ")
    print("- Album")
    print("- Artist")
    print("- Biggest Hit")
    print("- Genre")
    print("- Title")



main()
