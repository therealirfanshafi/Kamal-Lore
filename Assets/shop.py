import pygame
import os
from display_health_and_energy import display_health_and_energy
pygame.init()

screen = pygame.display.set_mode((800, 600))

absolute_path = os.path.dirname(__file__)

def shop(player):  # this module is used to implement the shop in the game to upgrade the player, it takes the player object as a parameter

    #loading of images
    shop_image = pygame.transform.scale_by(pygame.image.load(os.path.join(absolute_path, "Images/shop.jpg")), 800/2000)  # background image
    # the menu black boxes at the bottom
    left_dialogue_box = pygame.image.load(os.path.join(absolute_path, "Images/shop_left_dialogue_box.png"))
    right_dialogue_box = pygame.image.load(os.path.join(absolute_path, "Images/shop_right_dialogue_box.png"))
    shopkeeper = pygame.transform.scale_by(pygame.image.load(os.path.join(absolute_path, "Images/maher.png")), 0.75)
    speech_bubble = pygame.transform.scale_by(pygame.image.load(os.path.join(absolute_path, "Images/conversation.png")), 0.1)

    pygame.mixer.music.load(os.path.join(absolute_path, "Music/Pandora Palace.mp3"))  # music to be used as the bgm of the shop

    font = pygame.font.Font("freesansbold.ttf", 32)  # font for the item display
    font1 = pygame.font.Font("freesansbold.ttf", 16)  # font for the shopkeeper's speech

    clock = pygame.time.Clock()
    
    # static texts are rendered outside the loop
    
    # description of the options in the bottom menu
    buy_description = font.render("Buy things from the store", True, (255, 255, 255))
    leave_description = font.render("Return to the overworld", True, (255, 255, 255))
    heal_description = font.render("Restore full health", True, (255, 255, 255))
    def_factor_description = (font.render("Reduce the damage taken", True, (255, 255, 255)), font.render("from bosses by some percent", True, (255, 255, 255)))  # some of these descriptions are tuples to implement word wrapping as they cannot fit into a single line
    heal_factor_description = (font.render("Increase the value by which ", True, (255, 255, 255)), font.render("health increases in succesful", True, (255, 255, 255)), font.render("evading of boss attacks", True, (255, 255, 255)))
    max_health_description = (font.render("Increase the maximum limit", True, (255, 255, 255)), font.render("of health", True, (255, 255, 255)))
    back_description = font.render("Return to previous menu", True, (255, 255, 255))
    maxed_out = font.render("Category maxed out", True, (255, 255, 255))  # displayed when a item is at its maximum state

    running = True  # flag is set to false when the user leaves the shop
    option = [0, 0]  # an array of integers, each integer represents the option number of state 0 and 1 respecitvely the user is currently on
    state = 0  # this variable represents the state which the menu is on i.e it is used to change which menu options are displayed
    i = 0  # this variable is used to display the characters one by one when the shopkeeper's dialogue is displayed
    out_of_energy = False  # this flag variable is set to True whenever the user presses enter to buy something but they do not have enough energy points to buy said item
    pygame.mixer.music.play(-1)
    while running:  # main loop
        clock.tick(30)  # maintains 30 FPS

        # calculation of the price of the different items based on the current level it is in
        heal_price = 5
        max_health_price = int(player.max_health + 20)
        def_factor_price = int(round((player.def_factor + 0.1) * 200, 0))
        heal_factor_price = int((player.heal_factor) * 30)

        for event in pygame.event.get(): # used to check for key presses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s: 
                    option[state] += 1  # the option number is incremented if the down key is pressed
                    out_of_energy = False
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    option[state] -= 1  # the option number is decremented if the up key is pressed
                    out_of_energy = False  # this flag is set to false every time the option is changed
                if event.key == pygame.K_RETURN:  # performs different actions based on the pressing of the enter key
                    if state == 0:  # checks for menu state
                        if option[0] == 1:  # quits if the enter is pressed on leave
                            running = False
                        elif option[0] == 0:
                            state = 1  # goes to the 2nd menu if enter is pressed on buy
                    elif state == 1:
                        if option[1] == 4:  # goes to the previous menu if enter is pressed on back
                            option[1] = 0
                            state = 0
                        elif option[1] == 0:  
                            if player.current_health != player.max_health and player.energy >= heal_price:  # heals the player if the enter is pressed on heal, the player already is not at full health and the player has enough currency to do so
                                player.current_health = player.max_health
                                player.energy -= heal_price  # deduction energy by the price
                            elif player.energy < heal_price:
                                out_of_energy = True  # sets the flag as True if there is not enough energy to buy the desired product
                        elif option[1] == 1:  # rest of the options work in a similar way
                            if player.def_factor < 0.5 and player.energy >= def_factor_price:
                                player.def_factor += 0.1
                                player.energy -= def_factor_price
                            elif player.energy < def_factor_price:
                                out_of_energy = True
                        elif option[1] == 2:
                            if player.heal_factor < 4 and player.energy >= heal_factor_price:
                                player.heal_factor += 1
                                player.energy -= heal_factor_price
                            elif player.energy < heal_factor_price:
                                out_of_energy = True
                        elif option[1] == 3:
                            if player.max_health < 100 and player.energy >= max_health_price:
                                player.max_health += 20
                                player.current_health = player.max_health
                                player.energy -= max_health_price
                            elif player.energy < max_health_price:
                                out_of_energy = True
                        
        # draws the layout of the shop
        screen.blit(shop_image, (0,-350))
        screen.blit(left_dialogue_box, (0, 350))
        screen.blit(right_dialogue_box, (500, 350))
        screen.blit(shopkeeper, (325, 29))

        display_health_and_energy(player.current_health, player.max_health, player.energy)  # self explanatory procedure

        if out_of_energy:  # if this flag has been set to True, the shopkeeper gives a dialogue of the player not having enough energy to purchase an item
            screen.blit(speech_bubble, (500, 29))
            screen.blit(font1.render("Not enough energy"[:i], True, (0, 0, 0)), (520, 45))
            i += 1
            pygame.time.delay(50)
            if i > 30:
                i = 0
                out_of_energy = False  # stops displaying the message once all of it has been displayed 

        if state == 0:  # displays the options in the menu along with an explanation of each option (all conditions work in basically the same way)
            if option[0] == 0:  # yellows the text which option is currently on
                buy = font.render("Buy", True, (255, 255, 0))
                leave = font.render("Leave", True, (255, 255, 255))
                screen.blit(buy_description, (20, 370))
            elif option[0] == 1:
                buy = font.render("Buy", True, (255, 255, 255))
                leave = font.render("Leave", True, (255, 255, 0))
                screen.blit(leave_description, (20, 370))

            screen.blit(buy, (520, 370))
            screen.blit(leave, (520, 415))

            if option[0] < 0:  # ensures that the options of state 0 are only 0 and 1
                option[0] = 1
            elif option[0] > 1:
                option[0] = 0
        else:
            if option[1] == 0:
                screen.blit(heal_description, (20, 370))
                if player.current_health < player.max_health:
                    screen.blit(font.render(f"Price: {int(heal_price)} energy points", True, (255, 255, 255)), (20, 550))
                else:
                    screen.blit(maxed_out, (20, 550))  
                
                heal = font.render("Heal", True, (255, 255, 0))
                defence_factor = font.render("Defence Factor", True, (255, 255, 255))
                heal_factor = font.render("Heal Factor", True, (255, 255, 255))
                max_health = font.render("Max Health", True, (255, 255, 255))
                back = font.render("Back", True, (255, 255, 255))
            elif option[1] == 1:
                screen.blit(def_factor_description[0], (20, 370))
                screen.blit(def_factor_description[1], (20, 415))
                if player.def_factor < 0.5:  # displays the upgrade info and price of upgrade
                    screen.blit(font.render(f"From: {int(player.def_factor*100)}% to {int((player.def_factor+0.1)*100)}%", True, (255, 255, 255)), (20, 505))
                    screen.blit(font.render(f"Price: {int(def_factor_price)} energy points", True, (255, 255, 255)), (20, 550))
                else:
                    screen.blit(maxed_out, (20, 550))  # displays a max out message if the item is maxed out
                
                heal = font.render("Heal", True, (255, 255, 255))
                defence_factor = font.render("Defence Factor", True, (255, 255, 0))
                heal_factor = font.render("Heal Factor", True, (255, 255, 255))
                max_health = font.render("Max Health", True, (255, 255, 255))
                back = font.render("Back", True, (255, 255, 255))
            elif option[1] == 2:
                screen.blit(heal_factor_description[0], (20, 370))
                screen.blit(heal_factor_description[1], (20, 415))
                screen.blit(heal_factor_description[2], (20, 460))
                if player.heal_factor < 4:
                    screen.blit(font.render(f"From: {int(player.heal_factor)} to {int((player.heal_factor + 1))}", True, (255, 255, 255)), (20, 505))
                    screen.blit(font.render(f"Price: {int(heal_factor_price)} energy points", True, (255, 255, 255)), (20, 550))
                else:
                    screen.blit(maxed_out, (20, 550))

                heal = font.render("Heal", True, (255, 255, 255))
                defence_factor = font.render("Defence Factor", True, (255, 255, 255))
                heal_factor = font.render("Heal Factor", True, (255, 255, 0))
                max_health = font.render("Max Health", True, (255, 255, 255))
                back = font.render("Back", True, (255, 255, 255))
            elif option[1] == 3:
                screen.blit(max_health_description[0], (20, 370))
                screen.blit(max_health_description[1], (20, 415))
                if player.max_health < 100:
                    screen.blit(font.render(f"From: {int(player.max_health)} to {int((player.max_health + 20))}", True, (255, 255, 255)), (20, 505))
                    screen.blit(font.render(f"Price: {int(max_health_price)} energy points", True, (255, 255, 255)), (20, 550))
                else:
                    screen.blit(maxed_out, (20, 550))
                
                heal = font.render("Heal", True, (255, 255, 255))
                defence_factor = font.render("Defence Factor", True, (255, 255, 255))
                heal_factor = font.render("Heal Factor", True, (255, 255, 255))
                max_health = font.render("Max Health", True, (255, 255, 0))
                back = font.render("Back", True, (255, 255, 255))
            else:
                screen.blit(back_description, (20, 370))
                
                heal = font.render("Heal", True, (255, 255, 255))
                defence_factor = font.render("Defence Factor", True, (255, 255, 255))
                heal_factor = font.render("Heal Factor", True, (255, 255, 255))
                max_health = font.render("Max Health", True, (255, 255, 255))
                back = font.render("Back", True, (255, 255, 0))

            if option[1] < 0:  # ensures that the options of state 1 are only 0 to 4 inclusive
                option[1] = 4
            if option[1] > 4:
                option[1] = 0

            screen.blit(heal, (520, 370))
            screen.blit(defence_factor, (520, 415))
            screen.blit(heal_factor, (520, 460))
            screen.blit(max_health, (520, 505))
            screen.blit(back, (520, 550))
        pygame.display.update()
    pygame.mixer.music.stop()
    

# this part is only for testing the module and does not serve any other function
if __name__ == "__main__":
    class Player:
        def __init__(self, current_health, max_health, def_factor, heal_factor, energy):
            self.current_health = current_health
            self.max_health = max_health
            self.def_factor = def_factor
            self.heal_factor = heal_factor
            self.energy = energy
    p = Player(10, 20, 0, 1, 10)
    shop(p)
