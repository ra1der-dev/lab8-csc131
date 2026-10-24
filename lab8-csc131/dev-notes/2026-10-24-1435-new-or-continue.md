# New-game prompt treats anything other than c as a new game

Date: 2026-10-24 14:35
Status: fixed with the same loop as the save prompt

Where: the start of `main()`, prompt `(N)ew game or (C)ontinue?`.

What happened: only `c` loaded a checkpoint. Any other character, including a blank line, started a new hero.

What it does now: the prompt stays up until the answer is `n` or `c`. `n` starts a new hero. `c` loads the checkpoint. Any other answer prints `Type n or c.`

The prompt text was kept. See `2026-10-24-1433-save-prompt-yn.md` for the other fix ideas that were not used.
