from time import sleep
import os
import math

class Game:
    def __init__(self):
        self.player_experience = 0
        self.highscore = 0

    def add_experience(self,value):
        self.player_experience += value

    
#create a class called human
class Human:
    ##initialise human with properties health,hunger,thirst,energy,boredom,age,happiness,cleanliness,name all are set to 100
    def __init__(self):
        self.positive_stats = {"health":100, "happiness":100, "cleanliness":100, "energy":100}
        self.negative_stats = {"hunger":0, "thirst":0,"boredom":0}
        self.age = 0
        self.name = "man"
        self.alive = True
        self.inventory = []

    def set_health(self, value = 0):
        for stat_key,stat_value in self.negative_stats.items():
            if stat_value > 80:
                self.use_item(stat_key)
                self.positive_stats["health"] -= 1 + value
                
        
        for stat_key,stat_value in self.positive_stats.items():
            if stat_value < 20:
                self.use_item(stat_key)
                if stat_key != "health":
                    self.positive_stats["health"] -= 1 + value
                    

    def set_hunger(self, value = 0):
        self.negative_stats["hunger"] += 1*self.age + value

    def set_thirst(self, value = 0):
        self.negative_stats["thirst"] += 6*self.age + value

    def set_energy(self, value = 0):
        self.positive_stats["energy"] -= 1*self.age + value

    def set_boredom(self, value = 0):
        self.negative_stats["boredom"] += 3*self.age + value

    def set_happiness(self, value = 0):
        self.positive_stats["happiness"] -= 1*self.age + value

    def set_cleanliness(self, value = 0):
        self.positive_stats["cleanliness"] -= 1*self.age + value
    
    def set_age(self, value = 0):
        self.age += 0.1 + value

    def set_stats(self):
        self.set_health()
        self.set_hunger()
        self.set_thirst()
        self.set_energy()
        self.set_boredom()
        self.set_happiness()
        self.set_cleanliness()
        self.set_age()
    
    def check_death(self):
        print()
        for stat_value in self.positive_stats.values():
            if stat_value <= 0:
                print("the man has died")
                game.add_experience(math.floor(self.age))
                self.alive = False
        for stat_value in self.negative_stats.values():
            if stat_value >= 100:
                print("the man has died")
                game.add_experience(math.floor(self.age))
                self.alive = False

    def show_stats(self):
        for stat_key,stat_value in self.positive_stats.items():
            if stat_value < 0:
                print("\033[31m"+stat_key+" "+str(round(stat_value))+"\033[0m")
            else:
                print(stat_key+" "+str(round(stat_value)))
            
        for stat_key,stat_value in self.negative_stats.items():
            if stat_value > 100:
                print("\033[31m"+stat_key+" "+str(round(stat_value))+"\033[0m")
            else:
                print(stat_key+" "+str(round(stat_value)))
        print("Age:"+ str(math.floor(self.age)))

    def use_item(self,attribute):
        for item in self.inventory:
            if attribute in self.positive_stats:
                if item[1] == attribute:
                    self.positive_stats[attribute] += item[2]
                    self.inventory.remove(item)
                    print("the man used a "+item[0]+" to increase "+item[1]+" by "+str(item[2]))
                    sleep(1)
            elif attribute in self.negative_stats:
                if item[1] == attribute:
                    self.negative_stats[attribute] -= item[2]
                    self.inventory.remove(item)
                    print("the man used a "+item[0]+" to decrease "+item[1]+" by "+str(item[2]))     
                    sleep(1)                       

class Item_creator:
    def __init__(self):
        self.name = "item"
        self.attribute = "attribute"
        self.value = 0
        self.condition = "condition"
        
    def create_item(self):
        self.name = input("enter item name: ")
        self.attribute = input("enter attribute: ")
        self.value = int(input("enter value: "))
        self.add_item_to_inventory()

    def add_item_to_inventory(self):
        man.inventory.append([self.name,self.attribute,self.value])  
        print (man.inventory) 
    

man = Human()
game = Game()
item_creator = Item_creator()

def loop():
    while man.alive == True:
        os.system('cls')
        man.set_stats()
        man.show_stats()
        man.check_death()
        sleep(0.5)


item_creator.create_item()
loop()


print("")
input("press enter to exit")
