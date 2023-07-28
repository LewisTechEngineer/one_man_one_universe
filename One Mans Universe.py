import pygame
import sys

pygame.init()

# Set up the display
display_width, display_height = 800, 600
display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Text Display Example')

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)

# Set the font and font size
font = pygame.font.Font(None, 36)

# Text content and initial values
hunger = 0
energy = 0
thirst = 0

# Function to render text
def display_text():
    text_hunger = font.render(f'Hunger: {hunger}', True, white)
    text_energy = font.render(f'Energy: {energy}', True, white)
    text_thirst = font.render(f'Thirst: {thirst}', True, white)

    # Display the text at the top-left corner (offset from the edges)
    display.blit(text_hunger, (10, 10))
    display.blit(text_energy, (10, 50))
    display.blit(text_thirst, (10, 90))

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Clear the screen
    display.fill(black)

    # Call the function to display text
    display_text()

    # Update the display
    pygame.display.update()