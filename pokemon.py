
import csv
import os
import random
import math

catch_candy = [3, 5, 10]


def get_memory():
    memory = []
    with open(str(pname) + '.csv', 'r', newline='') as playerfile:
        for i in list(playerfile):
            memory.append(i.rstrip().split(','))
    return memory


def write_memory(memory):
    """Writes the player's user data to a file for later use."""
    with open(str(pname) + '.csv', 'w', newline='') as playerfile:
        writer = csv.writer(playerfile, delimiter=',')
        for i in memory:
            writer.writerow(i)


def add_player(name):
    """Takes a (string) name and creates a csv file with that name. It is initally empty except for the column headers associated with pokemon."""
    with open(str(name) + '.csv', 'w', newline='') as playerfile:
        writer = csv.writer(playerfile, delimiter=',')
        entry = ['Species', 'Level', 'CP', 'Name', 'Candy:', 0]
        writer.writerow(entry)


def add_pokemon(name, species, level, cp):
    """Takes (string) name and species, and (int) level and cp for the pokemon the user wants to add. This data is then formatted and written in the current player's pokemon file"""
    with open(str(pname) + '.csv', 'a', newline='') as playerfile:
        writer = csv.writer(playerfile, delimiter=',')
        entry = [species, level, cp, name]
        writer.writerow(entry)


def del_pokemon(pmon):
    """Takes arguments of pmon, looks at all pokemon for the same string and name, shows all potential candidates, takes input from user to know which one to delete. When done, it rewrites user table."""
    memory = get_memory()
    for i in memory:
        if i==pmon:
            kill=(memory.index(i))
    memory.pop(kill)
    write_memory(memory)

def switch_player():
    """Looks at csv files in the home directory that have usernames as their titles. The user is shown names and then if they select a name that has a csv file, the pname variable is changed."""
    players = []
    print("Here are the existing players: \n")
    for i in os.listdir():
        if i[-3:] == 'csv' and i[:-4] != 'Wildmons':
            print(i[0:-4])
            players.append(i[0:-4])
    possible = input('\nWhat is the name of the user you are selecting: ')
    for i in players:
        if possible == i:
            return i
    print('{} is not an existing user.'.format(possible))
    print('They have been added as a new user.')
    add_player(possible)
    return possible


def select_pokemon():
    """Asks player what pokemon they would like to choose and returns that pokemon's list entry."""
    memory = get_memory()
    s_list = []
    for i in memory:
        if memory.index(i) != 0:
            s_list.append([[memory.index(i)]+create(i)])
    if memory[0] == memory[-1]:
        print('Go out and catch something!')
        print('-' * 50)
    else:
      s_list_top = []
      s_list_bot = []
      for i in s_list:
          s_list_top.append(i[0][0:2])
          s_list_bot.append(i[0][2:])
      graph_it(s_list_top, s_list_bot)
      chosen = int(input('What is the number of the Pokemon you would like to select: '))
      try:
        return memory[chosen]
      except:
        print('Invalid entry, please enter an integer')


def candy_add(cta):
    """This function takes an (int) argument for the number of candies to add to the player profile."""
    memory = get_memory()
    # finds updated candy
    curr_candy = int(memory[0][-1])
    new_candy = curr_candy + cta
    if new_candy < 0:
        print('You do not have enough candies. Catch a pokemon to get more')
        return
    memory[0][-1] = new_candy
    write_memory(memory)


def catch_pokemon():
    """Generates a random pokemon and allows the user to catch and name it before it is added to the users storage"""
    with open('Wildmons.csv', 'r', newline='') as infile:
        memory = []
        for i in list(infile):
            memory.append(i.rstrip().split(','))
        memory.pop(0)
        ind = int(memory[random.randint(0, len(memory)-2)][0])
        species = memory[ind][1]
        cp = random.randint(int(memory[ind][-2]), int(memory[ind][-1]))
        level = random.randint(1, 5)
        # minigame
        free = True
        secret = random.randint(0, 100)
        print('A wild {} has appeared!'.format(species))
        while free:
            curr = int(input('Enter a strength to throw the pokeball (0-100)'))
            if curr == secret:
                free = False
                print('You caught it!')
            elif curr < secret:
                print('Throw harder!')
            else:
                print('Throw softer!')
        catch = input('Would you like to catch the {} (enter y): '.format(species))
        if catch != 'y':
          return
        tname = input('What would you like to name the {}: '.format(species))
        add_pokemon(tname, species, level, cp)
        candy_add(catch_candy[random.randint(0, 2)])
        print('{} has been added to your storage!'.format(tname))


def power_up(ipmon):
    """Levels up the pokemon if you have enough candy; if not, it will go on to the next action. Will also not work if the pokemon is at its max level."""
    curr_candy = int((get_memory())[0][-1])
    if int(ipmon[1]) < 30 and curr_candy > 1:
        candy_add(-1)
        add_cp(ipmon)
        print('You have sucessfully leveled up {}.'.format(ipmon[-1]))
    elif curr_candy < 1:
        print('You need more candy')
    elif int(ipmon[1]) < 40 and curr_candy > 2:
        candy_add(-2)
        add_cp(ipmon)
        print('You have sucessfully leveled up {}.'.format(ipmon[-1]))
    elif curr_candy < 2:
        print('You need more candy')
    else:
        print('The pokemon is at max level')


def add_cp(ipmon):
    """Contains the algorithm for leveling up a pokemon, and writes that to the user file."""
    curr = 1
    memory = get_memory()
    for i in memory:
        if i == ipmon:
            curr = memory.index(i)
    loaded_mon = memory[curr]
    level = int(loaded_mon[1])
    cp = int(loaded_mon[2])
    if int(ipmon[1]) > 30:
        memory[curr][2] = int(cp * 0.0094 / (0.095 * math.sqrt(level))) + cp
    elif int(ipmon[1]) <= 30:
        memory[curr][2] = int(cp * 0.0045 / (0.095 * math.sqrt(level))) + cp
    memory[curr][1] = str(int(memory[curr][1]) + 1)
    write_memory(memory)

def battle(pmon):
  with open('Wildmons.csv', 'r', newline='') as infile:
        memory = []
        for i in list(infile):
            memory.append(i.rstrip().split(','))
        memory.pop(0)
        ind = int(memory[random.randint(0, len(memory)-1)][0])
        species = memory[ind][1]
        cp = random.randint(int(memory[ind][-2]), int(memory[ind][-1]))
        level = random.randint(1, 20)
        print('A level {} {} has appeared'.format(level,species))
        yes = input('Would you like to fight it? (enter y)')
        if yes != 'y':
          return
        playerCP = int(pmon[2])*math.sqrt(int(pmon[1]))+random.randint(-50,50)
        oppCP = cp*math.sqrt(level)+random.randint(-50,50)
        print('Your strength is {:.2f} and your opponent''s strength is {:.2f}'.format(playerCP,oppCP) )
        if playerCP > oppCP:
          print('You won! Your pokemon has been leveled up')
          add_cp(pmon)
        else:
          print('You lost. You have lost two candies.')
          candy_add(-2)
        print('-'*50)


def create(pokemon):
    """Takes input of a pokemon in list form, then formats that for use in grapher"""
    l1 = '{} the {}'.format(pokemon[3], pokemon[0])
    l2 = 'Level: {} '.format(pokemon[1])
    l3 = 'CP: {}'.format(pokemon[2])
    return [l1, l2, l3]


def print_lines(data):
    counter = 0
    for i in data:
        for j in i:
            print('{} {}'.format(j[0], j[1]).center(30), end='')
            counter += 1
        print('')


def graph_it(l1,l2):
    l3 = []
    x = len(l1)
    if x%3 == 0:
        num_rows = x//3
    else:
        num_rows = x//3 + 1
    counter = 0
    while counter != num_rows:
        l3.append(l1[counter*3:(counter+1)*3])
        l3.append(l2[counter*3:(counter+1)*3])
        counter += 1
    print_lines(l3)


def fdo(num1,num2,text,ext):
    exit = 0
    while exit == 0:
      try:
        var = input('\n'+text)
        if var=='exit':
          exit=1
        elif int(var) >= num1 and int(var) <= num2:
          exit = 1
        else:
          exit = int('throw error')
      except ValueError:
        print('You must enter a number from the given range.')
    return(var)

#define variables
do_next = 'f'
pmon = ''

#A 'log-in' page
print('Welcome to Pokemon!\n')
print('1- Open an existing account')
print('2- Add a new account')
do_next = fdo(1,2,'What would you like to do: ',0)
print('-'*50)
#Actions for login
if do_next == '1':
    pname = switch_player()
elif do_next == '2':
    pname = input('What would you like to name your new player: ')
    add_player(pname)
print('-'*50)

#Main program loop
while do_next != 'exit':
    memory = get_memory()
    print('Pokemon!\n')
    print('Welcome {}!'.format(pname))
    curr_candy = int(memory[0][-1])
    print('You have {} candies\n'.format(curr_candy))
    print('1- Catch a Pokemon')
    print('2- Select a Pokemon')
    print('3- Change or Add an account')
    do_next = fdo(1,3,'What would you like to do (type exit to exit):',1)
    print('-'*50)
    #Catch pokemon
    if do_next == '1':
        catch_pokemon()
        print('-' * 50)
    #Select pokemon
    elif do_next == '2':
        pmon = select_pokemon()
        if pmon != None:
            print('-' * 50)
            print('1- Power-up {}'.format(pmon[3]))
            print('2- Delete {}'.format(pmon[3]))
            print('3- Battle {}'.format(pmon[3]))
            print('4- Go to the main menu\n')
            do_next = fdo(1,4,'What would you like to do: ',0)
            if do_next == '1':
                power_up(pmon)
            elif do_next == '2':
                del_pokemon(pmon)
            elif do_next == '3':
                battle(pmon)
    #Account management
    elif do_next == '3':
        pmon = ''
        print('1- Change your account')
        print('2- Add an account')
        do_next = fdo(1,2,'What would you like to do: ',0)
        print('-' * 50)
        if do_next == '1':
            pname = switch_player()
            print('-' * 50)
        elif do_next == '2':
            pname = input('What would you like to name your new player: ')
            print('-' * 50)
            add_player(pname)
