"""
This module is mainly for the rythm attack for the boss fights
It has a class which can easily make a fully functional rythm attack
For this, the correct arrow key has to pressed on the keyboard when the moving arrow is in the correct position, as marked
It is aided by the rythm generator module to easily generate a rythm pattern
"""

# imports of modules
import pygame
import os
pygame.init()  #initialise command

from rythm_generator import upArrow, downArrow, leftArrow, rightArrow  # imports already created images

screen = pygame.display.set_mode((800, 600))  #creates canvas


absolute_path = os.path.dirname(__file__)  # gets the absolute address of the current file

# imports the arrow zone pictures
upArrow_transparent = pygame.image.load(os.path.join(absolute_path, "Images/arrow-up transparent.png"))
leftArrow_transparent = pygame.image.load(os.path.join(absolute_path, "Images/arrow-left transparent.png"))
downArrow_transparent = pygame.image.load(os.path.join(absolute_path, "Images/arrow-down transparent.png"))
rightArrowArrow_transparent = pygame.image.load(os.path.join(absolute_path, "Images/right-arrow transparent.png"))



# main class
FPS = 30
class Rythm:
    def __init__(self, rythm_sequence, speed):
        self.speed = speed  # speed of the rythm pattterns 
        self.rythm_sequence = rythm_sequence  # an array of arrays, each array represents information about a move in the following pattern: [arrow_type, arrow_displacement from an initial position, whether it has been processed or not (set to false at this stage)]
        self.arrow_positions = dict()  # dictionary to hold all the displacements with the arrow types as keys
        self.position_index = dict()  # hash map to hold all the index values of the array with the arrow_displacement as key
        # generates the described dictionaries/hashmaps 
        for i in range(len(rythm_sequence)):
            if rythm_sequence[i][0] in self.arrow_positions:
                self.arrow_positions[rythm_sequence[i][0]] += [rythm_sequence[i][1]]
            else:
                self.arrow_positions[rythm_sequence[i][0]] = [rythm_sequence[i][1]]
            self.position_index[rythm_sequence[i][1]] = i
    
    # main module
    def execute(self, boss):
        clock = pygame.time.Clock() 
        for x in self.rythm_sequence:
            x[2] = False
        initialPos = 40 #  this is the value upon whom the positions of the arrows are calculated. This value is changed to automatically change the position where the arrows are drawn for all the arrows. Using this way, the distance between all the arrows remain connstant for all iterations


        
        #main rythm loop
        while initialPos - self.rythm_sequence[-1][1] <= 2000 and boss.player_health > 0:
            clock.tick(FPS)
            screen.fill((0, 0, 0))  # fills canvas to erase everything previosuly drawn
            boss.draw_boss_and_health()
            screen.blit(upArrow_transparent, (400, 500))
            screen.blit(leftArrow_transparent, (500, 500))
            screen.blit(downArrow_transparent, (600, 500))
            screen.blit(rightArrowArrow_transparent, (700, 500))
            
            # loop to draw all the arrows in their correct position
            
            for move in self.rythm_sequence:
                if move[0] == "up": # checks the type of arrow
                    screen.blit(upArrow, (400, initialPos - move[1]))  # draws the arrow based on the value of the initialPos variable
                elif move[0] == "left":
                    screen.blit(leftArrow, (500, initialPos - move[1]))
                elif move[0] == "down":
                    screen.blit(downArrow, (600, initialPos - move[1]))
                else:
                    screen.blit(rightArrow, (700, initialPos - move[1]))
                if not(move[2]) and (initialPos - move[1]) > 628:  # checks for keys who have not been pressed and have gone outside the pressing range
                    boss.player_health -= boss.boss_damage  # decrements    boss.player_health by damage factor
                    move[2] = True  # sets the "resolved" to true to prevent further damage from being taken by the same arrow
            
            
            for event in pygame.event.get():  # checks for key press
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:  # for when the up key is pressed
                        flag = False  # purpose explained later
                        for value in self.arrow_positions["up"]:  # checks for all the positions which correspond to the up key
                            if initialPos - value >= 468 and initialPos - value <= 596: # checks whether any of the arrow keys are within 50% of the region where the should be upon press
                                flag = True  # sets the flag to true (reason explained later)
                                if boss.player_health < boss.player_max_health:  # if the    boss.player_health is less than the full heath, the    boss.player_health is increased
                                    boss.player_health += boss.player_heal_factor
                                    if boss.player_health > boss.player_max_health:  # sets health back to max health if it is exceeded after increment
                                        boss.player_health = boss.player_max_health
                                self.rythm_sequence[self.position_index[value]][2] = True
                                break
                            elif initialPos - value >= 436 and initialPos - value <= 628:  #checks iif the arrow is within 75% of the required positon upon press, no    boss.player_health is incremented or decremented if this occurs
                                flag = True
                                self.rythm_sequence[self.position_index[value]][2] = True
                                break
                        if not(flag):  # if the flag is not set to true after the loop, i.e. none of the up arrows are at least within 75% of the required position, the    boss.player_health is decremeneted
                            boss.player_health -= boss.boss_damage
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:  # works the same way for all other keys
                        flag = False
                        for value in self.arrow_positions["left"]:
                            if initialPos - value >= 468 and initialPos - value <= 596:
                                flag = True
                                if boss.player_health < boss.player_max_health:
                                    boss.player_health += boss.player_heal_factor
                                    if boss.player_health > boss.player_max_health:
                                        boss.player_health = boss.player_max_health
                                self.rythm_sequence[self.position_index[value]][2] = True
                                break
                            elif initialPos - value >= 436 and initialPos - value <= 628:
                                flag = True
                                self.rythm_sequence[self.position_index[value]][2] = True
                                break
                        if not(flag):
                            boss.player_health -= boss.boss_damage
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        flag = False
                        for value in self.arrow_positions["down"]:
                            if initialPos - value >= 468 and initialPos - value <= 596:
                                flag = True
                                if boss.player_health < boss.player_max_health:
                                    boss.player_health += boss.player_heal_factor
                                    if boss.player_health > boss.player_max_health:
                                        boss.player_health = boss.player_max_health
                                self.rythm_sequence[self.position_index[value]][2] = True
                                break
                            elif initialPos - value >= 436 and initialPos - value <= 628:
                                flag = True
                                self.rythm_sequence[self.position_index[value]][2] = True
                                break
                        if not(flag):
                            boss.player_health -= boss.boss_damage
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        flag = False
                        for value in self.arrow_positions["right"]:
                            if initialPos - value >= 468 and initialPos - value <= 596:
                                flag = True
                                if boss.player_health < boss.player_max_health:
                                    boss.player_health += boss.player_heal_factor
                                    if boss.player_health > boss.player_max_health:
                                        boss.player_health = boss.player_max_health
                                self.rythm_sequence[self.position_index[value]][2] = True
                                break
                            elif initialPos - value >= 436 and initialPos - value <= 628:
                                flag = True
                                self.rythm_sequence[self.position_index[value]][2] = True
                                break
                        if not(flag):
                            boss.player_health -= boss.boss_damage
            

            initialPos += self.speed  # increments the initialPos variable by the speed value for every iteration of the loop
            pygame.display.update()
        #pygame.mixer.music.stop()

        if boss.player_health <= 0:
            return True
        return False

   