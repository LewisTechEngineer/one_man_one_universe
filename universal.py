from time import sleep
import os
import math

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

    def use_items(self):
        for attribute in list(self.positive_stats.keys()) + list(self.negative_stats.keys()):
            for item in self.inventory:
                if item[1] == attribute and ((attribute in self.positive_stats and self.positive_stats[attribute] < 30) or (attribute in self.negative_stats and self.negative_stats[attribute] > 70)):
                    use_item = input(f"Use {item[0]}? [Y]es or [N]o ").lower()
                    if use_item == "y":
                        if attribute in self.positive_stats:
                            self.positive_stats[attribute] += item[2]
                        else:
                            self.negative_stats[attribute] -= item[2]
                        print(f"{self.name} used a {item[0]} to modify {item[1]} by {item[2]}")
                        self.inventory.remove(item)
                        break

    def show_stats(self):
        for stat, value in self.positive_stats.items():
            print(f"{stat} {round(value)}")
        for stat, value in self.negative_stats.items():
            print(f"{stat} {round(value)}")
        print(f"Age: {math.floor(self.age)}")
        print(f"exp: {self.game.player_experience}")
        print()

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
            self.show_stats()

class ItemCreator:
    def __init__(self, game, man):
        self.game = game
        self.man = man
        self.name = "item"
        self.attribute = "attribute"
        self.strength = 0
        self.condition = "condition"

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def create_item(self):
        self.clear_screen()
        print("Current experience:", self.game.player_experience)
        print("Cost to create Item: 100 Exp")
        self.name = input("Enter item name: ")

        # Attribute selector menu
        print("Select attribute:")
        print("[He]alth, [Ha]ppiness, [C]leanliness, [E]nergy, [H]unger, [T]hirst, [B]oredom")
        attribute_input = input("Enter attribute letter: ").strip().lower()

        attribute_map = {
            'he': 'health',
            'ha': 'happiness',
            'c': 'cleanliness',
            'e': 'energy',
            'h': 'hunger',
            't': 'thirst',
            'b': 'boredom'
        }

        while attribute_input not in attribute_map:
            print("Invalid attribute selection. Please try again.")
            attribute_input = input("Enter attribute letter: ").strip().lower()

        self.attribute = attribute_map[attribute_input]

        print("Enter strength (type 'M' for max, 'H' for half, or a number for strength):")
        print("Each point of strength requires 1 Exp")
        print("Current experience:", self.game.player_experience - ITEM_COST)
        strength_input = input("Enter strength: ").strip().lower()

        if strength_input == 'm':
            self.strength = self.game.player_experience - ITEM_COST
        elif strength_input == 'h':
            self.strength = (self.game.player_experience - ITEM_COST) // 2
        else:
            while True:
                try:
                    self.strength = int(strength_input)
                    break
                except ValueError:
                    print("Invalid strength input. Please try again.")
                    strength_input = input("Enter strength: ").strip().lower()

        required_experience = self.strength + ITEM_COST

        if required_experience > self.game.player_experience:
            print("Not enough experience to create this item.")
            return

        self.game.player_experience -= required_experience
        self.add_item_to_inventory()

    def add_item_to_inventory(self):
        self.man.inventory.append([self.name, self.attribute, self.strength])
        print(self.man.inventory)

class GameController:
    def __init__(self):
        self.game = Game()
        self.man = Human(self.game)
        self.item_creator = ItemCreator(self.game, self.man)

    def run(self):
        print("Welcome to the game")
        input("Press Enter to begin")
        self.game_loop()
        input("Press Enter to exit")

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
            self.man.show_stats()
            self.man.use_items()
            self.man.check_death()
            sleep(SLEEP_TIME)
        self.post_game_options()

    def post_game_options(self):
        self.man.reset_stats()

        option = input("[P]lay again, [C]reate item (cost 100 xp), [E]xit ").lower()

        while option not in ["p", "c", "e"]:
            print("Invalid option. Please try again.")
            option = input("[P]lay again, [C]reate item (cost 100 xp), [E]xit ").lower()

        if option == "p":
            self.man.alive = True
            self.game_loop()
        elif option == "c":
            self.item_creator.create_item()
            self.game_loop()
        elif option == "e":
            exit()

if __name__ == "__main__":
    game_controller = GameController()
    game_controller.run()
