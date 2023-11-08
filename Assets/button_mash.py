import pygame
pygame.init()

"""
This module is another type of boss attack.
Here you have to mash the F key to move the white bar forward, with it moving backwards if not done so
If the white bar is the in green position after the alloted time, healh is incremented
For the blue part, nothing happens, and for the red part, health is decremented
"""

screen = pygame.display.set_mode((800, 600))


class ButtonMash:  # main class
    def __init__(self, position, back_speed, front_speed, time):  # takes position of the green bar, distance moved back if space is not pressed, distance moved forward if space is pressed and time of attack as parameters
        self.health_position = position
        self.back_speed = back_speed
        self.front_speed = front_speed
        self.time = time
        self.safe_position = position - 1.1 * (700 -position)  # calculates position of the blue zone
        
        # creates the rectangles for the red blue and green zone
        self.main_rect = pygame.Rect(400, 500, 300, 40)
        self.safe_rect = pygame.Rect(self.safe_position, 500, 700 - self.safe_position, 40)
        self.health_rect = pygame.Rect(self.health_position, 500, 700 - self.health_position, 40)

    def execute(self, boss):  # main function
        clock = pygame.time.Clock()
        endTime = startTime = pygame.time.get_ticks()  # timing variables
        movingPos = 400
        while endTime - startTime <= self.time:  # runs until the time passes
            # draws the rectangles
            clock.tick(30)
            screen.fill((0, 0, 0))
            boss.draw_boss_and_health()
            pygame.draw.rect(screen, (255, 0, 0), self.main_rect)
            pygame.draw.rect(screen, (0, 0, 255), self.safe_rect)
            pygame.draw.rect(screen, (0, 255, 0), self.health_rect)
            pressed = False  # flag is set to True if a space is pressed
            for event in pygame.event.get(): 
                if event.type == pygame.KEYDOWN:  # checks for key press
                    if event.key == pygame.K_f:
                        pressed = True
                        if movingPos <= 700:  # moves the moving bar forward only if it is not exceeding the red bar
                            movingPos += self.front_speed
            if not(pressed):
                if movingPos >= 400:
                    movingPos -= self.back_speed  # moves the moving bar back if it is not exceeding the red bar
            # creates and draws the red bar
            movingRect = pygame.Rect(400, 505, movingPos - 400, 30)
            pygame.draw.rect(screen, (255, 255, 255), movingRect)
            endTime = pygame.time.get_ticks()
            pygame.display.update()

        # increment or decrement of health based on the position of the moving bar     
        if movingPos >= self.health_position:
            if boss.player_health < boss.player_max_health:
                boss.player_health += boss.player_heal_factor
                if boss.player_health > boss.player_max_health:
                    boss.player_health = boss.player_max_health
        elif movingPos < self.safe_position:
            if boss.player_health > 0:
                boss.player_health -= boss.boss_damage
        
        if boss.player_health <= 0:
            return True
        return False
        