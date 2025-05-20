import time
import sys

#!/usr/bin/env python3

# ASCII art for items
SWORD_ART = r"""
    /\
     /  \
    |    |   ⚔ SWORD OF LIGHT ⚔
    | () |
    |____|
"""
SHIELD_ART = r"""
   __________
  / ________ \
 / /########\ \
( (  SHIELD  ) )
 \ \########/ /
  \________/
"""
POTION_ART = r"""
   ______
  / ____ \
 | |    | |  ✦ POTION OF HEALING ✦
  \______/ 
"""

class Game:
    def __init__(self):
      self.inventory = {}
      self.current_location = "start"
      self.game_over = False

    def delay_print(self, s, delay=0.05):
      for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(delay)
      print()

    def show_intro(self):
      intro_text = """
Welcome to the Grand Adventure!

You find yourself at the beginning of an epic journey. 
Your commands will shape your destiny in this world full of mystery,
treasure, and danger.

Type 'help' to see available commands.
"""
      self.delay_print(intro_text, delay=0.02)

    def show_help(self):
      help_text = """
Available commands:
  - look: Describe your current surroundings.
  - go [direction/place]: Move to a new location. Options depend on your location.
  - inventory: Show items in your inventory.
  - take [item]: Pick up an item if available.
  - use [item]: Use an item from your inventory.
  - help: Show this help message.
  - quit: Exit the game.
"""
      print(help_text)

    def show_inventory(self):
      if not self.inventory:
        print("Your inventory is empty.")
        return

      print("Your Inventory:")
      for key, item in self.inventory.items():
        print(f" - {key}")
        print(item["art"])
      print()

    def process_command(self, command):
      command = command.strip().lower()
      if command == "":
        return

      if command == "help":
        self.show_help()
      elif command == "inventory":
        self.show_inventory()
      elif command == "look":
        self.describe_location()
      elif command.startswith("go "):
        loc = command[3:]
        self.change_location(loc)
      elif command.startswith("take "):
        item = command[5:]
        self.attempt_take(item)
      elif command.startswith("use "):
        item = command[4:]
        self.attempt_use(item)
      elif command == "quit":
        print("Farewell, brave adventurer!")
        self.game_over = True
      else:
        print("Unknown command. Type 'help' for a list of commands.")

    def describe_location(self):
      if self.current_location == "start":
        text = """
You stand at a crossroads under a vast sky. 
Paths lead to a mysterious forest, a looming castle, 
and a quiet village.
        """
        print(text)
      elif self.current_location == "forest":
        text = """
The forest is dense with towering trees and lurking sounds.
The sunlight barely reaches the ground. You sense danger and opportunity.
There is a glint near a bush. It might be a sword.
        """
        print(text)
      elif self.current_location == "castle":
        text = """
The castle stands proud but abandoned. Dust covers the marble halls.
You see remnants of battles and faded heraldry. 
A guard's ghost may be waiting to challenge you.
        """
        print(text)
      elif self.current_location == "village":
        text = """
The quiet village is full of peculiar characters.
There is a marketplace with various goods and whispers of secret quests.
An old man beckons you to his hut.
        """
        print(text)
      elif self.current_location == "secret_grotto":
        text = """
You have discovered a secret grotto hidden behind a waterfall.
Mysterious runes cast a glow on ancient relics.
        """
        print(text)
      else:
        print("There's nothing noteworthy here.")

    def change_location(self, destination):
      valid_destinations = {
        "start": "start",
        "forest": "forest",
        "castle": "castle",
        "village": "village",
        "grotto": "secret_grotto",
        "secret": "secret_grotto"
      }

      if destination in valid_destinations:
        self.current_location = valid_destinations[destination]
        print(f"You travel to the {destination}...\n")
        self.describe_location()

        # Special events on arrival
        if self.current_location == "forest" and "sword" not in self.inventory:
            print("You notice a shining object partially buried in leaves.")
        if self.current_location == "castle":
            print("A ghostly figure appears in the distance!")
        if self.current_location == "village":
            print("Villagers greet you with nods and murmurs.")
      else:
        print("You cannot go there.")

    def attempt_take(self, item):
      if self.current_location == "forest" and item == "sword" and "sword" not in self.inventory:
        print("You pick up the shining sword!")
        self.inventory["sword"] = {"art": SWORD_ART, "description": "A radiant sword that glows with an inner light."}
      elif self.current_location == "castle" and item == "shield" and "shield" not in self.inventory:
        print("You salvage a sturdy shield from the castle ruins!")
        self.inventory["shield"] = {"art": SHIELD_ART, "description": "An old, yet reliable shield, bearing the insignia of a forgotten order."}
      elif self.current_location == "village" and item == "potion" and "potion" not in self.inventory:
        print("A kind villager hands you a healing potion!")
        self.inventory["potion"] = {"art": POTION_ART, "description": "A potion that sparkles with mysterious energies."}
      else:
        print("There's nothing like that to take here.")

    def attempt_use(self, item):
      if item not in self.inventory:
        print("You don't have that item.")
        return

      if item == "potion":
        print("You drink the potion and feel rejuvenated!")
        # Once used, remove potion from inventory.
        del self.inventory["potion"]
      elif item == "sword":
        print("You swing your sword valiantly, ready to face any foe!")
      elif item == "shield":
        print("You raise your shield to brace against incoming attacks!")
      else:
        print("You try to use it, but nothing happens.")

    def run(self):
      self.show_intro()
      while not self.game_over:
        command = input("> ")
        self.process_command(command)

def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    main()