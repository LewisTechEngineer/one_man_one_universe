from time import sleep
import os
import math

class Game:
    def __init__(self):
        self.player_experience = 0

    def add_experience(self,value):
        self.player_experience += value

class Human:
    def __init__(self):
        self.name = "man"
        self.alive = True
        self.inventory = []
        self.reset_stats()

    def reset_stats(self):
        self.positive_stats = {"health":100, "happiness":100, "cleanliness":100, "energy":100}
        self.negative_stats = {"hunger":0, "thirst":0,"boredom":0}
        self.age = 0

    def update_stat(self, stat, value=0, positive=True):
        if positive:
            self.positive_stats[stat] += value * self.age
        else:
            self.negative_stats[stat] += value * self.age
        # Ensure the stats don't go over their maximum or minimum values
        if stat in self.positive_stats:
            self.positive_stats[stat] = max(min(self.positive_stats[stat], 100), 0)
        else:
            self.negative_stats[stat] = max(min(self.negative_stats[stat], 100), 0)

    def use_items(self):
        for attribute in self.positive_stats:
            for item in self.inventory:
                if item[1] == attribute and self.positive_stats[attribute] < 30:
                    use_item = input(f"Use {item[0]}? [Y]es or [N]o ").lower()
                    if use_item == "y":
                        self.positive_stats[attribute] += item[2]
                        print(f"{self.name} used a {item[0]} to increase {item[1]} by {item[2]}")
                        self.inventory.remove(item)
                        break

        for attribute in self.negative_stats:
            for item in self.inventory:
                if item[1] == attribute and self.negative_stats[attribute] > 70:
                    use_item = input(f"Use {item[0]}? [Y]es or [N]o ").lower()
                    if use_item == "y":
                        self.negative_stats[attribute] -= item[2]
                        print(f"{self.name} used a {item[0]} to decrease {item[1]} by {item[2]}")
                        self.inventory.remove(item)
                        break


    def show_stats(self):
        for stat, value in self.positive_stats.items():
            print(f"{stat} {round(value)}")
        for stat, value in self.negative_stats.items():
            print(f"{stat} {round(value)}")
        print(f"Age: {math.floor(self.age)}")
        print(f"exp: {game.player_experience}")
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
            game.add_experience(math.floor(self.age))
            self.show_stats()
            
class ItemCreator:
    def __init__(self):
        self.name = "item"
        self.attribute = "attribute"
        self.strength = 0
        self.condition = "condition"

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def create_item(self):
        self.clear_screen()

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

        if attribute_input not in attribute_map:
            print("Invalid attribute selection. Please try again.")
            self.create_item()

        self.attribute = attribute_map[attribute_input]

        print("Enter strength (type 'M' for max or 'H' for half):")
        strength_input = input("Enter strength: ").strip().lower()

        if strength_input == 'm':
            self.strength = game.player_experience 
        elif strength_input == 'h':
            self.strength = game.player_experience / 2
        else:
            try:
                self.strength = int(strength_input)
            except ValueError:
                print("Invalid strength input. Please try again.")
                self.create_item()

        required_experience = self.strength
        
        if required_experience > game.player_experience:
            print("Not enough experience to create this item.")
            return

        game.player_experience -= required_experience
        self.add_item_to_inventory()

    def add_item_to_inventory(self):
        man.inventory.append([self.name, self.attribute, self.strength])
        print(man.inventory)

def game_loop():
    while man.alive:
        os.system('cls')

        # Update Health
        health_decrease = 0.5 + sum(0.2 for stat, value in man.negative_stats.items() if value > 50)
        health_decrease += sum(0.2 for stat, value in man.positive_stats.items() if stat != "health" and value < 30)
        man.update_stat("health", -health_decrease)

        # Update Hunger
        man.update_stat("hunger", 5, False)

        # Update Thirst
        man.update_stat("thirst", 8, False)

        # Update Energy
        man.update_stat("energy", -4)

        # Update Boredom
        man.update_stat("boredom", 3, False)

        # Update Happiness
        happiness_decrease = 2 + sum(0.1 for stat, value in man.negative_stats.items() if value > 50)
        happiness_decrease += 0.1 if man.positive_stats["cleanliness"] < 40 else 0
        man.update_stat("happiness", -happiness_decrease)

        # Update Cleanliness
        man.update_stat("cleanliness", -3)

        game.player_experience += 1

        # Update Age
        man.age += 0.1
        man.show_stats()
        man.use_items()
        man.check_death()
        sleep(0.5)
    post_game_options()

def post_game_options():
    man.reset_stats()
    option = input("[P]lay again, [C]reate item, [E]xit ").lower()

    if option == "p":
        man.alive = True
        game_loop()
    elif option == "c":
        item_creator.create_item()
        game_loop()
    elif option == "e":
        exit()

man = Human()
game = Game()
item_creator = ItemCreator()

print("Welcome to the game")
input("press enter to begin")
game_loop()
input("press enter to exit")
