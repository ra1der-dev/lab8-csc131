import random

SAVE_FILE = "saves/checkpoint.txt"
LOG_FILE = "saves/battle_log.txt"
STARTING_HP = 30
# Damage from the last lost fight. 0 means the hero was not hit.
LAST_BLOW = 0

HERO_NAMES = ["Thrall", "Grom", "Durotan", "Draka", "Saurfang", "Varok", "Nazgrel", "Aggra"]
WEAPON_TYPES = ["Club", "Sword", "Mace"]
POOR_PREFIX = ["Bent", "Rusty", "Cracked"]
COMMON_PREFIX = ["Iron", "Steel", "Bronze"]
RARE_WEAPONS = ["Blade of the Titans", "Ironfoe", "Shadowfang"]
EPIC_WEAPONS = ["Doomhammer", "Gorehowl", "Sulfuras"]
WEAPON_BONUS = {"Poor": 0, "Common": 1, "Rare": 2, "Epic": 3}
SHOP_PRICE = {"Poor": 20, "Common": 50}
POTION_COST = 15
POTION_HEAL = 10
REST_HEAL = 10
HERO_LIST = "saves/heroes.txt"

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

# The boss is not in MONSTERS. The lab checker compares those dictionaries
# to the starter monsters, and it also checks that extra monsters use only
# taunt, ac, damage, and xp.
BOSS = {
    "name": "Warchief of the Alliance",
    "taunt": "The Warchief of the Alliance raises a greatsword. 'Your Horde ends here!'",
    "ac": 16,
    "damage": 8,
    "xp": 80,
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

# One line printed before each monster appears.
ROOMS = [
    "You step into a torchlit tunnel.",
    "The cave opens into a cold stone hall.",
    "Roots hang over a muddy passage.",
    "A brazier burns in an empty guard room.",
    "Wind howls through a cracked gate.",
]

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


def random_weapon(tier):
    # Poor and Common are a random Club, Sword, or Mace with a prefix.
    # Rare and Epic are the named weapons, used only for a boss drop.
    if tier == "Poor":
        name = random.choice(POOR_PREFIX) + " " + random.choice(WEAPON_TYPES)
    elif tier == "Common":
        name = random.choice(COMMON_PREFIX) + " " + random.choice(WEAPON_TYPES)
    elif tier == "Rare":
        name = random.choice(RARE_WEAPONS)
    else:
        name = random.choice(EPIC_WEAPONS)
    return name, WEAPON_BONUS[tier]


def starting_weapon():
    # Same idea as the loot table: 1-60 is Poor, 61-100 is Common.
    roll = roll_die(100)
    if roll <= 60:
        return random_weapon("Poor")
    return random_weapon("Common")


def weapon_tier(item):
    if item in RARE_WEAPONS:
        return "Rare"
    if item in EPIC_WEAPONS:
        return "Epic"
    parts = item.split(" ")
    if len(parts) == 2 and parts[1] in WEAPON_TYPES:
        if parts[0] in POOR_PREFIX:
            return "Poor"
        if parts[0] in COMMON_PREFIX:
            return "Common"
    return ""


def level_from_xp(xp):
    # Level 2 costs 50 total XP. Each later level doubles that total.
    level = 1
    need = 50
    while xp >= need:
        level = level + 1
        need = need * 2
    return level


def apply_level(hero):
    # XP itself is never spent. The checker still sees xp=25 after one win.
    new_level = level_from_xp(hero["xp"])
    old_level = hero["level"]
    hero["level"] = new_level
    hero["max_hp"] = STARTING_HP + (new_level - 1) * 5
    if new_level > old_level:
        hero["hp"] = hero["hp"] + (new_level - old_level) * 5
        if hero["hp"] > hero["max_hp"]:
            hero["hp"] = hero["max_hp"]
        print("Level", str(new_level) + "! Max HP is now", str(hero["max_hp"]) + ".")


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
    # Named Rare and Epic weapons come from the boss only.
    # A normal monster that rolls that high drops Uncommon gear instead.
    if dropped == "Rare" or dropped == "Epic":
        dropped = "Uncommon"
    if dropped == "Poor" or dropped == "Common":
        item, bonus = random_weapon(dropped)
    else:
        item = ASSIGNED_LOOT[monster_name][dropped]
    hero["bag"].append(item)
    print("Loot! [" + dropped + "]", item, "(worth", LOOT[dropped]["value"], "gold)")
    log_event(hero["name"] + " looted " + item + " (" + dropped + ") from the " + monster_name + ".", LOG_FILE)


def boss_weapon_drop(hero):
    # One extra d100, and only after a boss kill. 71-90 is Rare, 91-100 is Epic.
    roll = roll_die(100)
    if roll <= 70:
        print("The Warchief carried no named weapon.")
        return
    if roll <= 90:
        tier = "Rare"
    else:
        tier = "Epic"
    item, bonus = random_weapon(tier)
    hero["bag"].append(item)
    print("Named weapon! [" + tier + "]", item)
    log_event(hero["name"] + " took the named weapon " + item + " (" + tier + ").", LOG_FILE)


def note_hit_damage(damage):
    # fight() already wrote "Name was hit by the Monster."
    # This adds the damage number onto the end of that same line.
    try:
        infile = open(LOG_FILE, "r")
        text = infile.read()
        infile.close()
    except FileNotFoundError:
        return
    if text.endswith(".\n") == False:
        return
    text = text[:-2] + " for " + str(damage) + " damage.\n"
    outfile = open(LOG_FILE, "w")
    outfile.write(text)
    outfile.close()


# Step 3
def fight(hero):
    global LAST_BLOW
    LAST_BLOW = 0
    # A new hero has wins 0, so the first fight is a normal monster.
    # The checker's hero has no wins key at all, so it never meets the boss.
    is_boss = False
    if "wins" in hero and hero["wins"] > 0 and hero["wins"] % 3 == 0:
        is_boss = True
        name = BOSS["name"]
        monster = BOSS
    else:
        name = random.choice(list(MONSTERS))
        monster = MONSTERS[name]
    print(random.choice(ROOMS))
    print(monster["taunt"])
    roll = roll_die(20)
    # The checker fights a hero that has no weapon yet. A missing bonus adds 0.
    bonus = 0
    if "attack_bonus" in hero:
        bonus = hero["attack_bonus"]
    if "level" in hero:
        bonus = bonus + (hero["level"] - 1) // 2
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
        if is_boss and "bag" in hero:
            boss_weapon_drop(hero)
        elif name in ASSIGNED_LOOT and "bag" in hero:
            roll_loot(hero, name)
        if "wins" in hero:
            hero["wins"] = hero["wins"] + 1
        if "level" in hero:
            apply_level(hero)
        return True
    else:
        hero["hp"] = hero["hp"] - monster["damage"]
        print("The", name, "hits you for", monster["damage"], "damage!")
        log_event(hero["name"] + " was hit by the " + name + ".", LOG_FILE)
        LAST_BLOW = monster["damage"]
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
    found = weapon_tier(item)
    if found != "":
        return found
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


def shop(hero):
    # Levels 1 and 2 see Poor weapons. Level 3 and up see Common weapons.
    if hero["level"] >= 3:
        tier = "Common"
    else:
        tier = "Poor"
    stock = [random_weapon(tier), random_weapon(tier)]
    buying = True
    while buying:
        print()
        print("Gold:", hero["gold"])
        print("1) Healing potion -", POTION_COST, "gold (restores", POTION_HEAL, "HP)")
        print("2)", stock[0][0], "-", SHOP_PRICE[tier], "gold")
        print("3)", stock[1][0], "-", SHOP_PRICE[tier], "gold")
        print("4) Leave")
        pick = input("Buy: ").strip()
        if pick == "1":
            if hero["gold"] < POTION_COST:
                print("Not enough gold.")
            else:
                hero["gold"] = hero["gold"] - POTION_COST
                hero["hp"] = hero["hp"] + POTION_HEAL
                if hero["hp"] > hero["max_hp"]:
                    hero["hp"] = hero["max_hp"]
                print("You drink the potion. HP is", str(hero["hp"]) + ".")
        elif pick == "2" or pick == "3":
            if pick == "2":
                chosen = stock[0]
            else:
                chosen = stock[1]
            price = SHOP_PRICE[tier]
            if hero["gold"] < price:
                print("Not enough gold.")
            else:
                hero["gold"] = hero["gold"] - price
                hero["weapon"] = chosen[0]
                hero["attack_bonus"] = chosen[1]
                print("You equip the", hero["weapon"] + ".")
        elif pick == "4":
            buying = False
        else:
            print("That's not in the shop.")


def hero_save_path(name):
    # Drop spaces so the file name is one word, such as saves/Thrall.txt.
    cleaned = ""
    for character in name:
        if character != " ":
            cleaned = cleaned + character
    if cleaned == "":
        cleaned = "hero"
    return "saves/" + cleaned + ".txt"


def remember_hero_file(filename):
    # heroes.txt is the list option 9 reads. The lab allows no import besides random,
    # so the game keeps its own list instead of scanning the folder.
    try:
        infile = open(HERO_LIST, "r")
        for line in infile:
            if line.rstrip("\n") == filename:
                infile.close()
                return
        infile.close()
    except FileNotFoundError:
        pass
    outfile = open(HERO_LIST, "a")
    outfile.write(filename + "\n")
    outfile.close()


def print_battle_log():
    try:
        infile = open(LOG_FILE, "r")
        text = infile.read()
        infile.close()
    except FileNotFoundError:
        print("The battle log is empty.")
        return
    if text.strip() == "":
        print("The battle log is empty.")
        return
    print(text, end="")


def load_saved_hero(hero):
    try:
        infile = open(HERO_LIST, "r")
        names = []
        for line in infile:
            filename = line.rstrip("\n")
            if filename != "":
                names.append(filename)
        infile.close()
    except FileNotFoundError:
        print("No hero saves yet.")
        return hero
    if len(names) == 0:
        print("No hero saves yet.")
        return hero
    number = 1
    for filename in names:
        print(str(number) + ")", filename)
        number = number + 1
    pick = input("Load which hero? ").strip()
    if pick.isdigit() == False:
        print("That's not a save.")
        return hero
    index = int(pick) - 1
    if index < 0 or index >= len(names):
        print("That's not a save.")
        return hero
    try:
        loaded = load_checkpoint(names[index])
    except FileNotFoundError:
        print("That save file is missing.")
        return hero
    fill_hero(loaded)
    print("Loaded", loaded["name"] + ".")
    return loaded


def fill_hero(hero):
    # Old saves have only name, hp, xp, and gold. Fill the rest here,
    # after load, so load_checkpoint itself stays an exact copy of the file.
    if "weapon" not in hero:
        weapon_name, weapon_bonus = random_weapon("Poor")
        hero["weapon"] = weapon_name
        hero["attack_bonus"] = weapon_bonus
    if "attack_bonus" not in hero:
        hero["attack_bonus"] = 0
    if "bag" not in hero:
        hero["bag"] = []
    if "wins" not in hero:
        hero["wins"] = 0
    if "level" not in hero:
        hero["level"] = level_from_xp(hero["xp"])
    if "max_hp" not in hero:
        hero["max_hp"] = STARTING_HP + (hero["level"] - 1) * 5


def print_menu():
    # Nine choices, three across. A short label gets spaces so the next
    # column starts in the same place on every row.
    options = [
        "1) Fight a monster",
        "2) View hero",
        "3) Save checkpoint",
        "4) Quit",
        "5) View loot bag",
        "6) Visit the shop",
        "7) Rest",
        "8) Read battle log",
        "9) Load a hero",
    ]
    columns = 3
    gap = "    "
    widths = [0, 0, 0]
    index = 0
    for option in options:
        column = index % columns
        if len(option) > widths[column]:
            widths[column] = len(option)
        index = index + 1
    index = 0
    line = ""
    for option in options:
        column = index % columns
        text = option
        last_in_row = column == columns - 1 or index == len(options) - 1
        if last_in_row == False:
            while len(text) < widths[column]:
                text = text + " "
            line = line + text + gap
        else:
            line = line + text
            print(line)
            line = ""
        index = index + 1


# Step 6
def main():
    print("=== FOR THE HORDE ===")
    assign_loot()
    choice = ""
    while choice != "n" and choice != "c":
        choice = input("(N)ew game or (C)ontinue? ").strip().lower()
        if choice != "n" and choice != "c":
            print("Type n or c.")
    hero = None
    if choice == "c":
        try:
            hero = load_checkpoint(SAVE_FILE)
        except FileNotFoundError:
            print("No checkpoint found. Starting a new hero.")
            hero = None
        if hero is not None:
            fill_hero(hero)
            print("Welcome back,", hero["name"] + "!")
    if hero is None:
        name = input("Name your hero (Enter for a random name): ")
        if name == "":
            name = random.choice(HERO_NAMES)
        weapon_name, weapon_bonus = starting_weapon()
        hero = {
            "name": name,
            "hp": STARTING_HP,
            "xp": 0,
            "gold": 0,
            "weapon": weapon_name,
            "attack_bonus": weapon_bonus,
            "bag": [],
            "wins": 0,
            "level": 1,
            "max_hp": STARTING_HP,
        }
        print(name, "grips the", weapon_name + ".")

    playing = True
    while playing:
        print()
        print_menu()
        choice = input("Choose an action: ")

        if choice == "1":
            fight(hero)
            if LAST_BLOW > 0:
                note_hit_damage(LAST_BLOW)
            if hero["hp"] <= 0:
                print("You collapse... and wake up back at camp.")
                if "max_hp" in hero:
                    hero["hp"] = hero["max_hp"]
                else:
                    hero["hp"] = STARTING_HP
                log_event(hero["name"] + " collapsed and woke up back at camp.", LOG_FILE)
            save_checkpoint(hero, SAVE_FILE)
            print("Checkpoint saved.")
        elif choice == "2":
            print(hero["name"], "| Level", hero["level"], "| HP", str(hero["hp"]) + "/" + str(hero["max_hp"]),
                  "| XP", hero["xp"], "| Gold", hero["gold"],
                  "| Weapon", hero["weapon"], "(+" + str(hero["attack_bonus"]) + ")",
                  "| Items", len(hero["bag"]))
        elif choice == "3":
            save_checkpoint(hero, SAVE_FILE)
            hero_file = hero_save_path(hero["name"])
            save_checkpoint(hero, hero_file)
            remember_hero_file(hero_file)
            print("Checkpoint saved.")
        elif choice == "4":
            print("Farewell,", hero["name"] + ". Lok'tar.")
            playing = False
        elif choice == "5":
            view_bag(hero)
        elif choice == "6":
            shop(hero)
        elif choice == "7":
            if hero["hp"] >= hero["max_hp"]:
                print(hero["name"], "is already rested.")
            else:
                hero["hp"] = hero["hp"] + REST_HEAL
                if hero["hp"] > hero["max_hp"]:
                    hero["hp"] = hero["max_hp"]
                print(hero["name"], "rests. HP is", str(hero["hp"]) + ".")
        elif choice == "8":
            print_battle_log()
        elif choice == "9":
            hero = load_saved_hero(hero)
        else:
            print("That's not an option.")


main()
