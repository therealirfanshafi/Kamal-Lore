import pygame
import os
import random
pygame.init()

"""
This module is a class for a type of boss attack. 
In this attack, you have to press space at the instance when the white moving bar is in the green zone.
If this is done, health is incremented (provided the health is not the max health)
If it is pressed while the while bar is in the blue zone, no damage is taken, but health doesnt increase either
If it is pressed while in the red zone, or not pressed at all, damage is taken
"""

screen = pygame.display.set_mode((800, 600))


# main class
class BarTiming:
    def __init__(self, width, speed): #constructor which takes the width of the green zone and speed of the white bar as parameter
        self.speed = speed
        self.healthZoneStart = random.randint(500, 600) #  the green zone position is randomly decided
        self.healthZoneEnd = self.healthZoneStart + width 
        self.safeZoneStart = self.healthZoneStart - width * 1.1 #  the blue zone is 110% the size of the green zone and lies in the in the left and right of the green zone
        self.safeZoneEnd = self.healthZoneEnd + width * 1.1

        # creates the zone rectangles
        self.healthRect = pygame.Rect(self.healthZoneStart, 500, width, 40) 
        self.safeRect = pygame.Rect(self.safeZoneStart, 500, self.safeZoneEnd - self.safeZoneStart, 40)
        self.mainRect = pygame.Rect(400, 500, 300, 40)
    
    def execute(self, boss):  # main function
        clock = pygame.time.Clock()
        initialPos = 390  # starting position of white bar
        pressed_correct = False  # flag which is only set to true if space is pressed in the green or blue zone to prevent taking damage
        pressed = False  # flag which is set to true if spacebar is pressed to break the main loop
        while initialPos <= 710:  # main loop which terminates when the white bar is outside the main rectangle
            clock.tick(30)
            screen.fill((0, 0, 0))
            boss.draw_boss_and_health()
            pygame.draw.rect(screen, (255, 0, 0), self.mainRect)
            pygame.draw.rect(screen, (0, 0, 255), self.safeRect)
            pygame.draw.rect(screen,  (0, 255, 0), self.healthRect)
            movingRect = pygame.Rect(initialPos, 500, 5, 40)
            pygame.draw.rect(screen, (255, 255, 255), movingRect)
            pygame.display.update()
            for event in pygame.event.get():  # checks for key press, specifically space
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pressed = True   # sets pressed flag to True if a space press is detected
                        if initialPos >= self.healthZoneStart and initialPos + 5 <= self.healthZoneEnd:  # checks for green zone
                            pressed_correct = True
                            if boss.player_health < boss.player_max_health:
                                boss.player_health += boss.player_heal_factor
                                if boss.player_health > boss.player_max_health:
                                    boss.player_health = boss.player_max_health
                        elif initialPos >= self.safeZoneStart and initialPos + 5 <= self.safeZoneEnd:  # checks for blue zone
                            pressed_correct = True
            if pressed:
                break
            initialPos += self.speed  # increments the position of the white moving bar by the speed value
        
        if not(pressed_correct):  # decrements health if not pressed at all, or pressed at incorrect time
            if boss.player_health > 0:
                boss.player_health -= boss.boss_damage
        # because the loop breaks, we need to update the new information again outside the loop
        screen.fill((0, 0, 0))
        boss.draw_boss_and_health()
        
        pygame.draw.rect(screen, (255, 0, 0), self.mainRect)
        pygame.draw.rect(screen, (0, 0, 255), self.safeRect)
        pygame.draw.rect(screen,  (0, 255, 0), self.healthRect)
        pygame.draw.rect(screen, (255, 255, 255), movingRect)
        pygame.display.update()

        if boss.player_health <= 0:
            return True
        return False
    
    

