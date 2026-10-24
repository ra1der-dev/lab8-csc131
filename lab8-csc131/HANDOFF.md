# Handoff: work done so far

Exported from a Claude session on Oct 23-24, 2026.

## History
1. **Phase 1 baseline** - class-built `app.py` ("COAST OF THE WIZARD"): roll_die, log_event, fight, save_checkpoint, load_checkpoint, main, plus a Mimic monster.
2. **Horde theme** - title changed, default hero Thrall, Doomhammer (+2) added to the d20 roll, three Alliance monsters, random victory shouts.
3. **Armory** - option 5 shop with Gorehowl and Blood Fury Axe. **Later removed** at Jay's request.
4. **Loot system** - WoW-style tiers, per-monster random loot tables, loot bag saved with the hero, option 5 now shows the bag.
5. **Save fix** - `load_checkpoint` keeps `name`, `weapon`, `bag` as strings and supports old saves.

## Source for the loot tiers
Warcraft Wiki, Item Quality: https://warcraft.wiki.gg/wiki/Item_Quality
It names the tiers and colors but gives no exact drop rates, so the percentages here are our own picks.

## Tested
- New game, fights, loot in every tier including "nothing", save, quit, Continue restores everything.
- Old Phase 1 save (no weapon or bag lines) loads without crashing.
- `check_lab.py` was not available during the session. Run it once to confirm 21/21.

## Open items
- Push to GitHub: https://github.com/ra1der-dev/lab8-csc131
- Invite lab teammates as collaborators (repo Settings > Collaborators).
- Phase 3 questions and reflection (Word doc) are separate and not started here.

## Ideas not built yet (from the lab sheet)
Rest option, potions that heal, print the battle log, room descriptions, leveling up, a boss after three wins, one save file per hero, Continue that doesn't crash with no save.
