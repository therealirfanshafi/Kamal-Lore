"""
This module is used to create the game and dance objects using the class implemented above
It inherits the boss class as the features are very similar
However it uses some polymorphism to customise certain features
It basically runs a single set Button mash command depending on the mode in which it is called
"""

import pygame, os
from boss import Boss
from button_mash import ButtonMash
pygame.init()

screen = pygame.display.set_mode((800, 600))
absolute_path = os.path.dirname(__file__)

class GameOrDance(Boss):
    def __init__(self,  player_health, player_max_health, player_heal_factor, mode):  # constructor
        super().__init__(None, None, None, player_health, player_max_health, player_heal_factor)  # calls the constructor of the boss class with the first 3 arguments being None since these have some default values based on th the mode
        self.mode = mode  # either "g" to indicate gaming or "d" to indicate dancing

        if mode == "g":  # loads the appropriate images/music and values based on the mode
            self.image = pygame.transform.scale_by(pygame.image.load(os.path.join(absolute_path, "Images/pac man.jpg")), 0.2)
            self.music = os.path.join(absolute_path, "Music/Running in the 90's.mp3")
            self.boss_damage = 1
            self.energy = 5
            self.attack = ButtonMash(650, 0.1, 5, 11000)

        elif mode == "d":
            self.image = pygame.transform.scale_by(pygame.image.load(os.path.join(absolute_path, "Images/default dance.png")), 1.2)
            self.music = os.path.join(absolute_path, "Music/ALL MY FELLAS.mp3")
            self.boss_damage = 5
            self.energy = 20
            self.attack = ButtonMash(675, 1, 7, 11000)

    def display_lost_message(self):  # displays you failed on the screen if the button mash attack fails
        screen.fill((0, 0, 0))
        lost_message = self.font2.render("You failed", True, (255, 255, 255))
        screen.blit(lost_message, (300, 250))
        pygame.display.update()
        pygame.time.delay(3500)
    
    def display_win_message(self):  # displays a win message if the buttom mash attack is evaded successfully
        pygame.mixer.music.load(os.path.join(absolute_path, "Music/GTA San Andreas - Mission passed sound.mp3"))
        pygame.mixer.music.play()
        screen.fill((0, 0, 0))
        win_message = pygame.image.load(os.path.join(absolute_path, "Images/mission passed.png"))
        screen.blit(win_message, (100, 200))
        pygame.display.update()
        pygame.time.delay(7500)
        pygame.mixer.music.stop()
    
    def execute(self):  # main method
        # loads and the plays the music from the correct spot
        pygame.mixer.music.load(self.music)
        if self.mode == "g":
            pygame.mixer.music.play(start= 25)
        elif self.mode == "d":
            pygame.mixer.music.play()

        self.attack.execute(self)  # executes the button mash attack
        pygame.time.delay(1000)
        pygame.mixer.music.stop()
        if self.player_health < self.player_initial_health:  # uses the fact that health decrement occurs upon failure to detect failure
            self.display_lost_message()
            return 0, self.player_health  # returs no energy if failed
        self.display_win_message()
        return self.energy, self.player_health  # returns the appropriate energy if sucess occurs

