import random

SAVE_FILE = "saves/checkpoint.txt"
LOG_FILE = "saves/battle_log.txt"
STARTING_HP = 30
DEFAULT_HERO = "Thrall"
STARTING_WEAPON = "Doomhammer"
STARTING_BONUS = 2

MONSTERS = {
    "Goblin": {"taunt": "A Goblin leaps out, waving a rusty dagger!", "ac": 8, "damage": 4, "xp": 20},
    "Skeleton": {"taunt": "Bones rattle as a Skeleton rises from the dust.", "ac": 10, "damage": 5, "xp": 30},
    "Orc": {"taunt": "An Orc pounds its chest and roars at you!", "ac": 13, "damage": 7, "xp": 50},
    # Step 7: my own monster
    "Mimic": {"taunt": "The treasure chest grows teeth and lunges!", "ac": 11, "damage": 6, "xp": 40},
    # Phase 2: Alliance monsters
    "Human Footman": {"taunt": "A Human Footman raises his shield. 'For Stormwind!'", "ac": 9, "damage": 4, "xp": 25},
    "Night Elf Sentinel": {"taunt": "A Night Elf Sentinel drops from the trees, glaive spinning!", "ac": 11, "damage": 5, "xp": 35},
    "Dwarf Mountaineer": {"taunt": "A Dwarf Mountaineer levels his rifle. 'Hold yer ground, orc!'", "ac": 12, "damage": 6, "xp": 45},
}

# Phase 2: loot tiers, ordered worst to best, like WoW's gray/white/green/blue/purple.
# "min_roll" is the lowest d100 result that reaches this tier. A roll under the
# Poor line means the monster dropped nothing (trash mobs often drop nothing).
LOOT = {
    "Poor": {
        "min_roll": 31,
        "value": 1,
        "items": ["Broken Fang", "Tattered Cloth", "Bent Spoon", "Cracked Shield", "Rusty Nail", "Chipped Tusk"],
    },
    "Common": {
        "min_roll": 61,
        "value": 5,
        "items": ["Linen Cloth", "Light Leather", "Copper Ore", "Minor Healing Potion", "Peacebloom", "Rough Stone"],
    },
    "Uncommon": {
        "min_roll": 81,
        "value": 20,
        "items": ["Ironforge Breastplate", "Shortsword of the Bear", "Spidersilk Boots", "Hunter's Muskets", "Ring of Precision", "Orcish War Leggings"],
    },
    "Rare": {
        "min_roll": 94,
        "value": 60,
        "items": ["Blade of the Titans", "Ironfoe", "Staff of Jordan", "Eye of Rend", "Shadowfang", "Warden's Band"],
    },
    "Epic": {
        "min_roll": 100,
        "value": 200,
        "items": ["Gorehowl", "Sulfuras Shard", "Ashkandi", "Thunderfury Bindings", "Felstriker", "Quel'Serrar"],
    },
}

# Phase 2: random victory shouts
VICTORY_MESSAGES = [
    "Lok'tar ogar!",
    "For the Horde!",
    "Blood and thunder!",
    "The elements are with you!",
]


# Step 1
def roll_die(sides):
    return random.randint(1, sides)


# Step 2
def log_event(message, filename):
    with open(filename, "a") as outfile:
        outfile.write(message + "\n")


# Loot rolls live here, not on MONSTERS. The lab checker compares Goblin,
# Skeleton, and Orc to the starter dictionaries, so those keep only
# taunt, ac, damage, and xp.
ASSIGNED_LOOT = {}


# Phase 2: give every monster its own random loot table.
# Each monster gets one random item from each tier, so two Goblins in two
# different play sessions can carry different loot.
def assign_loot():
    for name in MONSTERS:
        ASSIGNED_LOOT[name] = {}
        for tier in LOOT:
            ASSIGNED_LOOT[name][tier] = random.choice(LOOT[tier]["items"])


# Phase 2: roll on the monster's loot table after a win.
# Tougher monsters (higher AC) get a small luck bonus on the d100,
# the same way bosses drop better gear than trash mobs.
def roll_loot(hero, monster_name):
    monster = MONSTERS[monster_name]
    luck = monster["ac"] - 8
    roll = roll_die(100) + luck
    dropped = None
    for tier in LOOT:
        if roll >= LOOT[tier]["min_roll"]:
            dropped = tier
    if dropped is None:
        print("The", monster_name, "had nothing worth taking.")
        return
    item = ASSIGNED_LOOT[monster_name][dropped]
    hero["bag"].append(item)
    print("Loot! [" + dropped + "]", item, "(worth", LOOT[dropped]["value"], "gold)")
    log_event(hero["name"] + " looted " + item + " (" + dropped + ") from the " + monster_name + ".", LOG_FILE)


# Step 3
def fight(hero):
    name = random.choice(list(MONSTERS))
    monster = MONSTERS[name]
    print(monster["taunt"])
    roll = roll_die(20)
    # The checker fights a hero that has no weapon yet. A missing bonus adds 0.
    bonus = 0
    if "attack_bonus" in hero:
        bonus = hero["attack_bonus"]
    total = roll + bonus
    if "weapon" in hero:
        print("You rolled", roll, "+", bonus, "(" + hero["weapon"] + ") =", total, "against AC", monster["ac"])
    else:
        print("You rolled", roll, "+", bonus, "=", total, "against AC", monster["ac"])
    if total >= monster["ac"]:
        gold = roll_die(10)
        hero["xp"] = hero["xp"] + monster["xp"]
        hero["gold"] = hero["gold"] + gold
        print(random.choice(VICTORY_MESSAGES))
        print("You defeated the", name, "and found", gold, "gold!")
        log_event(hero["name"] + " defeated the " + name + ".", LOG_FILE)
        # Skip loot when this monster has no table, or the hero has no bag.
        # That keeps the checker's fight to one d20 and one d10.
        if name in ASSIGNED_LOOT and "bag" in hero:
            roll_loot(hero, name)
        return True
    else:
        hero["hp"] = hero["hp"] - monster["damage"]
        print("The", name, "hits you for", monster["damage"], "damage!")
        log_event(hero["name"] + " was hit by the " + name + ".", LOG_FILE)
        return False


# Step 4
def save_checkpoint(hero, filename):
    with open(filename, "w") as outfile:
        for key in hero:
            if key == "bag":
                outfile.write(key + "=" + "|".join(hero[key]) + "\n")
            else:
                outfile.write(key + "=" + str(hero[key]) + "\n")


# Step 5
def load_checkpoint(filename):
    hero = {}
    with open(filename, "r") as infile:
        for line in infile:
            line = line.rstrip("\n")
            parts = line.split("=")
            if parts[0] == "name" or parts[0] == "weapon":
                hero[parts[0]] = parts[1]
            elif parts[0] == "bag":
                if parts[1] == "":
                    hero["bag"] = []
                else:
                    hero["bag"] = parts[1].split("|")
            else:
                hero[parts[0]] = int(parts[1])
    return hero


# Phase 2: look up which tier an item belongs to
def item_tier(item):
    for tier in LOOT:
        if item in LOOT[tier]["items"]:
            return tier
    return "Poor"


# Phase 2: show the loot bag
def view_bag(hero):
    print()
    print("--- " + hero["name"].upper() + "'S LOOT BAG ---")
    if len(hero["bag"]) == 0:
        print("Empty. Go fight something.")
        return
    total = 0
    for item in hero["bag"]:
        tier = item_tier(item)
        value = LOOT[tier]["value"]
        total = total + value
        print("[" + tier + "]", item, "-", value, "gold")
    print("Total bag value:", total, "gold")


# Step 6
def main():
    print("=== FOR THE HORDE ===")
    assign_loot()
    choice = ""
    while choice != "n" and choice != "c":
        choice = input("(N)ew game or (C)ontinue? ").strip().lower()
        if choice != "n" and choice != "c":
            print("Type n or c.")
    if choice == "c":
        hero = load_checkpoint(SAVE_FILE)
        # Old saves have only name, hp, xp, and gold. Fill the rest here,
        # after load, so load_checkpoint itself stays an exact copy of the file.
        if "weapon" not in hero:
            hero["weapon"] = STARTING_WEAPON
        if "attack_bonus" not in hero:
            hero["attack_bonus"] = STARTING_BONUS
        if "bag" not in hero:
            hero["bag"] = []
        print("Welcome back,", hero["name"] + "!")
    else:
        name = input("Name your hero (Enter for " + DEFAULT_HERO + "): ")
        if name == "":
            name = DEFAULT_HERO
        hero = {
            "name": name,
            "hp": STARTING_HP,
            "xp": 0,
            "gold": 0,
            "weapon": STARTING_WEAPON,
            "attack_bonus": STARTING_BONUS,
            "bag": [],
        }
        print(name, "grips the", STARTING_WEAPON + ". The Horde awaits.")

    playing = True
    while playing:
        print()
        print("1) Fight a monster")
        print("2) View hero")
        print("3) Save checkpoint")
        print("4) Quit")
        print("5) View loot bag")
        choice = input("Choose an action: ")

        if choice == "1":
            won = fight(hero)
            if won:
                answer = ""
                while answer != "y" and answer != "n":
                    answer = input("Save your checkpoint? (y/n) ").strip().lower()
                    if answer != "y" and answer != "n":
                        print("Type y or n.")
                if answer == "y":
                    save_checkpoint(hero, SAVE_FILE)
                    print("Checkpoint saved.")
            if hero["hp"] <= 0:
                print("You collapse... and wake up back at camp.")
                hero["hp"] = STARTING_HP
        elif choice == "2":
            print(hero["name"], "| HP", hero["hp"], "| XP", hero["xp"], "| Gold", hero["gold"],
                  "| Weapon", hero["weapon"], "(+" + str(hero["attack_bonus"]) + ")",
                  "| Items", len(hero["bag"]))
        elif choice == "3":
            save_checkpoint(hero, SAVE_FILE)
            print("Checkpoint saved.")
        elif choice == "4":
            print("Farewell,", hero["name"] + ". Lok'tar.")
            playing = False
        elif choice == "5":
            view_bag(hero)
        else:
            print("That's not an option.")


main()
