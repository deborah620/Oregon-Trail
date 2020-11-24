"""
File:    proj1.py
Author:  Deborah Miller
Date:    03/24/2020
Section: 14
E-mail:  d169@umbc.edu
Description:
  Game similar to oregon trail
user builds a character and has 
a certain amount of time to reach the ITE building
"""
TAB = "    "
MAX_STEALTH_AND_CHARISMA = 10
START = "The Dorms"
FINISH = "ITE"

def load_map(map_file_name):
    """
    param: given a map file 
    opens the correct map file
    return: the map in a dictionary 
    with the place you are as the key 
    and the places you can go as its value
    """
    
    dict_place = {}
    dict_options = {}
    place = ""
    key_value = ""
    
    with open(map_file_name) as map_use:
        game_map = map_use.readlines()
            
        for line in game_map:

            if "\t" not in line: 
                dict_options = {}
                place = line.strip()
                     
            elif "\t" in line:
                key_value = line.split(",")
                dict_options[key_value[0].strip()] = key_value[1].strip()

            dict_place[place] = dict_options
        
        return dict_place
    

def load_events(event_file_name):
    """
    param: given event file
    opens he correct event file
    return: event in a different format
    """
    
    dict_events = {}
    list_actions = []

    with open(event_file_name) as event_use:    
        events = event_use.readlines()
        
        for line in events:
            word = line.strip().split(",")
            list_actions = []
            
            for i in range(1, len(word)):
                list_actions.append(word[i])
            
            dict_events[word[0]] = list_actions
    
        return dict_events


def play_game(start_time, game_map, events, c_and_s):
    """
    bulk of game is played in here
    param: start time, the game map and events, the character's charisma and stealth
    return: win or lose
    """
    at_now = START
    
    print("You are currently in " + START + " and have " + start_time + " seconds left to get to " + FINISH + ".")
    
    # iterates through the 1st dict and pulls the value for the key the dorm
    # since the value is a 2nd dict it again interates and prints out the 2nd dict (keys and values)
    for places in game_map[at_now]:           

        print(TAB, places, game_map[at_now][places])
                
    go_to = input("Where do you want to go next? ")

    # makes sure user can go there
    check = []
    for places in game_map[at_now]:
            
        while go_to not in game_map[at_now].keys():
            if go_to == FINISH:
                print("Nice try")

            print("That was not one of the options")
            go_to = input("Where do you want to go next? ")
        
    # game play
    while go_to != FINISH:

        # minuses appropriate amount of time from place chosen
        for places in game_map[at_now]:
            if places == go_to:
                start_time = str(int(start_time) - int(game_map[at_now][places]))
                if int(start_time) < 0:
                    return "lose"
                
        # if event at place, print event and see if win or lose 
        # displays appropriate text and minuses time if the user lost
        for key in events:
            if key == go_to:
                value = events[key]
                print(value[0].strip())

                if c_and_s[0] >= int(value[3]) and c_and_s[1] >= int(value[4]):
                    print(TAB, value[1])

                else:
                    print(value[2])
                    print("You lose" + value[5] + " seconds.")

                    start_time = str(int(start_time) - int(value[5]))                  

                if int(start_time) < 0:
                    return "lose"

        # tells player where they currently are and give options for where can go    
        print("You are currently in " + go_to + " and have " + start_time + " seconds left to get to " + FINISH + ".")

        at_now = go_to            
        for places in game_map[at_now]:
            print(TAB, places, game_map[at_now][places])            

        go_to = input("Where do you want to go next? ")

        # makes sure user can go there
        check = []
        for places in game_map[at_now]:

            while go_to not in game_map[at_now].keys():
                if go_to == FINISH:
                    print("Nice try")

                print("That was not one of the options")
                go_to = input("Where do you want to go next? ")
   
    if go_to == FINISH:

        return "win"
    
    else:
        
        return "lose"

def create_characters():
    """
    gets character name, charisma level, and stealth level from the user
    character must have more than one name
    charisma + stealth must equal ten and individually be greater than -1
    """
    list_c_s = []
    
    name = input("What is your name? Enter a first (middle) last separated by spaces, middle being optional. ")

    while " " not in name:
        name = input("What is your name? Enter a first (middle) last separated by spaces, middle being optional. ")

    # get points
    print("You have 10 skill points to distribute, otherwise you aren't going anywhere.")

    charisma = int(input("How charismatic are you, you have 10 skill points left? "))
    points_left = str(MAX_STEALTH_AND_CHARISMA - charisma)
    stealth = int(input("How sneaky are you, you have " + points_left + " skill points left? \
"))

    # if user entered negative points
    while charisma < 0 or stealth < 0:
        print("You have 10 skill points to distribute, they must all be positive.")
        
        charisma = int(input("How charismatic are you, you have 10 skill points left? "))
        points_left = str(MAX_STEALTH_AND_CHARISMA - charisma)
        stealth = int(input("How sneaky are you, you have " + points_left + " skill points left? "))

    # points don't add up to 10
    while charisma + stealth != 10:
        print("You have 10 skill points to distribute, you hear that 10!")

        charisma = int(input("How charismatic are you, you have 10 skill points\
 left? "))
        points_left = str(MAX_STEALTH_AND_CHARISMA - charisma)
        stealth = int(input("How sneaky are you, you have " + points_left + " s\
kill points left? "))
        
    list_c_s.append(charisma)
    list_c_s.append(stealth)

    return list_c_s 
    
if __name__ == "__main__":
    map_file_name = input("What is the map file? ")
    
    event_file_name = input("What is the events file? ")

    start_time = input("How much time do you want to start with? ")

    while int(start_time) < 0:
        print("Automatic loss?" )
        start_time = input("How much time do you want to start with? ")

    win_or_lose = play_game(start_time, load_map(map_file_name), load_events(event_file_name), create_characters()) 
    
    if win_or_lose == "win":
        print("You made it to ITE and now can learn the secrets of computer science.  You win!")

    elif win_or_lose == "lose":
        print("You have run out of time, and so you lose.")
