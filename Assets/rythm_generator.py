import pygame
from pygame import mixer
import os
pygame.init()


#speed and relative displacement
initialPos = 40
speed = 10
#image loaders
absolutePath = os.path.dirname(__file__)
upArrow = pygame.image.load(os.path.join(absolutePath,"Images/arrow-up.png"))
downArrow = pygame.image.load(os.path.join(absolutePath,"Images/arrow-down.png"))
leftArrow = pygame.image.load(os.path.join(absolutePath,"Images/arrow-left.png"))
rightArrow = pygame.image.load(os.path.join(absolutePath,"Images/right-arrow.png"))



clock = pygame.time.Clock()
pressed = list() #list to save information about the keys pressed
draw = list() #list to draw the pressed keys       

if __name__ == "__main__":
    """
    This module is to help easily generate a sequence of rythm patterns visiually which will save a lot of effort to create the game in the future
    """
    music = pygame.mixer.music.load(os.path.join(absolutePath, "Music/_Bullet Hell_ (OverSave-Tale) Sans BOSS Theme.mp3"))
    pygame.mixer.music.play(start=75274/1000)
    screen = pygame.display.set_mode((800, 600))

  

    running = True
    while running: #main game loop
        clock.tick(30)
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:  # checks for key press
                if event.key == pygame.K_UP:  # draws the appropriate arrow on screen to visually indicate what arrow was pressed
                    pressed.append(["up", initialPos - 500, False])  # records the distance of the intialPos variable from the bottom of the screen
                    draw.append([upArrow, 40])
                elif event.key == pygame.K_LEFT:
                    pressed.append(["left", initialPos - 500, False])
                    draw.append([leftArrow, 40])
                elif event.key == pygame.K_DOWN:
                    pressed.append(["down", initialPos - 500, False])
                    draw.append([downArrow, 40])
                elif event.key == pygame.K_RIGHT:
                    pressed.append(["right", initialPos - 500, False])
                    draw.append([rightArrow, 40])

        initialPos += speed
        for arrow in draw:
            if arrow[0] == upArrow:
                screen.blit(upArrow, (400, arrow[1]))
            if arrow[0] == leftArrow:
                screen.blit(leftArrow, (500, arrow[1]))
            if arrow[0] == downArrow:
                screen.blit(downArrow, (600, arrow[1]))
            if arrow[0] == rightArrow:
                screen.blit(rightArrow, (700, arrow[1]))
        
        draw = list(map(lambda x: [x[0], x[1] + speed], draw))
    
        if draw:
            if draw[0][1] >= 600:
                draw.pop(0)
        pygame.display.update()

    print(pressed)  # prints the required information on screen