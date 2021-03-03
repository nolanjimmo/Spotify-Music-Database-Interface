# CS205 Team 3 Warm Up Project
# Nolan Jimmo
# Greg Levine
# Echo Norcott
# Delaney Sullivan

# main program holds the interface of the program
import re
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
# Examples:
# artists, genre, Alesso
# title, artists, Under Control

# Essentially, the first command is the data that the user specifies, and the second command is what they want in return
# I also had to change to the command "biggest hit" to "biggesthit" because column names in the database don't have
# spaces and I wanted to use the command given by the user as the actual syntax in the SQL in this case.

# There is also a createConnection() function that is basically a loadData() function I just haven't done anything
# with putting it in to the input validation loop or anything yet.


def main():
    database_creation = input("Please load the data ")
    while database_creation != "load data":
        database_creation = input("Please load the data ")
    cursor = create_connection()
    ##### These are just some test queries that will run automatically to show functionality, but try your own#####
    # doubleCommandQuery('artist', 'genre', "Alesso", cursor)
    # doubleCommandQuery('artist', 'title', 'Swedish House Mafia', cursor)
    # doubleCommandQuery('artist', 'biggesthit', 'Alesso', cursor)
    # doubleCommandQuery('album', 'artist', 'Clarity', cursor)

    # example for a double command "artist album Zedd title Spectrum"
    ##EXAMPLE COMMANDS
    # > artist album Zedd title Spectrum
    # Clarity
    # > artist genre Alesso
    # Progessive House

    # Change this to be << but this is easier to read while testing
    command = input("> ")
    my_SQL_list = []
    my_SQL_list = parser(command)

    if len(my_SQL_list) == 1:
        command_call = my_SQL_list[0]
        command_call2 = " "
        desired_data = None
        command_call3 = None
        desired_data2 = None
    elif len(my_SQL_list) == 3:
        command_call = my_SQL_list[0]
        command_call2 = my_SQL_list[1]
        desired_data = my_SQL_list[2]
        command_call3 = None
        desired_data2 = None
    elif len(my_SQL_list) == 5:
        command_call = my_SQL_list[0]
        command_call2 = my_SQL_list[1]
        desired_data = my_SQL_list[2]
        command_call3 = my_SQL_list[3]
        desired_data2 = my_SQL_list[4]
    else:
        command_call = " "
        command_call2 = " "
        desired_data = " "
        command_call3 = None
        desired_data2 = None
    # loop for different commands until quit
    while command_call.lower() != "quit":
        print("Command 1 = " + command_call)

        if command_call2 == None:
            print("Command 2 = None")
        else:
            print("Command 2 = " + command_call2)

        if desired_data == None:
            print("Desired Data = None")
        else:
            print("Desired Data = " + desired_data)

        if command_call3 == None:
            print("Command 3 = None")
        else:
            print("Command 3 = " + command_call3)

        if desired_data2 == None:
            print("Desired Data 2 = None")
        else:
            print("Desired Data 2 = " + desired_data2)

        if (command_call.lower() == "artist" or command_call.lower() == "title" or command_call.lower() == "album"
            or command_call.lower() == "genre") and (
                command_call2.lower() == "artist" or command_call2.lower() == "title" or command_call2.lower() == "album"
                or command_call2.lower() == "genre") and (command_call.lower() != command_call2.lower()):
            double_command_query(command_call, command_call2, desired_data, command_call3, desired_data2, cursor)
        elif command_call.lower() == "help":
            help()
        else:
            print("Sorry, your command is not recognized")
            help()

        command = input("> ")
        my_SQL_list = []
        my_SQL_list = parser(command)

        if len(my_SQL_list) == 1:
            command_call = my_SQL_list[0]
            command_call2 = " "
            desired_data = None
            command_call3 = None
            desired_data2 = None
        elif len(my_SQL_list) == 3:
            command_call = my_SQL_list[0]
            command_call2 = my_SQL_list[1]
            desired_data = my_SQL_list[2]
            command_call3 = None
            desired_data2 = None
        elif len(my_SQL_list) == 5:
            command_call = my_SQL_list[0]
            command_call2 = my_SQL_list[1]
            desired_data = my_SQL_list[2]
            command_call3 = my_SQL_list[3]
            desired_data2 = my_SQL_list[4]
        else:
            command_call = " "
            command_call2 = " "
            desired_data = " "
            command_call3 = None
            desired_data2 = None



##########Database Interaction#########################

# alternate way to access the database using a single and double command query
# I am going to comment out the connection to the database right now so we don't get any messy errors when we run for now
def create_connection():
    connection = None
    try:
        connection = sqlite3.connect('SongsArtistsDB.db')
    except Error as e:
        print(e)
    finally:
        if connection:
            return connection.cursor()

def parser(command):
    command_list = command.split()

    keywords = ["artist", "title", "biggesthit", "album", "genre"]

    double_word_list = re.findall('"([^"]*)"', command)

    list_for_SQL = []
    dupe_list = []
    amount_of_double_words = len(double_word_list)
    list_indexer = 0
    if amount_of_double_words > 0:
        for word in command_list:
            if word not in keywords:
                dupe_list.append(double_word_list[list_indexer])
                if amount_of_double_words == 2:
                    list_indexer = 1
            elif word[0] and word[-1] != '"':
                dupe_list.append(word)
            else:
                dupe_list.append(word)
        for word in dupe_list:
            if word not in list_for_SQL:
                list_for_SQL.append(word)

    else:
        for word in command_list:
            list_for_SQL.append(word)
    return list_for_SQL


def double_command_query(command1, command2, desired_data, command3, desired_data2, curs):
    if command1 == "artist" and (command2 == "genre" or command2 == "biggesthit"):
        curs.execute("SELECT %s FROM artists WHERE name = '%s'" % (command2, desired_data))
    elif command1 == "artist" and (command2 == "title" or command2 == "album"):
        if command3 is not None:
            curs.execute("SELECT %s FROM %s WHERE %s = '%s' AND %s = '%s'"
                         % (command2, "songs", command1, desired_data, command3, desired_data2))
        else:
            curs.execute("SELECT %s FROM %s WHERE artist = '%s'" % (command2, "songs", desired_data))
    elif command1 == "title" and command2 == "artists":
        curs.execute("SELECT %s FROM %s WHERE title = '%s'" % ('artist', 'songs', desired_data))
    elif command1 == "title" and command2 == "album":
        curs.execute("SELECT %s FROM %s WHERE title = '%s'" % (command2, 'songs', desired_data))
    elif command1 == "title" and command2 == "genre":
        curs.execute("SELECT artists.%s FROM artists INNER JOIN songs ON songs.artist = artists.name "
                     "WHERE songs.title = '%s'" % (command2, desired_data))
    elif command1 == "genre" and command2 == "artists":
        curs.execute("SELECT %s FROM %s WHERE genre = '%s'" % ('name', command2, desired_data))
    elif command1 == "genre" and (command2 == "title" or command2 == "album"):
        curs.execute("SELECT %s FROM songs INNER JOIN artists ON songs.artist = artists.name "
                     "WHERE artists.genre = '%s'" % (command2, desired_data))
    elif command1 == "album" and (command2 == "artist" or command2 == "genre"):
        curs.execute("SELECT %s FROM songs WHERE album = '%s'" % (command2, desired_data))
    else:
        print("Command sequence invalid")

    rows = curs.fetchall()
    for row in rows:
        print(row[0])


def help():
    print("You may enter: ")
    print("- album artist Album Name")
    print("- album genre Album Name\n")
    print("- artist genre Artist Name")
    print("- artist biggesthit Artist Name")
    print("- artist song Artist Name")
    print("- artist album Artist Name\n")
    print("- genre artists Genre")
    print("- genre title Genre")
    print("- genre album Genre\n")
    print("- title artists Song Title")
    print("- title album Song Title")
    print("- title genre Song Title")


main()

