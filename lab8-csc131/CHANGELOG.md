# Changelog

Changes on `jays-fork` that are not on `main`. `main` stays at the original lab game: random weapons, the shop, and levels.

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
