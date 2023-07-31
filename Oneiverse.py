from time import sleep
import pygame
import os
import math
import sys

# Constants
HEALTH_DECREASE = 0.5
HUNGER_INCREASE = 5
THIRST_INCREASE = 8
ENERGY_DECREASE = 4
BOREDOM_INCREASE = 3
HAPPINESS_DECREASE = 2
CLEANLINESS_DECREASE = 3
ITEM_COST = 100
EXPERIENCE_MULTIPLIER = 1
AGE_INCREASE = 0.1
SLEEP_TIME = 0.5
DISPLAY_DIMENSIONS = (800, 600)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 36
TEXT_OFFSET = 10


class Game:
    def __init__(self):
        self.player_experience = 0

    def add_experience(self, value):
        self.player_experience += value


class Human:
    def __init__(self, game):
        self.game = game
        self.name = "man"
        self.alive = True
        self.inventory = []
        self.reset_stats()

    def reset_stats(self):
        self.positive_stats = {"health": 100, "happiness": 100, "cleanliness": 100, "energy": 100}
        self.negative_stats = {"hunger": 0, "thirst": 0, "boredom": 0}
        self.age = 0

    def update_stat(self, stat, value=0, positive=True):
        stat_dict = self.positive_stats if positive else self.negative_stats
        stat_dict[stat] += value * self.age
        stat_dict[stat] = max(min(stat_dict[stat], 100), 0)

    def show_stats(self):
        stats = {}
        for stat, value in self.positive_stats.items():
            stats[stat] = round(value)
        for stat, value in self.negative_stats.items():
            stats[stat] = round(value)
        stats["Age"] = math.floor(self.age)
        stats["exp"] = self.game.player_experience
        return stats

    def check_death(self):
        for value in self.positive_stats.values():
            if value <= 0:
                self.alive = False
        for value in self.negative_stats.values():
            if value >= 100:
                self.alive = False
        if not self.alive:
            os.system('cls')
            print("the man has died")
            self.game.add_experience(math.floor(self.age))
            return True
        return False


class GameController:
    def __init__(self):
        self.game = Game()
        self.man = Human(self.game)
        self.stats = {}

        # Pygame initializations
        pygame.init()
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.display = pygame.display.set_mode(DISPLAY_DIMENSIONS)
        pygame.display.set_caption('Game UI')

    def update_display(self):
        self.display.fill(BLACK)

        y_offset = TEXT_OFFSET
        for stat, value in self.stats.items():
            text = self.font.render(f"{stat}: {value}", True, WHITE)
            self.display.blit(text, (TEXT_OFFSET, y_offset))
            y_offset += FONT_SIZE + TEXT_OFFSET

        pygame.display.update()

    def run(self):
        print("Welcome to the game")
        input("Press Enter to begin")
        self.game_loop()

    def game_loop(self):
        while self.man.alive:
            os.system('cls')

            # Update Health
            health_decrease = HEALTH_DECREASE + sum(0.2 for stat, value in self.man.negative_stats.items() if value > 50)
            health_decrease += sum(0.2 for stat, value in self.man.positive_stats.items() if stat != "health" and value < 30)
            self.man.update_stat("health", -health_decrease)

            # Update Hunger
            self.man.update_stat("hunger", HUNGER_INCREASE, False)

            # Update Thirst
            self.man.update_stat("thirst", THIRST_INCREASE, False)

            # Update Energy
            self.man.update_stat("energy", -ENERGY_DECREASE)

            # Update Boredom
            self.man.update_stat("boredom", BOREDOM_INCREASE, False)

            # Update Happiness
            happiness_decrease = HAPPINESS_DECREASE + sum(0.1 for stat, value in self.man.negative_stats.items() if value > 50)
            happiness_decrease += 0.1 if self.man.positive_stats["cleanliness"] < 40 else 0
            self.man.update_stat("happiness", -happiness_decrease)

            # Update Cleanliness
            self.man.update_stat("cleanliness", -CLEANLINESS_DECREASE)

            self.game.player_experience += EXPERIENCE_MULTIPLIER * self.man.age * 10

            # Update Age
            self.man.age += AGE_INCREASE

            # Display game stats
            self.stats = self.man.show_stats()
            self.update_display()

            if self.man.check_death():
                break

            # Process Pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            sleep(SLEEP_TIME)


if __name__ == "__main__":
    game_controller = GameController()
    game_controller.run()