# This module contains a class to easily generate a boss fight
from rythm import Rythm
from fight_dialogue import FightDialouge
from button_mash import ButtonMash
from bar_timing import BarTiming
import os
import pygame
pygame.init()

screen = pygame.display.set_mode((800, 600))

Clock = pygame.time.Clock()


class Boss:
    def __init__(self, image, music, boss_damage, player_health, player_max_health, player_heal_factor, *attacks):   #many parameters for constructor
        self.image = image  # image of boss
        self.music = music  # main theme of boss
        self.boss_damage = boss_damage  # damage dealt by boss
        self.player_health = player_health  # health of player
        self.player_initial_health = player_health  # health of player stored in another variable to reinitialise in case of loss of health
        self.player_max_health = player_max_health  # max possible health allowed for the player
        self.player_heal_factor = player_heal_factor  # value by which player heals in case of success
        self.attacks = attacks  # an array of attacks by boss 
        self.player_health_bar = pygame.Rect(40, 550, player_max_health * 3, 10)  # creates health bar 
        # loading of fonts
        self.font = pygame.font.Font("freesansbold.ttf", 16)
        self.font2 = pygame.font.Font("freesansbold.ttf", 32)
        self.loss_font = pygame.font.Font("freesansbold.ttf", 64)
    
    # draws boss and health bars
    def draw_boss_and_health(self):
        player_current_health_rect = pygame.Rect(40, 550, self.player_health * 3, 10)  # health bar
        player_health_display = self.font.render(f"Your health: {round(self.player_health, 1)}", True, (255, 255, 255))  # value of current health
        screen.blit(player_health_display, (40, 570))  
        pygame.draw.rect(screen, (255, 0, 0), self.player_health_bar)
        pygame.draw.rect(screen, (0, 255, 0), player_current_health_rect)
        screen.blit(self.image, (40, 50))


    # displays lost message if lost in the fight
    def display_lost_message(self):
        pygame.mixer.music.load(os.path.join(absolute_path, "Music/Do or Die OST - Medley for a Broken Sky.mp3"))  # loss theme
        pygame.mixer.music.play()
        pygame.time.delay(1000)
        loss_message = "YOU DIED"

        # loop to display the string YOU DIED slowly
        for i in range(9):
            currentWords = self.loss_font.render(loss_message[:i], True, (255, 255, 255))
            screen.fill((0, 0, 0))
            screen.blit(currentWords, (240, 64))
            pygame.time.delay(200)
            pygame.display.update()
        pygame.time.delay(200)

        option = 0  # tracks which option in the menu the pointer is one
        while True:
            screen.fill((0, 0, 0))
            screen.blit(currentWords, (240, 64))
            if option == 0:  # condition yellows the option pointed to
                try_again = self.font2.render("Try Again", True, (255, 255, 0))
                leave = self.font2.render("Quit", True, (255, 255, 255))
            else:
                try_again = self.font2.render("Try Again", True, (255, 255, 255))
                leave = self.font2.render("Quit", True, (255, 255, 0))
            # displays the options on screen
            screen.blit(try_again, (240, 164))
            screen.blit(leave, (240, 224))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:  # allows scrolling up and down based on key press
                        option += 1
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        option -= 1
                    if event.key == pygame.K_RETURN:  # if enter is pressed 
                        pygame.mixer.music.stop() 
                        if option == 0:  # on TRY AGAIN, the fight starts against
                            return True
                        return False  # otherwise the fight ends
            if option < 0:
                option = 1
            elif option > 1:
                option = 0
            pygame.display.update()
    
    def display_win_message(self):
        screen.fill((0, 0, 0))
        win_message = "YOU WON"
        for i in range(8):
            currentWords = self.loss_font.render(win_message[:i], True, (255, 255, 255))
            screen.fill((0, 0, 0))
            screen.blit(currentWords, (240, 64))
            pygame.time.delay(200)
            pygame.display.update()
        pygame.time.delay(2000)

    # main function
    def execute(self):
        while True:  # continues until the fight is won or the player quits
            Clock.tick(30)
            lost = False
            pygame.mixer.music.load(self.music)  # loads and plays boss music
            pygame.mixer.music.play()
            for attack in self.attacks:  # iteterates throught each attack and executes it
                lost = attack.execute(self) # returns a boolean of False if health falls 0 or below
                self.draw_boss_and_health()
                pygame.time.delay(2000)  # break of 2 s between every attack
                if lost:
                    pygame.mixer.music.stop()  # displays loss message if health goes below 0
                    continue_playing = self.display_lost_message()
                    break     
            if not(lost):
                self.display_win_message()
                return True, self.player_health  # flags whose use is to be decided later
            elif not(continue_playing):
                return False
            else:
                self.player_health = self.player_initial_health  # resets health to what it was at the beginning if fight attempted again
        
absolute_path = os.path.dirname(__file__)

