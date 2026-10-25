# AGENTS.md

Project: Lab 8, CSC 131 (UNCW). A beginner Python text dungeon game in one file, `app.py`, themed on World of Warcraft (Horde).

The GitHub repo is https://github.com/ra1der-dev/lab8-csc131. `main` is the lab game. `ascii-fight` is the side branch with the fight pictures. Do not merge `ascii-fight` into `main`.

Rules and design live in `.cursor/rules/`:
- `lab8-rules.mdc` - hard rules from the lab. Always apply.
- `game-design.mdc` - how the hero, monsters, loot, and save file work.
- `no-ascii-on-main.mdc` - ASCII fight pictures stay on `ascii-fight` only. Always apply.

How to test:
1. After a full change, run `python check_lab-2.py` in this folder. It grades `app.py` and must show 21/21.
2. Play: (N)ew game, fight a few times (one room line prints before the taunt), 5 to view loot, 7 to rest, 8 to read the battle log, 3 to save, 9 to load a saved hero, 4 to quit.
3. Run again, choose (C)ontinue, check that HP, XP, gold, weapon, and loot bag came back. Continue with no `saves/checkpoint.txt` starts a new hero.

`check_lab-2.py` stays on this machine. Do not commit it to GitHub.
