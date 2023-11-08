import pygame
pygame.init()

screen = pygame.display.set_mode((800, 600))

def display_health_and_energy(current_health, max_health, energy):  # self explanatory procedure used to draw the health bar in the corner in the overworld
    font = pygame.font.Font("freesansbold.ttf", 16)
    player_health_bar = pygame.Rect(10, 10, max_health * 3, 10)
    player_current_health_rect = pygame.Rect(10, 10, current_health * 3, 10) 
    player_health_display = font.render(f"Your health: {round(current_health, 1)}", True, (255, 255, 255))  
    player_energy_display = font.render(f"Your Energy: {int(energy)} points", True, (255, 255, 255))
    screen.blit(player_health_display, (10, 30)) 
    screen.blit(player_energy_display, (10, 50)) 
    pygame.draw.rect(screen, (255, 0, 0), player_health_bar)
    pygame.draw.rect(screen, (0, 255, 0), player_current_health_rect)
