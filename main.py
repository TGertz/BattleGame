from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random


# Create Black Magic
fire = Spell("Fire", 10, 100, "black")
thunder = Spell("Thunder", 10, 100, "black")
blizzard = Spell("Blizzard", 10, 100, "black")
meteor = Spell("Meteor", 20, 200, "black")
quake = Spell("Quake", 14, 140, "black")

# Create White Magic
cure = Spell("Cure", 12, 120, "white")
cura = Spell("Cura", 18, 200, "white")

# Create some Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 500 HP", 500)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
hielixer = Item("Hi-Elixer", "elixer", "Fully restores party's HP/MP", 9999)
drenade = Item("Grenade", "attack", "Deals 500 HP damage", 500)

player_spells = [fire, thunder, blizzard, meteor, quake, cure, cura]
player_items = [{"item": potion, "quantity": 15},
                {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5},
                {"item": elixer, "quantity": 5},
                {"item": hielixer, "quantity": 2},
                {"item": drenade, "quantity": 5}]

# Instantiate People
player1 = Person("Human :", 1000, 100, 100, 34, player_spells, player_items)
player2 = Person("Orch  :", 1500, 65, 200, 34, player_spells, player_items)
player3 = Person("Elf   :", 800, 200, 80, 34, player_spells, player_items)
enemy1 = Person("Troll :", 1100, 0, 80, 25, [], [])
enemy2 = Person("Queen :", 10000, 0, 60, 25, [], [])
enemy3 = Person("Undead:", 1200, 0, 50, 25, [], [])

players = [player1, player2, player3]
enemys = [enemy1, enemy2, enemy3]

running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!!!" + bcolors.ENDC)

while running:
    print("===================================")
    print("\n")

    for player in players:
        player.get_stats()
        print("\n")

    for enemy in enemys:
        enemy.enemy_get_stats()
        print("\n")

    for player in players:
        player.choose_action()
        choice = input("Choose action: ")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemys)
            enemys[enemy].take_damage(dmg)
            print(bcolors.FAIL + "You attacked the " + enemys[enemy].name + " for", dmg, "points of damage" + bcolors.ENDC)
        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("Choose magic power: ")) - 1

            if magic_choice == -1: # Press 0 to back
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + "heals for", str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == "black":
                enemy = player.choose_target(enemys)
                enemys[enemy].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage to " + enemys[enemy].name + bcolors.ENDC)
        elif index == 2:
            player.choose_item()
            item_choice = int(input("Choose item : ")) - 1

            if item_choice == -1: # Back
                continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "You don't have more items..." + bcolors.ENDC)

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP" + bcolors.ENDC)
            elif item.type == "elixer":
                player.hp = player.maxhp
                player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP" + bcolors.ENDC)
            elif item.type == "attack":
                enemy = player.choose_target(enemys)
                enemys[enemy].take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + "deals", str(item.prop), "points of damage to " + enemys[enemy].name + bcolors.ENDC)

    enemy_choice = 1
    target = random.randrange(0, 3)
    enemy_dmg = enemys[0].generate_damage()
    players[target].take_damage(enemy_dmg)
    print("Enemy attacks for", enemy_dmg)

    print("___________________________________________")

    defeated_players = 0
    defeated_enemys = 0

    for enemy in enemys:
        if enemy.get_hp() == 0:
            defeated_enemys += 1

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    if defeated_enemys == 2:
        print(bcolors.OKGREEN + "You Win!!!" + bcolors.ENDC)
        running = False
    elif defeated_players == 2:
        print(bcolors.FAIL + "Your enemies have defeated you!!!" + bcolors.ENDC)
        running = False
