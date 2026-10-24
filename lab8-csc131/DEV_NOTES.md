# Dev notes

Bugs and coder notes for the Lab 8 dungeon game.

Lab limits for any later fix: beginner Python only (variables, if/elif/else, loops, lists, dictionaries, `random`, text files). No classes. No imports besides `random`. Do not rename `save_checkpoint` or menu options 1–4.

After a code change, run `python check_lab.py` (from Canvas; it is not in this repo). It must still show 21/21.

## Fixed

### 1. Save prompt accepts anything besides `y`

Status: fixed with idea 1.

Where: `main()`, after a won fight, prompt `Save your checkpoint? (y/n)`.

What happened: typing a character other than `y` or `n` skipped the save and returned to the menu.

Coder note (Jay): other characters bypass the save requirement and go back to the menu screen.

What it does now: the prompt stays up until the answer is `y` or `n`. Spaces are stripped. `y` saves. `n` returns to the menu without saving. Any other answer prints `Type y or n.`

These inputs used to take the same path as `n`:

- `x` or any other letter
- `yes` (the check is the whole string, so only `y` counts)
- a blank line
- `y ` with a space (`lower()` does not remove spaces)

### 2. New-game prompt treats anything other than `c` as a new game

Status: fixed with the same loop.

Where: the start of `main()`, prompt `(N)ew game or (C)ontinue?`.

What happened: only `c` loaded a checkpoint. Any other character, including a blank line, started a new hero.

What it does now: the prompt stays up until the answer is `n` or `c`. `n` starts a new hero. `c` loads the checkpoint. Any other answer prints `Type n or c.`

## Fix ideas

Idea 1 is the one applied to both prompts. The prompt text was kept so `check_lab.py` is less likely to fail if it looks for those strings.

### 1. Ask again until the answer is one of the two letters

Applied. A `while` loop strips spaces, lowercases the text, and prints a short reminder for anything else. Junk input cannot leave the prompt.

### 2. Same loop, but accept a word that starts with the letter

Not applied. `yes` and `no` would count. `yep` would also count as yes.

### 3. Strip spaces, then keep the exact check with no loop

Not applied. `y ` would work. `x` would still skip the save.

### 4. Save unless the answer is exactly `n`

Not applied. Junk input would save instead of asking again.
