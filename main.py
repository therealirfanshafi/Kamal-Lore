"""
This is the main program for the game
This file mainly uses modules buit in other files
However this file also has some module and class definitions as it would be more suitable to have those directly in the main file
"""
# import of the standard program libraries
import pygame
import os
import sys

root = os.path.dirname(__file__)   # gets the absolute path of the current file

sys.path.insert(0, os.path.join(root, "Assets"))  # adds the Assets folder to the path

# import of my written modules 
from boss import Boss
from fight_dialogue import FightDialouge
from button_mash import ButtonMash
from bar_timing import BarTiming
from rythm import Rythm
from display_health_and_energy import display_health_and_energy
from shop import shop
from game_dance import GameOrDance
from opening import opening
from display_health_and_energy import display_health_and_energy
from ending import ending

pygame.init() 

# sets the screen resolution, titile and icon
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Kamal Lore")

clock = pygame.time.Clock()  # used for maintenance of constant FPS

def main_menu():  # module to display the main menu
    global running  # global varialble used in the main game loop

    #loads the different fonts of the menue 
    font_title = pygame.font.Font("freesansbold.ttf", 64)
    font_option = pygame.font.Font("freesansbold.ttf", 32)  
    title = font_title.render("KAMAL LORE", True, (255, 255, 255))  # game title
    
    # this try - except block checks if the save file exists or not, thus determining whether this is the first time playing the game or not
    try:
        save_file = open(os.path.join(root, "Assets/Save Data/save_file.txt"), "r")
        save_file.close()
        first_time = False
    except FileNotFoundError:
        first_time = True
    
    option = 0  # initialisation of the option variable 
    running = True

    # loads and plays the music
    pygame.mixer.music.load(os.path.join(root, "Assets/Music/Halo Theme Song Original.mp3"))
    pygame.mixer.music.play()

    while running:  # main loop of the menu
        screen.fill((0, 0, 0))
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:  # checks for key press
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    option += 1  # moves to the option below 
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    option -= 1  # moves to the option above
                elif event.key == pygame.K_RETURN:
                    if option == 2:  # quits game if enter is pressed on the option 2 (QUIT)
                        running = False
                    pygame.mixer.music.stop()
                    return option
        if first_time:
            # makes sure that the options are 1 and 2 only if the game is loaded for the first time
            if option < 1:
                option = 2
            if option > 2:
                option = 1 
            continue_game = font_option.render("Continue Game", True, (100, 100 , 100))  # displays continue game in grey as there is nowehre to continue from
            if option == 1:  # yellows the text on which the current option is on
                new_game = font_option.render("New Game", True, (255, 255, 0))
                quit_game = font_option.render("Quit Game", True, (255, 255, 255))
            elif option == 2:
                new_game = font_option.render("New Game", True, (255, 255, 255))
                quit_game = font_option.render("Quit Game", True, (255, 255, 0))
        else:  # similar logic to first time, except continue game is also a selectable option
            if option < 0:
                option = 2
            if option > 2:
                option = 0
            if option == 0:
                continue_game = font_option.render("Continue Game", True, (255, 255 , 0))
                new_game = font_option.render("New Game", True, (255, 255, 255))
                quit_game = font_option.render("Quit Game", True, (255, 255, 255))
            elif option == 1:
                continue_game = font_option.render("Continue Game", True, (255, 255 , 255))
                new_game = font_option.render("New Game", True, (255, 255, 0))
                quit_game = font_option.render("Quit Game", True, (255, 255, 255))
            elif option == 2:
                continue_game = font_option.render("Continue Game", True, (255, 255 , 255))
                new_game = font_option.render("New Game", True, (255, 255, 255))
                quit_game = font_option.render("Quit Game", True, (255, 255, 0))

        # draws everything on the screen
        screen.blit(title, (175, 40))
        screen.blit(continue_game, (200, 140))
        screen.blit(new_game, (200, 200))
        screen.blit(quit_game, (200, 260))
        pygame.display.update()

class Player:  # player class to encapsulate all info related to the player
    def __init__(self, current_health, max_health, def_factor, heal_factor, energy):
        self.current_health = current_health 
        self.max_health = max_health
        self.def_factor = def_factor
        self.heal_factor = heal_factor
        self.energy = energy
        self.playerX = 400  # default player coordinates
        self.playerY = 300
        self.speed = 5  # movement speed when movement keys are pressed
        self.image = pygame.transform.scale_by(pygame.image.load(os.path.join(root, "Assets/Images/Kamal.png")), 0.25)  # player image

    def movment(self):  # method to allow player movement
        keys = pygame.key.get_pressed()  # dictionary holding keys which are pressed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:  # moves in the direction according to key press
            self.playerX -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.playerX += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.playerY -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.playerY += self.speed

def read_save_data():  # function to read the data from the save file
    with open(os.path.join(root, "Assets/Save Data/save_file.txt"), "r") as save_file:
        line1 = int(save_file.readline())
        line2 = float(save_file.readline())
        line3 = int(save_file.readline())
        line4 = float(save_file.readline())
        line5 = int(save_file.readline())
        line6 = int(save_file.readline())
        return line1, line2, line3, line4, line5, line6

def write_save_data():
    with open(os.path.join(root, "Assets/Save Data/save_file.txt"), "w") as save_file:
        save_file.writelines(map(lambda x: str(x) +"\n", [game_state, kamal.current_health, kamal.max_health, kamal.def_factor, kamal.heal_factor, kamal.energy]))

def pause_menu():  # pressing escape on any room calls this menu
    global running
    font = pygame.font.Font("freesansbold.ttf", 32)
    option = 0
    while running:
        clock.tick(30)  # maintenance of FPS
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:  # allows to choose between options
                    option += 1  
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    option -= 1 
                elif event.key == pygame.K_RETURN:
                    if option == 1:  # quits game if option 1 is selected
                        running = False
                    return  # otherwise simply returns to back to game
    
        # ensures options stay between 0 and 1
        if option < 0:
            option = 1
        elif option > 1:
            option = 0

        if option == 0:  # yellows selected text
            resume = font.render("Resume Game", True, (255, 255, 0))
            quit_game = font.render("Quit Game", True, (255, 255, 255))
        elif option == 1:
            resume = font.render("Resume Game", True, (255, 255, 255))
            quit_game = font.render("Quit Game", True, (255, 255, 0))
        screen.blit(resume, (200, 140))
        screen.blit(quit_game, (200, 200))
        pygame.display.update()



def generic_menu(text):  # simple menu which opens for interaction, takes a parameter of heading word to use in simple menu
    global generic_menu_open
    global generic_option
    
    # loads, draws and renders the text of the heading and background of the image
    menu = pygame.image.load(os.path.join(root, "Assets/Images/generic_menu.png"))
    screen.blit(menu, (0, 500))
    font = pygame.font.Font("freesansbold.ttf", 16)
    heading = font.render(text, True, (255, 255, 255))

    if generic_option < 0:  # ensures that the options of the menu stay between 0 and 1
        generic_option = 1
    elif generic_option > 1:
        generic_option = 0

    if generic_option == 0:  # yellows the required text based on the option selected
        yes = font.render("Yes", True, (255, 255, 0))
        no = font.render("No", True, (255, 255, 255))
    elif generic_option == 1:
        yes = font.render("Yes", True, (255, 255, 255))
        no = font.render("No", True, (255, 255, 0))

    # draws the text in the menu    
    screen.blit(heading, (5, 520))
    screen.blit(yes, (20, 540))
    screen.blit(no, (20, 560))

def central_room(player):  # the main cross road room in which the player starts in
    global central_room_flag
    global room
    global pause_menu_opened
    global shop_visited
    screen.fill((0, 0, 0))

    for event in pygame.event.get():  # allows pausing
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_menu_opened = True
                    pause_menu()
    screen.blit(central_room_background, (0, 0))  # draws the background
    screen.blit(player.image, (player.playerX, player.playerY))  # draws the player

    if (player.playerY < 150 or player.playerY > 250) and not central_room_flag:  # implements room boundaries. Flag is required to detect whether the interesction of the crossroad has been crossed or not. Rather difficult to explain how it works
        if player.playerX < 300:
            player.playerX = 300
        elif player.playerX > 400:
            player.playerX = 400
    elif player.playerX < 300 or player.playerX > 400:
        central_room_flag = True
        if player.playerY < 150:
            player.playerY = 150
        elif player.playerY > 250:
            player.playerY = 250
    else:
        central_room_flag = False
    
    if player.playerX < -50:  # allows movement to other rooms
        room = 1
        player.playerX = 740
    if player.playerY > 500:
        room = 2
        player.playerY = 300
        player.playerX = 610
    if player.playerY < -80:
        shop_visited = True
        pygame.mixer.music.stop()
        shop(player)  # calls the shop module if the upper road is used
        pygame.mixer.music.load(os.path.join(root, "Assets/Music/Deltarune OST_ 13 - Field of Hopes and Dreams.mp3"))  # music is stopped and restarted
        pygame.mixer.music.play(-1)
        player.playerY = -20  # the player is moved slightly below the topmost road after exiting the shop
    
    if player.playerX > 740:
        room = 3
        player.playerX = -50 

def home(player):  # the home room, very similar to how central room works. Difference is explained using comments
    global generic_menu_open
    global generic_option
    global room
    global gamed
    
    screen.blit(home_background, (0, 0))  
    screen.blit(player.image, (player.playerX, player.playerY))
    if player.playerY > 300:  
        player.playerY = 300
    if player.playerY < 150:
        player.playerY = 150
    if player.playerX < 0:
        player.playerX = 0

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if generic_menu_open and event.key == pygame.K_RETURN:  # checks if the generic menu is opened
                if generic_option == 0:  # creates a game/dance object in mode "g" and executes it if "YES" is selected
                    if player.current_health > 1:  # allows gaming only if enough health is there
                        gamed = True
                        game = GameOrDance(player.current_health, player.max_health, player.heal_factor, "g")
                        pygame.mixer.music.stop()
                        result = game.execute()

                        pygame.mixer.music.load(os.path.join(root, "Assets/Music/Deltarune OST_ 13 - Field of Hopes and Dreams.mp3"))
                        pygame.mixer.music.play(-1)

                        player.energy += result[0]  # updates health and energy according to the return values
                        player.current_health = result[1]
                    generic_menu_open = False  # closes the menu
                if generic_option == 1:  # simply cloes menu if "No" is selected
                    generic_menu_open = False
    
            elif event.key == pygame.K_RETURN and player.playerY >= 300:  # if eneter is pressed near to the couch without the generic menu open, the generic menu is opened
                generic_menu_open = True
            elif generic_menu_open and event.key == pygame.K_UP or event.key == pygame.K_w:  # moves between the options
                generic_option -= 1
            elif generic_menu_open and event.key == pygame.K_DOWN or event.key == pygame.K_s:
                generic_option += 1
            elif event.key == pygame.K_ESCAPE:
                    pause_menu()
    if generic_menu_open:
        generic_menu("Game?")  # calls genenirc menu with the heading "game" if the flag is set to True
    
    if player.playerX > 740:
        room = 0
        player.playerX = -50

def club(player):  # no difference from the previous room, just the fact that this time dance is used instead of game
    global generic_menu_open
    global generic_option
    global room
    global danced

    for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and generic_menu_open:
                    if generic_option == 0:
                        generic_menu_open = False
                        if player.current_health > 5:
                            danced = True
                            dance = GameOrDance(player.current_health, player.max_health, player.heal_factor, "d")
                            pygame.mixer.music.stop()
                            result = dance.execute()

                            pygame.mixer.music.load(os.path.join(root, "Assets/Music/Deltarune OST_ 13 - Field of Hopes and Dreams.mp3"))
                            pygame.mixer.music.play(-1)

                            player.energy += result[0]
                            player.current_health = result[1]
                
                    elif generic_option == 1:
                        generic_menu_open = False
                
                elif event.key == pygame.K_RETURN and player.playerX <= 250:

                    generic_menu_open = True
                   
                
                elif event.key == pygame.K_UP or event.key == pygame.K_w and generic_menu_open:
                    generic_option -= 1
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s and generic_menu_open:
                    generic_option += 1
                elif event.key == pygame.K_ESCAPE:
                    pause_menu()
    
    screen.blit(club_background, (0, 0))
    screen.blit(player.image, (player.playerX, player.playerY))
    screen.blit(dance_floor, (0, 300))

    if player.playerY > 390:
        player.playerY = 390
    if player.playerY < 290:
        player.playerY = 290
    if player.playerX < 250:
        player.playerX = 250
    if player.playerX > 690:
        player.playerX = 690

    if generic_menu_open:
        generic_menu("Dance?")
    
    if player.playerX >= 605 and player.playerX <= 630 and player.playerY <= 290:
        room = 0
        player.playerY = 500

def boss_room(player):  # room where boss is fought
    global generic_menu_open
    global generic_option
    global room
    global game_state
    global running

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and generic_menu_open:
                if generic_option == 0:
                    generic_menu_open = False
                    if game_state == 0:  # uses the game state variable to determine which boss should be loaded
                        boss = Boss(pygame.transform.scale_by(pygame.image.load(os.path.join(root, "Assets/Images/NPC Black and White.png")), 0.55), npc_music, (1 - player.def_factor) * 0.5, player.current_health, player.max_health, player.heal_factor, 
                        FightDialouge("Welcome"),
                        FightDialouge("I am the NPC who has been guiding you along your path so far"),
                        FightDialouge("Didn't expect me, did you?"),
                        FightDialouge("Why am I helping you? Don't ask"),
                        FightDialouge("It seems like the creator of the game ran out of ideas of people he could use for the tutorial"),
                        FightDialouge("So here I am"),
                        FightDialouge("All this introduction aside, I will be showing you how to fight back against your enemies"),
                        FightDialouge("Let's begin with the most common and possibly the most difficult attack, rythm"),
                        FightDialouge("For this you have to press the arrow key corressponding to the arrow on the screen when the arrow on the screen is at the highlighted position at the bottom"),
                        FightDialouge("Say for example if the up arrow is at the bottom highlighted position at a moment, you have to press the up arrow then"),
                        FightDialouge("Pressing the key when it is within 50% of the highlighted zone will result in no loss of health"),
                        FightDialouge("Pressing the key when it is within 25% of the highlighted zone will result in gain of health by your current heal factor"),
                        FightDialouge("Pressing the arrow at the wrong time or not pressing the arrow at all will result in loss of health"),
                        FightDialouge("Wow that was some lengthy explanation"),
                        FightDialouge("Well lets see how much you understood"),
                        FightDialouge("I'll go easy on you"),
                        FightDialouge("Here I go"),
                        Rythm([['up', 150, False], ['right', 210, False], ['down', 390, False], ['left', 500, False], ['right', 600, False], ['up', 900, False], ['left', 1000, False], ['right', 1110, False], ['down', 1400, False], ['up', 1470, False], ['right', 1570, False], ['up', 1930, False], ['down', 2020, False], ['right', 2100, False], ['down', 2410, False], ['up', 2510, False], ['left', 2600, False]], 10),
                        FightDialouge("Good job (well actually I don't know if you did)"),
                        FightDialouge("(Mainly because the creator was too lazy to add some conditional logic to test for sucess)"),
                        FightDialouge("Now for our next attack, it is a bar timing attack"),
                        FightDialouge("A white bar will move accross the bottom"),
                        FightDialouge("You have to press space when the white bar is in the green area"),
                        FightDialouge("Pressing it in the green area will cause increase in health, blue causes no damage to be taken, and red causes health decrement"),
                        FightDialouge("Ready? Let's go"),
                        BarTiming(20, 5),
                        FightDialouge("All right lets move to our last attack"),
                        FightDialouge("You have seen this attack before, its the button mash attack from the dancing part"),
                        FightDialouge("As such I wont be going into an explanation, lets just test it out shall we"),
                        ButtonMash(650, 1, 10, 10000),
                        FightDialouge("All right you have completed the tutorial, let's see how well you fare against the real bosses"))
        
                    elif game_state == 1:
                        boss = Boss(pygame.transform.scale_by(pygame.image.load(os.path.join(root, "Assets/Images/Jiraya Black and White.png")), 0.5), jiraya_music, (1-player.def_factor) * 1.1, player.current_health, player.max_health, player.heal_factor,
                        Rythm([['up', 3020, False], ['right', 3185, False], ['down', 3365, False], ['left', 3575, False], ['up', 3755, False], ['right', 3965, False], ['up', 4175, False], ['down', 4325, False], ['right', 4535, False], ['left', 4715, False], ['down', 4910, False], ['up', 5090, False], ['right', 5285, False], ['left', 5435, False], ['right', 5660, False], ['left', 5750, False], ['up', 6065, False], ['down', 6275, False], ['right', 6455, False], ['right', 6545, False], ['left', 6740, False], ['up', 6890, False], ['down', 7085, False], ['up', 7220, False], ['down', 7400, False], ['right', 7565, False], ['left', 7760, False], ['up', 7940, False], ['down', 8150, False], ['right', 8405, False], ['left', 8510, False], ['right', 8750, False], ['left', 8855, False]], 15),
                        FightDialouge("It was fun messing around while we could, but its time to end you with my [ Insert Naruto Reference Here ]"),
                        ButtonMash(600, 1, 10, 10000),
                        FightDialouge("Damn how did you avoid my [ Re-insert Naruto Reference Here]"),
                        FightDialouge("Wait lemme [jiraya thing] to regain energy"),
                        FightDialouge("Ok time to fight again"),
                        Rythm([['up', 3080, False], ['right', 3200, False], ['down', 3305, False], ['up', 3395, False], ['left', 3605, False], ['right', 3710, False], ['left', 3935, False], ['right', 3980, False], ['left', 4025, False], ['up', 4310, False], ['down', 4445, False], ['right', 4640, False], ['left', 4805, False], ['up', 4940, False], ['down', 5015, False], ['right', 5150, False], ['down', 5210, False], ['left', 5255, False], ['up', 5465, False], ['right', 5615, False], ['left', 5765, False], ['down', 5930, False], ['left', 6140, False], ['right', 6290, False], ['left', 6365, False], ['right', 6425, False], ['down', 6665, False], ['up', 6785, False], ['down', 7085, False], ['right', 7130, False], ['left', 7160, False], ['up', 7340, False], ['down', 7520, False], ['right', 7700, False], ['left', 7850, False], ['up', 7925, False], ['down', 8045, False], ['right', 8135, False], ['left', 8225, False], ['up', 8315, False], ['down', 8465, False], ['right', 8585, False], ['left', 8660, False], ['right', 8810, False]], 15),
                        BarTiming(20, 5),
                        FightDialouge("Oh no, thats the end, I couldn't even do the Kamehama"),
                        FightDialouge("Wait my bad that's Dragon Ball"),
                        FightDialouge("Wait, you didnt betray me? Oh I guess i understood wrong") )
            
                    elif game_state == 2:
                        boss = Boss(pygame.transform.scale_by(pygame.image.load(os.path.join(root, "Assets/Images/pitbull Black and White.png")), 0.6), pitbull_music, (1 - player.def_factor) * 3, player.current_health, player.max_health, player.heal_factor, 
                        Rythm([['up', 3660, False], ['right', 3760, False], ['down', 3920, False], ['up', 4060, False], ['right', 4340, False], ['left', 4420, False], ['down', 4760, False], ['up', 4960, False], ['right', 5180, False], ['down', 5380, False], ['left', 5820, False], ['up', 5960, False], ['right', 6300, False], ['up', 6820, False], ['right', 7300, False], ['left', 7440, False], ['down', 7680, False], ['up', 7920, False], ['left', 8100, False], ['right', 8280, False], ['up', 8420, False], ['down', 8760, False], ['right', 8940, False], ['left', 9040, False], ['up', 9160, False], ['down', 9440, False], ['right', 9520, False], ['up', 9720, False], ['down', 9940, False], ['right', 10080, False], ['up', 10280, False], ['down', 10420, False], ['right', 10700, False], ['left', 10880, False], ['up', 11040, False], ['left', 11160, False], ['down', 11340, False], ['right', 11540, False], ['up', 11640, False], ['right', 12300, False], ['down', 12720, False]], 20),
                        FightDialouge("I thought I was Mr Worldwide, but seems like you tell the world lies."),
                        FightDialouge("How could you betray the gang, it was perfect"),
                        BarTiming(20, 10),
                        BarTiming(20, 15),
                        FightDialouge("Were all the times we rapped together fake?"),
                        Rythm([['up', 1140, False], ['right', 1260, False], ['down', 1460, False], ['up', 1620, False], ['left', 1720, False], ['right', 1840, False], ['up', 1980, False], ['left', 2160, False], ['down', 2300, False], ['up', 2460, False], ['right', 2660, False], ['left', 2840, False], ['right', 3040, False], ['up', 3260, False], ['down', 3400, False], ['left', 3600, False], ['up', 3700, False], ['down', 3900, False], ['up', 4040, False], ['right', 4120, False], ['left', 4260, False], ['up', 4340, False], ['right', 4480, False],  ['left', 4700, False], ['right', 4780, False],  ['left', 5060, False], ['up', 5220, False], ['down', 5320, False], ['right', 5580, False], ['up', 6040, False], ['down', 6240, False],  ['right', 7020, False], ['left', 7100, False], ['right', 7980, False], ['left', 8040, False], ['right', 8100, False], ['left', 8200, False], ['up', 8300, False], ['down', 8400, False], ['right', 8540, False], ['left', 8740, False], ['right', 8960, False], ['up', 9020, False]], 20),
                        FightDialouge("It hurts me to hurt you like this"),
                        FightDialouge("But there is no choice"),
                        FightDialouge("Town ain't big enough for two worldwides"),
                        FightDialouge("Btw, remember to not waste water unecessarily or you will get a united nations meeting"),
                        BarTiming(20, 15),
                        BarTiming(20, 15),
                        BarTiming(20, 15),
                        ButtonMash(600, 1, 10, 10000),
                        FightDialouge("Damn you are tough"),
                        FightDialouge("This is looking bad for me"),
                        FightDialouge("I CALL UPON THE LAWS OF THE WORLD"),
                        FightDialouge("GIVE ME THE POWER TO DEFEAT THIS GUY"),
                        FightDialouge("AGHHHHHHH"),
                        Rythm([['up', 1920, False], ['right', 2640, False], ['down', 3020, False], ['up', 3500, False], ['right', 3640, False], ['left', 3860, False], ['down', 4000, False], ['up', 4120, False], ['right', 4200, False], ['left', 4320, False], ['up', 4480, False], ['down', 4660, False], ['right', 4800, False], ['left', 4940, False], ['up', 5120, False], ['right', 5240, False], ['left', 5400, False],  ['right', 5760, False], ['up', 5940, False], ['down', 6060, False], ['left', 6320, False], ['up', 6440, False], ['right', 6660, False], ['left', 6860, False], ['up', 7040, False], ['down', 7160, False], ['right', 7240, False], ['left', 7340, False], ['up', 7700, False], ['down', 7820, False], ['right', 8000, False], ['left', 8100, False]], 20),
                        Rythm([['up', 1700, False], ['right', 1940, False], ['down', 2140, False], ['left', 2320, False], ['up', 2440, False],  ['up', 2980, False], ['right', 3300, False], ['left', 3360, False],  ['down', 4140, False], ['right', 4240, False], ['left', 4300, False], ['up', 4500, False], ['up', 4900, False], ['up', 5300, False], ['left', 5400, False], ['right', 5560, False], ['up', 5660, False], ['left', 5760, False], ['right', 5880, False],   ['up', 6900, False],  ['up', 7120, False], ['right', 7220, False], ['left', 7320, False], ['up', 7420, False], ['left', 7660, False],  ['right', 8020, False], ['left', 9740, False], ['right', 9820, False],  ['up', 10420, False], ['down', 10520, False], ['up', 10620, False], ['down', 10720, False], ['right', 11200, False], ['left', 11440, False], ['up', 11640, False], ['down', 11760, False], ['right', 11840, False], ['left', 12000, False], ['up', 12120, False], ['right', 12360, False], ['down', 12500, False], ['up', 12600, False], ['left', 12680, False]], 20),
                        FightDialouge("Seems like you did not betray the gang"),
                        FightDialouge("Thank you for clearing this up Kamal"))
        
                    elif game_state == 3:
                        boss = Boss(pygame.transform.scale_by(pygame.image.load(os.path.join(root, "Assets/Images/rock Black and White.png")), 0.6), rock_music, (1 - player.def_factor) * 5, player.current_health, player.max_health, player.heal_factor,
                        Rythm([['up', 1915, False], ['right', 2115, False], ['down', 2315, False], ['up', 2515, False], ['left', 2715, False], ['down', 2965, False], ['up', 3165, False], ['down', 3390, False], ['up', 3565, False], ['down', 3790, False], ['right', 4015, False], ['left', 4340, False], ['up', 4515, False], ['down', 4690, False], ['up', 4940, False], ['down', 5190, False], ['up', 5315, False], ['right', 5465, False], ['left', 5590, False], ['down', 5815, False], ['up', 5990, False], ['left', 6215, False], ['down', 6390, False], ['right', 6515, False], ['up', 6640, False], ['left', 6790, False], ['down', 7040, False], ['up', 7215, False], ['down', 7440, False], ['up', 7615, False], ['right', 7790, False], ['left', 7965, False], ['up', 8140, False], ['down', 8465, False], ['up', 8615, False], ['right', 8840, False], ['left', 9115, False], ['up', 9290, False], ['down', 9440, False], ['right', 9640, False], ['up', 9790, False], ['left', 10015, False], ['down', 10165, False], ['up', 10315, False], ['down', 10440, False], ['up', 10615, False], ['right', 10865, False], ['left', 11065, False], ['up', 11215, False], ['down', 11415, False], ['up', 11540, False], ['right', 11740, False], ['down', 11940, False], ['left', 12090, False], ['up', 12240, False], ['down', 12415, False], ['up', 12565, False], ['down', 12715, False], ['up', 12840, False], ['down', 13065, False], ['up', 13215, False], ['down', 13440, False], ['left', 13640, False], ['right', 13915, False], ['up', 14115, False], ['down', 14265, False], ['left', 14540, False], ['up', 14740, False], ['down', 14890, False], ['up', 15040, False], ['down', 15165, False], ['up', 15365, False], ['down', 15540, False], ['right', 15640, False], ['left', 15815, False], ['down', 15965, False], ['up', 16115, False], ['down', 16240, False], ['left', 16365, False], ['up', 16540, False], ['down', 16790, False], ['up', 17065, False], ['down', 17290, False], ['up', 17415, False], ['right', 17565, False], ['down', 17740, False], ['left', 17915, False], ['up', 18040, False], ['down', 18215, False], ['up', 18440, False]], 25),
                        FightDialouge("You thought my cold stares were hard, well check this out"),
                        BarTiming(15, 10),
                        FightDialouge("It was so fun acting for roles together, but I guess all good times come to an end"),
                        FightDialouge("Remember that time we wrote the lyrics of my song together for that disney movie; where are those times now?"),
                        FightDialouge("Who will assist me with my movie production now? Sad really."),
                        ButtonMash(650, 2, 10, 9000),
                        ButtonMash(650, 2, 10, 9000),
                        BarTiming(15, 10),
                        ButtonMash(650, 2, 10, 9000),
                        FightDialouge("Damn you are good, I mean I should have known it wouldn't be that easy"),
                        FightDialouge("You have almost done me in, BUT I SHALL FIGHT YOU WITH THE ONE LAST BREATH I HAVE LEFT. YOU DON'T GET TO ENTERTAIN PEOPLE ALONE."),
                        Rythm([['right', 7415, False], ['left', 7540, False], ['right', 7690, False], ['left', 7790, False], ['right', 7915, False], ['up', 8090, False], ['down', 8240, False], ['up', 8390, False], ['right', 8640, False], ['left', 8765, False], ['right', 8915, False], ['left', 9015, False], ['up', 9240, False], ['down', 9515, False], ['up', 9965, False], ['right', 10490, False], ['left', 11015, False], ['right', 11140, False], ['left', 11290, False], ['right', 11440, False], ['left', 11565, False], ['down', 11765, False], ['up', 11890, False], ['down', 12215, False], ['right', 12365, False], ['left', 12465, False], ['right', 12690, False], ['up', 12815, False], ['down', 13090, False], ['right', 13315, False], ['left', 13615, False], ['up', 14515, False], ['down', 14665, False], ['right', 14765, False], ['left', 14890, False], ['up', 15015, False], ['right', 15190, False], ['left', 15290, False], ['right', 15465, False], ['up', 15790, False], ['down', 15940, False], ['up', 16090, False], ['down', 16240, False], ['up', 16565, False], ['right', 16915, False], ['left', 17190, False], ['up', 17615, False], ['right', 18115, False], ['left', 18540, False], ['right', 18665, False], ['up', 18940, False], ['down', 19115, False], ['right', 19315, False], ['up', 19515, False], ['left', 19790, False], ['up', 19965, False]], 25),
                        Rythm([['right', 1365, False], ['left', 1540, False], ['right', 1665, False], ['left', 1765, False], ['right', 1890, False], ['up', 2140, False], ['down', 2290, False], ['up', 2615, False], ['right', 2690, False], ['left', 2815, False], ['right', 2990, False], ['left', 3240, False], ['up', 3290, False], ['down', 3565, False], ['up', 3715, False], ['down', 3865, False], ['right', 4065, False], ['left', 4165, False], ['right', 5040, False], ['left', 5165, False], ['right', 5290, False], ['left', 5415, False], ['up', 5590, False], ['down', 5715, False], ['up', 5865, False], ['right', 6190, False]], 25),
                        FightDialouge("Ah damn I couldn't beat you. Maybe I should have given you a hard stare instead"),
                        FightDialouge("Wait, you did not say those things about me? Oh well it seems like we have no beef then"))
    
                    elif game_state == 4:
                        boss = Boss(pygame.transform.scale_by(pygame.image.load(os.path.join(root, "Assets/Images/Irfan Black and White.png")), 0.8), irfan_music, (1 - player.def_factor) * 6, player.current_health, player.max_health, player.heal_factor,
                        Rythm([['up', 14300, False], ['down', 14840, False], ['up', 15020, False], ['right', 15530, False], ['left', 15770, False], ['up', 16040, False], ['down', 16340, False], ['up', 16790, False], ['down', 17000, False], ['up', 17180, False], ['down', 17690, False], ['up', 17870, False], ['right', 18020, False], ['left', 18470, False], ['up', 18740, False], ['down', 18980, False], ['right', 19220, False], ['up', 19430, False], ['left', 19790, False], ['down', 19910, False], ['up', 20270, False], ['down', 20750, False], ['up', 20960, False], ['left', 21110, False], ['right', 21440, False], ['up', 21680, False], ['left', 21920, False], ['down', 22220, False], ['up', 22670, False], ['down', 22880, False], ['up', 23030, False], ['down', 23630, False], ['up', 23780, False], ['right', 23870, False], ['left', 24350, False], ['up', 24470, False], ['down', 24710, False], ['up', 25070, False], ['down', 25250, False], ['left', 25700, False], ['up', 25820, False], ['right', 26180, False], ['up', 26510, False], ['up', 26930, False], ['up', 27080, False], ['up', 27140, False], ['up', 27320, False], ['down', 27650, False], ['up', 28070, False], ['down', 28400, False], ['up', 28550, False], ['up', 28640, False], ['up', 28730, False], ['up', 28850, False], ['down', 29150, False], ['right', 29510, False], ['up', 29900, False], ['up', 30020, False], ['up', 30110, False], ['down', 30290, False], ['right', 30650, False], ['left', 30890, False], ['up', 31010, False], ['down', 31220, False], ['right', 31310, False], ['left', 31430, False], ['up', 31550, False], ['right', 31730, False], ['down', 31850, False], ['up', 32120, False], ['down', 32480, False], ['up', 32840, False], ['up', 32960, False], ['up', 33050, False], ['right', 33260, False], ['left', 33650, False], ['up', 33980, False], ['right', 34310, False], ['up', 34490, False], ['up', 34610, False], ['up', 34730, False], ['right', 34970, False], ['down', 35150, False], ['up', 35510, False], ['left', 35750, False], ['up', 35900, False], ['up', 36020, False], ['up', 36200, False], ['right', 36440, False], ['left', 36620, False], ['up', 36740, False], ['right', 36890, False], ['down', 37010, False], ['left', 37160, False], ['up', 37340, False], ['right', 37520, False], ['down', 37730, False]], 30),
                        BarTiming(10, 15),
                        FightDialouge("The True Battle Begins Now"),
                        FightDialouge("Be prepared to live the last breath of your life"),
                        ButtonMash(650, 0.2, 7, 6000),
                        BarTiming(15, 10),
                        FightDialouge("I thought seperating you from your gang would work, but I underestimated how benevolent you are."),
                        FightDialouge("Guess I'll have to put an end to your goodness myself"),
                        BarTiming(10, 15),
                        BarTiming(10, 15),
                        BarTiming(10, 15),
                        BarTiming(10, 15),
                        BarTiming(10, 15),
                        FightDialouge("Huh you're holding up pretty well. Eh I'll still win"),
                        Rythm([['up', 5330, False], ['up', 5450, False], ['right', 5570, False], ['down', 5660, False], ['left', 5960, False], ['up', 6080, False], ['right', 6260, False], ['down', 6380, False], ['left', 6500, False], ['up', 6740, False], ['up', 6830, False], ['up', 6920, False], ['right', 7070, False], ['down', 7220, False], ['left', 7490, False], ['up', 7640, False], ['right', 7850, False], ['down', 8000, False], ['left', 8090, False], ['up', 8270, False], ['up', 8360, False], ['up', 8450, False], ['right', 8630, False], ['down', 8840, False], ['left', 9020, False], ['up', 9170, False], ['right', 9320, False], ['down', 9530, False], ['left', 9650, False], ['up', 9800, False], ['up', 9890, False], ['up', 9980, False], ['up', 10070, False], ['right', 10190, False], ['down', 10370, False], ['left', 10520, False], ['up', 10730, False], ['right', 10850, False], ['down', 11000, False], ['left', 11090, False], ['up', 11210, False], ['up', 11330, False], ['up', 11420, False], ['up', 11510, False], ['right', 11630, False], ['down', 11780, False], ['left', 11930, False], ['up', 12110, False], ['right', 12260, False], ['down', 12470, False], ['left', 12560, False], ['up', 12740, False], ['up', 12860, False], ['up', 13100, False], ['right', 13160, False], ['down', 13370, False], ['left', 13430, False], ['up', 13580, False], ['right', 13730, False], ['down', 13880, False], ['left', 14000, False], ['up', 14180, False], ['up', 14330, False], ['up', 14450, False], ['up', 14570, False], ['right', 14750, False], ['down', 14870, False], ['left', 14990, False], ['up', 15140, False], ['right', 15290, False], ['left', 15530, False], ['up', 15770, False], ['down', 15980, False], ['up', 16130, False], ['up', 16280, False], ['up', 16400, False], ['up', 16520, False], ['right', 16640, False], ['down', 16790, False], ['left', 16910, False], ['up', 17030, False]], 30),
                        FightDialouge("You feel pain? Yeah, this is what your friends went through"),
                        FightDialouge("You know what, I think you get the point. So I'll not attack you anymore"),
                        Rythm([['up', 25790, False]], 30),
                        FightDialouge("Sike, didnt you see the arrows?"),
                        Rythm([['up', 2660, False], ['right', 2870, False], ['down', 2990, False], ['left', 3110, False], ['up', 3260, False], ['up', 3380, False], ['up', 3470, False], ['right', 3560, False], ['down', 3710, False], ['left', 3800, False], ['up', 3950, False], ['right', 4160, False], ['down', 4250, False], ['up', 4490, False], ['up', 4640, False], ['up', 4700, False], ['right', 4880, False], ['down', 5000, False], ['left', 5060, False], ['up', 5270, False], ['right', 5360, False], ['left', 5570, False], ['up', 5690, False], ['up', 5810, False], ['up', 5930, False], ['up', 6020, False], ['up', 6140, False], ['right', 6170, False], ['down', 6290, False], ['left', 6380, False], ['up', 6500, False], ['right', 6560, False], ['down', 6650, False], ['left', 6680, False], ['up', 6800, False], ['right', 6920, False], ['down', 7010, False], ['left', 7040, False], ['up', 7310, False], ['up', 7460, False], ['up', 7610, False], ['up', 7700, False], ['right', 7820, False], ['down', 7910, False], ['left', 7970, False], ['up', 8060, False], ['right', 8150, False], ['left', 8240, False], ['up', 8510, False], ['left', 8510, False], ['down', 8750, False], ['up', 8930, False], ['left', 9050, False], ['up', 9110, False], ['up', 9230, False], ['up', 9290, False], ['right', 9440, False], ['left', 9650, False], ['up', 9890, False], ['right', 10130, False], ['down', 10220, False], ['left', 10280, False], ['up', 10370, False], ['up', 10460, False], ['up', 10550, False], ['right', 10670, False], ['down', 10790, False], ['left', 10820, False], ['up', 10970, False], ['right', 11090, False], ['down', 11210, False], ['left', 11270, False], ['up', 11390, False], ['down', 11660, False], ['right', 11870, False], ['left', 12020, False]], 30),
                        ButtonMash(680, 1.5, 10, 10000),
                        FightDialouge("Aw man, that was all I had"),
                        FightDialouge("*Sigh*"),
                        FightDialouge("How pathetic, I couldn't even stop you"),
                        FightDialouge("Thought I could put an end to you but alas, it is what it is innit"),
                        FightDialouge("Hope you enjoy the life, Kamal"),
                        FightDialouge("Seems like revenge never ends well, does it?"),
                        FightDialouge("I guess maybe I should have taken some other route to satisfy me"),
                        FightDialouge("But maybe there was no other way"),
                        FightDialouge("Maybe all of you were destined to be together"),
                        FightDialouge("All except me . . ."),
                        FightDialouge("Hey man"),
                        FightDialouge("I'm about to go now"),
                        FightDialouge("But I have one last wish"),
                        FightDialouge("Please forgive me for this incident, will you? I'm truly sorry"))

                    pygame.mixer.music.stop()
                    result = boss.execute()

                    pygame.mixer.music.load(os.path.join(root, "Assets/Music/Deltarune OST_ 13 - Field of Hopes and Dreams.mp3"))
                    pygame.mixer.music.play(-1)

                    if result:  # updates the health and increments game state if the boss fight is won
                        game_state += 1
                        player.current_health = result[1]
                    else:
                        running = False  # otherwise quits the game

                    if game_state == 5:  # ends the game if the final boss has been beaten
                        running = False

                    room = 0  # moves back to room 0 and default coordinates if the room after the fight
                    player.playerX = 400
                    player.playerY = 300
            
                elif generic_option == 1:
                    generic_menu_open = False
            elif event.key == pygame.K_RETURN and player.playerX >= 420:
                generic_menu_open = True
            elif event.key == pygame.K_UP or event.key == pygame.K_w and generic_menu_open:
                generic_option -= 1
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s and generic_menu_open:
                generic_option += 1
            if event.key == pygame.K_ESCAPE:
                pause_menu()
    
    screen.blit(boss_room_background, (0, 0))
    screen.blit(player.image, (player.playerX, player.playerY))

    if game_state == 0:  # draws the appropriate boss based on game state
        screen.blit(npc_image, (485, 185))
    elif game_state == 1:
        screen.blit(jiraya_image, (490, 185))
    elif game_state == 2:
        screen.blit(pitbull_image, (485, 185))
    elif game_state == 3:
        screen.blit(rock_image, (485, 170))
    elif game_state == 4:
        screen.blit(irfan_image, (500, 185))

    
    if player.playerX > 420:
        player.playerX = 420
    if player.playerY < 0:
        player.playerY = 0
    if player.playerY > 450:
        player.playerY = 450
    
    if generic_menu_open:
        generic_menu("Fight boss?")
    
    if player.playerX < -50:
        room = 0
        player.playerX = 740
    
    
# main program begins here
if __name__ == "__main__":
    opening()  # calls the intro module

    screen.fill((0, 0, 0))  # black screen for some waiting time
    pygame.display.update()
    pygame.time.delay(1000)

    result = main_menu()  # calls the main menu
    if result == 0:  # if the first option is selected, then the game state variable and player object is initialsed using the save data
        result = read_save_data()
        game_state = result[0]
        kamal = Player(*result[1:])

    elif result == 1:  # if new game option is selected, the game is launched with default values
        game_state = 0
        kamal = Player(20, 20, 0, 1, 0)
    else:
        game_state = 0

    # loading of many global variables
    central_room_flag = False  # used to set boundaries in the central room
    generic_menu_open = False  # flag to determine whether the generic menu is open
    generic_option = 0  # variable to store the option highlighted in the generic menu
    
    # loads images, explanatory by name
    central_room_background = pygame.image.load(os.path.join(root, "Assets/Images/Central Room.jpg"))
    home_background =pygame.image.load(os.path.join(root, "Assets/Images/Home.jpg"))
    club_background = pygame.image.load(os.path.join(root, "Assets/Images/club.jpg"))
    dance_floor = pygame.transform.scale_by(pygame.image.load(os.path.join(root, "Assets/Images/dance floor.jpg")), 0.15)
    boss_room_background = pygame.image.load(os.path.join(root, "Assets/Images/Boss Room.jpg"))

    npc_image = pygame.transform.scale_by(pygame.image.load(os.path.join(root, "Assets/Images/NPC.png")), 0.5)
    jiraya_image = pygame.transform.scale_by(pygame.image.load(os.path.join(root, "Assets/Images/Jiraya.png")), 0.25)
    pitbull_image = pygame.transform.scale_by(pygame.image.load(os.path.join(root, "Assets/Images/pitbull.png")), 0.5)
    rock_image = pygame.transform.scale_by(pygame.image.load(os.path.join(root, "Assets/Images/rock.png")), 0.4)
    irfan_image = pygame.transform.scale_by(pygame.image.load(os.path.join(root, "Assets/Images/Irfan.png")), 0.6)
    
    # gets file name of the music, self explanatory names
    npc_music = os.path.join(root, "Assets/Music/_Bullet Hell_ (OverSave-Tale) Sans BOSS Theme.mp3")
    jiraya_music = os.path.join(root, "Assets/Music/Naruto Theme - The Raising Fighting Spirit.mp3")
    pitbull_music = os.path.join(root, "Assets/Music/Underverse - Overwrite [X-Event!Chara Theme].mp3")
    rock_music = os.path.join(root, "Assets/Music/undyne-the-undying--online-audio-converter.com-.mp3")
    irfan_music = os.path.join(root, "Assets/Music/Undertale Last Breath_ An Enigmatic Encounter (Phase 3).mp3")

    tutorial_font = pygame.font.Font("freesansbold.ttf", 16)
    tutorial_text = tuple(map(lambda x: tutorial_font.render(x, True, (255, 255, 0)) ,("Welcome to the game. Lets begin the Tutorial", "Please press escape to pause the game","Pause the game and return to proceed further", "Exiting the game using menu will auto-save the game", "(although it wont save without finishing the tutorial)" ,"Use arrow keys or WASD to move around", "Move and follow the path to the left and do not stop following it", "We are now at Kamal's house", "Here you can game to gain energy", "Go near the couch and press enter to begin gaming", "After pressing enter on yes in the menu,", "mash the F key repeatedly such that the white bar moves to the green zone", "Succesful gaming gives you 5 enery points", "The amount of hp you gain or lose depends on the zone you end up in", "Go move to the right to return to the central room","Follow the downwards path to go to the club", "where kamal can dance", "Go upto the dance floor and press enter to begin dancing", "Dancing works in the same way as gaming", "Dancing gives you 20 energy", "Leave by going up through the door", "Lets explain the purpose of the red, blue and green zone in these mini games shall we?", "Green zone causes an increase health by a value called the heal factor", "Blue causes no damage to be taken and red causes health decrement", "Travel up the road to go to the shop to use energy to upgrade kamal", "Ok now finally go to the right room to fight your first \"boss\"", "In the room press enter near the boss to initiate the boss fight", "Defeating the boss will complete the tutorial allowing progress to be saved", "Note that if you do not have enough health you cannot game or dance", "Health will never be allowed to fall to 1 or below by default")))  # generates text for tutorial

    # flags to mark different actions being completed
    pause_menu_opened = False
    home_visited = False
    gamed = False
    club_visited = False
    danced = False
    shop_visited = False
    boss_visited = False


    room = 0  # inital room number
    pygame.mixer.music.load(os.path.join(root, "Assets/Music/Deltarune OST_ 13 - Field of Hopes and Dreams.mp3"))  # loads and plays the background music
    pygame.mixer.music.play(-1)

    while running:  # main game loop
        clock.tick(30)  # maintenance of FPS
        if not(boss_visited) and game_state == 0:  # checks if tutorial has not been completed
            if shop_visited:  # blits different parts of the tutorial text depending on what has been done. The full features of the game are restricted till the tutorial is complete
                if room == 0:
                    central_room(kamal)
                    screen.blit(tutorial_text[25], (20, 65))
                    screen.blit(tutorial_text[26], (20, 85))
                    screen.blit(tutorial_text[27], (20, 105))
                elif room == 1:
                    home(kamal)
                elif room == 2:
                    club(kamal)
                elif room == 3:
                    boss_visited = True
            elif danced:
                if room == 0:
                    central_room(kamal)
                    screen.blit(tutorial_text[21], (20, 65))
                    screen.blit(tutorial_text[22], (20, 85))
                    screen.blit(tutorial_text[23], (20, 105))
                    screen.blit(tutorial_text[28], (20, 125))
                    screen.blit(tutorial_text[29], (20, 145))
                    screen.blit(tutorial_text[24], (20, 165))
                elif room == 1:
                    home(kamal)
                elif room == 2:
                    club(kamal)
                    screen.blit(tutorial_text[19], (20, 65))
                    screen.blit(tutorial_text[20], (20, 85))
                elif room == 3:
                    room = 0
                    kamal.playerX = 740

            elif club_visited:
                club(kamal)
                if room == 0:
                    room = 2
                screen.blit(tutorial_text[17], (20, 65))
                screen.blit(tutorial_text[18], (20, 85))
                
            elif gamed:
                if room == 1:
                    home(kamal)
                    screen.blit(tutorial_text[12], (20, 65))
                    screen.blit(tutorial_text[13], (20, 85))
                    screen.blit(tutorial_text[14], (20, 105))
                elif room == 0:
                    central_room(kamal)
                    if room == 3:
                        room = 0
                        kamal.playerX = 740
                    if kamal.playerY < 0:
                        kamal.playerY = 0
                    if room == 2:
                        club_visited = True
                    screen.blit(tutorial_text[15], (20, 65))
                    screen.blit(tutorial_text[16], (20, 85))
            elif home_visited:
                home(kamal)
                if room == 0:
                    room = 1
                    kamal.playerX = 740
                screen.blit(tutorial_text[7], (20, 65))
                screen.blit(tutorial_text[8], (20, 85))
                screen.blit(tutorial_text[9], (20, 105))
                screen.blit(tutorial_text[10], (20, 125))
                screen.blit(tutorial_text[11], (20, 145))
            elif pause_menu_opened:
                central_room(kamal)
                if room == 1:
                    home_visited = True
                if room == 2:
                    room = 0
                    kamal.playerY = 500
                if room == 3:
                    room = 0
                    kamal.playerX = 740
                if kamal.playerY < 0:
                    kamal.playerY = 0
                screen.blit(tutorial_text[3], (20, 65))
                screen.blit(tutorial_text[4], (20, 85))
                screen.blit(tutorial_text[5], (20, 105))
                screen.blit(tutorial_text[6], (20, 125))
            else:
                central_room(kamal)
                screen.blit(tutorial_text[0], (20, 65))
                screen.blit(tutorial_text[1], (20, 85))
                screen.blit(tutorial_text[2], (20, 105))

            if pause_menu_opened:
                kamal.movment()
        else:  # if the tutorial is complete then this part runs
            # detects which room kamal is in and draws out the appropriate room
            if room == 0:
                central_room(kamal)
            elif room == 1:
                home(kamal)
            elif room == 2:
                club(kamal)
            elif room == 3:
                boss_room(kamal)
            kamal.movment()  # player movement
            
        display_health_and_energy(kamal.current_health, kamal.max_health, kamal.energy)  # draws the health and energy in the corner of the screen
        pygame.display.update()
        if kamal.current_health <= 1:  # prevents health from going 1 or below
            kamal.current_health = 1.1
    if game_state > 0 and game_state < 5:  # game saving mechanism if the tutorial has been completed
        write_save_data()
    elif game_state == 5:  # rolls the credits if the game ends without saving
        ending()
