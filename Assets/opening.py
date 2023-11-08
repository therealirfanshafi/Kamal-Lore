import pygame
import os
pygame.init()

screen = pygame.display.set_mode((800, 600))

def opening():  # this module is for the opening sequence of the game
    absolute_path = os.path.dirname(__file__)
    pygame.mixer.music.load(os.path.join(absolute_path, "Music/Avatar The Last Airbender Intro Edited.mp3"))
    clock = pygame.time.Clock()
    font = pygame.font.Font("freesansbold.ttf", 32)
    skipped = False  # flag to check if the intro has been skipped or not

    # the commented part of this code was used to generate the text - wrapped tuple of arrays. It uses the same logic as it did in the fight dialogue, just with the font and width of wrapping changed
    """
    lore = ["Kamal",
            "Jiraya",
            "Pitbull",
            "Dwayne the Rock Johnson",
            "Long ago the 4 friends lived together enjoying their lives together",
            "But then everything changed when Irfan attacked",
            "Irfan had some beef with the group",
            "So he slowly spread lies to the group memembers about Kamal so that they would begin to hate him ",
            "\"Did you know Kamal talks bad about you behind your backs\" and such he said",
            "Surprisingly, Irfan's plan worked; they believed these lies",
            "They sought out for Kamal's blood",
            "Kamal had no choice but to fight back",
            "As they were Kamal's precious friends, Kamal could not bring himself to destroy",
            "So I believe Kamal will clear his name"
    ]
    for text in lore:
        words = text.split()  # splits the text into an array of words 
        text_lines  = list()
        line = ""
        for word in words:
            if not(line):
                line = word
            else:
                newline = line + " " + word  # concatenates words to form a string
                if font.size(newline)[0] <= 700:
                    line = newline
                else:  # if the size of string exceeds the required width, this string is appended to the array
                    text_lines.append(line)
                    line = word
            if word == words[-1]:
                text_lines.append(line)
        # this esentially creates an array with each element representing a line of text corresponding to the width of the text bubbles
        print(text_lines)
    
    """
    escape_message = font.render("Press ESC to skip intro", True, (255, 255, 0))  # gives users the information of being able to skip the intro by pressing escape

    # this tuple holds the opening lore for the game
    lore = (['Kamal'],
            ['Jiraya'],
            ['Pitbull'],
            ['Dwayne the Rock Johnson'],
            ['Long ago the 4 friends lived enjoying', 'their lives together'],
            ['But then everything changed when Irfan', 'attacked'],
            ['Irfan had some beef with the group'],
            ['So he slowly spread lies to the group', 'memembers about Kamal so that they', 'would begin to hate him'],
            ['"Did you know Kamal talks bad about you', 'behind your backs" and such he said'],
            ["Surprisingly, Irfan's plan worked; they", 'believed these lies without any question why', 'he would do such a thing'],
            ["They sought out for Kamal's blood"],
            ['Kamal had no choice but to fight back'],
            ["As they were Kamal's precious friends,", 'Kamal could not bring himself to destroy', 'them'],
            ['So I believe Kamal will clear his name'])
    
    pygame.mixer.music.play()
    for text in lore:  # this loop iterates through all elements in the tuple and displays them as it does in the fight dialogue module
        # this code is basically the same as the code in the fight dialogue module, just with the timings changes slightly. See the fight dialogue module for comments on specifics parts of this code
        clock.tick(30)
        current_line = text[0]  
        lines_drawn = list()  
        i=0 
        while text:  
            clock.tick(30)
            for event in pygame.event.get():  # this part is different from fight dialouge, it simply checks if the escape key was pressed or not and thus sets a flag to true which causes the loops to break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        skipped = True
            screen.fill((0, 0, 0))
            screen.blit(escape_message, (20, 10))
            current_height = 50 
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
            
            if skipped:  # loop breaks if skipped
                break

            pygame.display.update()
        if skipped:
            break
        pygame.time.delay(300)
    pygame.mixer.music.stop()
