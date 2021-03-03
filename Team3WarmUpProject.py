# CS205 Team 3 Warm Up Project
# Nolan Jimmo
# Greg Levine
# Echo Norcott
# Delaney Sullivan

# import sql and regular expressions
import re
import sqlite3
from sqlite3 import Error

def main():

    #require the user to load data before they can start using the program
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

    command = input("> ")
    my_SQL_list = []
    #send the command to the parser so it can be sent to the SQL Calls
    my_SQL_list = parser(command)

    #different if statements for the valid commands so they can be properly passed to our call
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
    #catch all for invalid commands
    else:
        command_call = " "
        command_call2 = " "
        desired_data = " "
        command_call3 = None
        desired_data2 = None

    # loop to continue until the user wants to quit
    while command_call.lower() != "quit":

    #making sure that the command is valid before the function is called
        if (command_call.lower() == "artist" or command_call.lower() == "title" or command_call.lower() == "album"
            or command_call.lower() == "genre") and (
                command_call2.lower() == "artist" or command_call2.lower() == "title" or command_call2.lower() == "album"
                or command_call2.lower() == "genre" or command_call2.lower() == "biggesthit") and (command_call.lower() != command_call2.lower()):
            double_command_query(command_call, command_call2, desired_data, command_call3, desired_data2, cursor)
        elif command_call.lower() == "help":
            help()
        else:
            print("Sorry, your command is not recognized")
            help()

        #allow for the looping for the commands
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

#Create the connections for the database for the user to use
def create_connection():
    connection = None
    try:
        connection = sqlite3.connect('SongsArtistsDB.db')
    except Error as e:
        print(e)
    finally:
        if connection:
            return connection.cursor()

#parser takes in the command from the user and returns the list of commands for the SQL Calls
def parser(command):

    #split the command into separate words
    command_list = command.split()

    #list of our keywords for commands
    keywords = ["artist", "title", "biggesthit", "album", "genre"]

    #make a list of any words that are surrounded by ""
    double_word_list = re.findall('"([^"]*)"', command)

    #create empty lists to add to
    list_for_SQL = []
    dupe_list = []
    amount_of_double_words = len(double_word_list)
    list_indexer = 0

    #if there are double words
    if amount_of_double_words > 0:
        #loop through the words in the command list
        for word in command_list:
            #if the word is not a keyword, put it in the duplicate list
            if word not in keywords:
                dupe_list.append(double_word_list[list_indexer])
                #there only ever could be two instances of double words that are valid so it could only go from index 0 to 1
                if amount_of_double_words == 2:
                    list_indexer = 1
            #if the word in command like is not starting or ending with " then add it to the dupe list
            elif word[0] and word[-1] != '"':
                dupe_list.append(word)
            #last chance to add the word
            else:
                dupe_list.append(word)
        #remove any duplicates from the list
        for word in dupe_list:
            if word not in list_for_SQL:
                list_for_SQL.append(word)

    #else means there were no double words so the list works just as is, put it in the final list
    else:
        for word in command_list:
            list_for_SQL.append(word)
    return list_for_SQL

#doubel command query takes in 6 items, desired data is anything data the user can type in, command_call are the keywords
#curs is the connection to the db
#if anything is not needed for that specific call, it is None
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

#help for the user who needs instructions
def help():
    print("You may enter: ")
    print("- album artist Album Name")
    print("- album genre Album Name\n")
    print("- artist genre Artist Name")
    print("- artist biggesthit Artist Name")
    print("- artist song Artist Name")
    print("- artist album Artist Name")
    print("- artist album Artist Name title Song Title\n")
    print("- genre artists Genre")
    print("- genre title Genre")
    print("- genre album Genre\n")
    print("- title artists Song Title")
    print("- title album Song Title")
    print("- title genre Song Title")


main()

