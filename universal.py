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
SLEEP_TIME = 0.1

class Game:
    def __init__(self):
        self.player_experience = 0
        self.saved_items = []

    def add_experience(self, value):
        self.player_experience += value

    def save_item(self, name, attribute, strength):
        self.saved_items.append((name, attribute, strength))

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
        self.game.add_experience(math.floor(1 * EXPERIENCE_MULTIPLIER * self.age))

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

    def load_item(self):
        print("Select item to load:")
        for i, item in enumerate(self.game.saved_items):
            print(f"[{i}] {item[0]}")
        item_index = input("Enter item number: ").strip().lower()
        while not item_index.isdigit() or int(item_index) >= len(self.game.saved_items):
            print("Invalid item selection. Please try again.")
            item_index = input("Enter item number: ").strip().lower()
        self.name, self.attribute, self.strength = self.game.saved_items[int(item_index)]
        # add item to player inventory

    def create_item(self):
        self.clear_screen()
        print("Current experience:", self.game.player_experience)
        print("Cost to create Item: 100 Exp")
        if len(self.game.saved_items) > 0:
            load_item = input("Load item? [Y]es or [N]o ").lower()
            if load_item == "y":
                self.load_item()
        
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
            if self.game.player_experience - ITEM_COST < 70:
                self.strength = self.game.player_experience - ITEM_COST
            else:
                self.strength = 70
        elif strength_input == 'h':
            if self.game.player_experience - ITEM_COST < 35:
                self.strength = (self.game.player_experience - ITEM_COST) // 2
            else:
                self.strength = 35
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
        if self.game.player_experience >= 10:
            save_item = input("Save item? [Y]es or [N]o (10 exp) ").lower()
            if save_item == "y":
                self.game.player_experience -= 10
                self.game.save_item(self                .name, self.attribute, self.strength)

    def add_item_to_inventory(self):
        self.man.inventory.append((self.name, self.attribute, self.strength))
        print(f"Item {self.name} created and added to inventory!")

def game_loop():
    game = Game()
    man = Human(game)
    item_creator = ItemCreator(game, man)
    
    
    print("Options:")
    print("[1] Create Item")
    print("[2] Create Life")
    option = input("Choose an option: ").strip()

    if option == "1":
        item_creator.create_item()
    elif option == "2":
        while man.alive:
            man.use_items()
            man.update_stat("health", -HEALTH_DECREASE)
            man.update_stat("hunger", HUNGER_INCREASE, positive=False)
            man.update_stat("thirst", THIRST_INCREASE, positive=False)
            man.update_stat("energy", -ENERGY_DECREASE)
            man.update_stat("boredom", BOREDOM_INCREASE, positive=False)
            man.update_stat("happiness", -HAPPINESS_DECREASE)
            man.update_stat("cleanliness", -CLEANLINESS_DECREASE)
            man.age += AGE_INCREASE
            man.show_stats()
            sleep(SLEEP_TIME)
            os.system('cls' if os.name == 'nt' else 'clear')
            man.check_death()
    else:
        print("Invalid option! Please try again.")
    
    print("Game Over!")
    print(f"Final experience: {game.player_experience}")
    game_loop()

    

if __name__ == "__main__":
    game_loop()

