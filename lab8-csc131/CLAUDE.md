# Lab 8 – CSC 131 – "For the Horde" dungeon game

Single-file beginner Python game: `app.py`. Grading checker: `check_lab.py` (must stay 21/21).

## Hard rules (from the lab)
- Only beginner Python: variables, if/elif/else, loops, lists, dictionaries, `random`, and text files. No classes, no imports besides `random`.
- Do not rename or change the parameters of `roll_die`, `log_event`, `fight`, `save_checkpoint`, `load_checkpoint`, or `main`. `fight()` must still return True or False.
- Keep `SAVE_FILE`, `LOG_FILE`, and `STARTING_HP` as they are.
- Menu options 1–4 stay exactly as they are. New features go in option 5 and up.
- After every change: run `python3 check_lab.py` and a quick play-test (new game → fight → save → quit → Continue). If the checker drops below 21/21, fix that before adding anything else.

## Current state
- Theme: World of Warcraft, Horde. Default hero Thrall, starting weapon Doomhammer (+2 to the d20).
- Monsters: original four plus three Alliance foes. Each monster gets a randomized loot table at startup (`assign_loot`).
- Loot: five WoW-style tiers (Poor → Epic) rolled on d100 + (monster AC − 8) in `roll_loot`. Rolls under 31 drop nothing.
- Save format is `key=value` per line. `name`, `weapon`, and `bag` are strings (`bag` is `|`-joined); everything else is an int. Old saves without those keys must still load.
- `saves/` holds `checkpoint.txt` and `battle_log.txt`; keep the folder, never commit its contents.

## Workflow
- Explain every line added or changed, in plain language, so it can be read aloud to the guild.
- Prefer small, testable steps over big rewrites.
