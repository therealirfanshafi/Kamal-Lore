import pygame
import os
pygame.init()

screen = pygame.display.set_mode((800, 600))

def ending():  # this module is for the ending seqeunce of the game. It works in the exact same way as the opening, just without the skipping ability, so most of the code is copied
    absolute_path = os.path.dirname(__file__)
    pygame.mixer.music.load(os.path.join(absolute_path, "Music/VOJ, Narvent - Memory Reboot.mp3"))
    clock = pygame.time.Clock()
    font = pygame.font.Font("freesansbold.ttf", 32)

    credits = (["CONGRATULATIONS"],
            ['You have completed the game'],
            ['Credits Time'],
            ['Written using python', "With the pygame package"],
            ['IDE used: VSCode'],
            ['Image Credits:','Arrow keys for rythm from flaticon.com','Other background images moslty from', 'freepik.com', "Other images were gathered by many of you"],
            ['Music Credits:', 'Opening: Avatar The last Airbender Intro', "Main Menu: Halo Theme Song", "Overworld: Deltarune Ch1 - Field of Hopes and", "Dreams", "Game: Running in the 90s", "Dance: ALL MY FELLAS"],
            ["Shop: Deltarune Ch2 - Pandora Palace", "Tutorial: OverSave-Tale - Bullet Hell", "Jiraya: Naruto Theme - The Raising Fighting", "Spirit", "Pitbull: Underverse - Overwrite", "Rock: Undertale The Final Run - Undyne the", "Undying Boss Theme"],
            ["Irfan: Undertale Last Breath - An Enigmatic", "Encounter", "Boss Loss: Glitchtale - Medley for a broken sky", "Game/dance sucess: GTA SA mission passed", "theme", "Ending theme: VOJ, Narvent - Memory Reeboot"],
            ["Thats it for the credits", "Thank you so much for playing this mess of a", "game", "I worked very hard on this so hope you enjoyed", "It almost took 1900 lines of code to write this", "game"],
            ["The screen wil remain like this till the music ends", "Then it will automatically close", "Cuz this is some good music innit"]
            )
    
    pygame.mixer.music.play()
    for text in credits:  
        clock.tick(30)
        current_line = text[0]  
        lines_drawn = list()  
        i=0 
        while text:  
            clock.tick(30)
            screen.fill((0, 0, 0))
        
            current_height = 10 
            for line in lines_drawn: 
                text_rendered = font.render(line, True, (255, 255, 255))
                screen.blit(text_rendered, (20, current_height))
                current_height += 40
            
            text_rendered = font.render(current_line[:i], True, (255, 255, 255)) 
            screen.blit(text_rendered, (20, current_height))
            pygame.time.delay(100)  
            if current_line[:i] == current_line:  
                lines_drawn.append(text.pop(0))  
                i = 0  
                if text:
                    current_line = text[0] 
            else:
                i += 1
            

            pygame.display.update()
        pygame.time.delay(300)
    pygame.time.delay(95 * 1000)
    pygame.mixer.music.stop()
