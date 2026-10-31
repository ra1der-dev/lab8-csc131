# Changelog

Changes on `jays-fork` that are not on `main`. `main` stays at the original lab game: random weapons, the shop, and levels.

## Title, taunts, and saves setup

- Startup prints a figlet **Dungeons & Deadlines** banner before anything else.
- Each monster (and the boss) has extra taunt lines in `TAUNT_LINES`. The locked `taunt` on `MONSTERS` / `BOSS` is unchanged for the checker. `pick_taunt()` mixes them.
- If the `saves/` folder is missing, the game prints setup instructions and stops (no `os.mkdir`; lab allows only `import random`).
- Continue / Load treat a damaged checkpoint (non-number fields) as a soft failure instead of crashing.

## Gear, shop, and fight choices

- Weapons and armor catalogs by tier. Attack / armor bonuses: Poor 0, Common 1, Uncommon 1, Rare 2, Epic 3 (capped for power creep). Armor reduces hit damage but never below 1.
- Bag (option 5) equips weapons **or** armor; junk is rejected. Hero save includes `armor` / `armor_bonus`.
- Shop: level-scaled potions (`25 + (level-1)*15`), two rotating Uncommon/Rare/Epic weapon-or-armor offers (buy 150/350/900), and sell-from-bag. No Poor/Common shop stock.
- Sell values: Poor 8, Common 25, Uncommon 60, Rare 150, Epic 400.
- Fights with a `wins` key ask Attack or Flee. Flee is a d20 vs monster difficulty. Checker paths without `wins` still auto-attack.

## Rest, rooms, and hero files

- Continue with no `saves/checkpoint.txt` starts a new hero instead of crashing.
- Option 7 rests and heals 10 HP, up to max HP.
- Option 8 prints `saves/battle_log.txt`.
- Each fight prints one random room line, then the monster's taunt.
- Option 3 still writes `saves/checkpoint.txt`. It also writes `saves/<hero>.txt`, with spaces removed from the name, and lists that file in `saves/heroes.txt`.
- Option 9 loads one of those hero files.

## Menu

- The nine choices print in three columns, with four spaces between columns.

## After a fight

- Every fight saves `saves/checkpoint.txt` on its own. The old `Save your checkpoint? (y/n)` question is gone.
- If HP drops to 0 or below, the hero wakes at camp with max HP, and that full HP is what gets saved.

## Battle log

- A hit is recorded as `Name was hit by the Monster for N damage.`
- A defeat adds `Name collapsed and woke up back at camp.`

## Notes

- `AGENTS.md`, `.cursor/rules/`, and this file describe `jays-fork`.
- `ascii-fight` is a separate branch with the fight pictures. It is not part of this fork, and it is not merged into `main`.
