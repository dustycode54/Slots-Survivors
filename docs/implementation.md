# Implementation Plan

> How the work is split up, what order it happens in, and who is waiting on whom.

See the [Project Overview](project_overview.md) for what the game is, and the [pygame Study Guide](pygame_info.md) for pygame basics.

---

## Team Roles

| Member | Area | Main Files |
| ------ | ---- | ---------- |
| **Member 1** | Slot Machine & Scoring Logic | `src/slot_machine.py`, `tests/test_slot_machine.py` |
| **Member 2** | Skill Tree & Upgrade System | `src/upgrades.py`, `tests/test_upgrades.py` |
| **Member 3** | Pygame Graphics & UI | `src/ui.py`, `tests/test_ui.py` |
| **Member 4** | Game Progression & State | `src/game_state.py`, `tests/test_game_state.py` |

Original role breakdown: [team_roles.png](images/team_roles.png)

### Project Layout

```
main.py          # starts the game (run with: python main.py)
src/             # game code, one module per member
tests/           # one test file per module
docs/            # overview, pygame guide, this plan
```

Imports look like `from src.slot_machine import spin_reels`. Run tests from the project root (e.g. `python -m pytest`) so `src` can be found.

Each member's module should be testable **on its own** using fake/hardcoded data, so nobody is blocked waiting on someone else to finish.

---

## Phases

```
Phase 0: Setup & Agreements (everyone)
   │
   ▼
Phase 1: Build modules in parallel
   ├── Member 1: slot machine + scoring
   ├── Member 2: upgrades + skill tree
   ├── Member 3: screens + drawing
   └── Member 4: game state + rounds
   │
   ▼
Phase 2: Integration (wire it together in main.py)
   │
   ▼
Phase 3: Balancing, polish & stretch goals
```

### Phase 0: Setup & Agreements
Everyone together, ideally in one meeting. The goal is to agree on the **shared data shapes** (what a spin result looks like, what `player_stats` holds, what an upgrade looks like) so each person can build against them independently. Also make a first pass at the open questions in the overview.

### Phase 1: Parallel Development
Each member builds and tests their own module. Use fake data where you would normally need someone else's code (e.g. the UI can draw a hardcoded `["seven", "seven", "bell"]`).

### Phase 2: Integration
Connect the modules in a main game loop. This is where the dependencies actually matter, so expect some back and forth.

### Phase 3: Polish
Tune the numbers so the game is fun, fix bugs, and pick up stretch goals if there's time.

---

## Dependency Overview

| Ticket | Depends On |
| ------ | ---------- |
| T0.1 – T0.3 | none |
| T1.x (Member 1) | T0.2 |
| T2.x (Member 2) | T0.2 |
| T3.x (Member 3) | T0.2 |
| T4.x (Member 4) | T0.2 |
| T2.4 Apply upgrade effects | T1.1, T4.1 (needs to know what it's changing) |
| T5.1 Main game loop | T1.3, T2.3, T3.4, T4.3 |
| T5.2 – T5.3 | T5.1 |
| T6.x | T5.1 |

> **Rule of thumb:** if your ticket depends on someone else's, you can still start it with fake data. You just can't *finish* it until theirs is done.

---

## Tickets

Tickets are intentionally short. The "Suggestions" are just ideas, not requirements. Use your own judgment.

### Phase 0: Setup (Everyone)

#### T0.1: Project skeleton
- **Owner:** Anyone
- **Depends on:** none
- **Task:** Create the empty files listed above plus a `main.py`, a `requirements.txt` with `pygame`, and a short "how to run" in the README.
- **Done when:** Everyone can clone the repo, install pygame, and run `python main.py` to open an empty window.

#### T0.2: Agree on shared data shapes
- **Owner:** Everyone
- **Depends on:** none
- **Task:** Write down (in this doc or a new `docs/interfaces.md`) the shapes everyone will pass around, and the names of the main functions each module will expose.
- **Suggestions:**
  - Spin result: a list of symbol names, e.g. `["cherry", "seven", "seven"]`
  - Player stats: a dictionary like the one in the overview
  - Upgrade: a dictionary like `{"id": "extra_pull", "name": "Extra Pull", "description": "...", "requires": []}`
  - Function names, e.g. `spin_reels()`, `score_spin(results)`, `get_upgrade_offers(owned)`
- **Done when:** Everyone has signed off and knows what their module takes in and gives back.

#### T0.3: Answer the open questions (first pass)
- **Owner:** Everyone
- **Depends on:** none
- **Task:** Make a first decision on each open question in the overview (quota scaling, payout rules, number of reels, endless vs. fixed rounds, number of upgrade choices). These can change later during balancing.
- **Done when:** The overview's Open Questions section has an answer (even a tentative one) for each item.

---

### Member 1: Slot Machine & Scoring

#### T1.1: Symbol data
- **Depends on:** T0.2
- **Task:** Define the symbols, their base scores, and their weights.
- **Suggestions:** A dictionary like `symbol_stats` in the overview. Keep it easy for upgrades to modify.

#### T1.2: Weighted spin
- **Depends on:** T1.1
- **Task:** Write a function that returns one random symbol per reel, using the weights.
- **Suggestions:** `random.choices` with a `weights` list does most of the work.
- **Done when:** Running it 10,000 times shows rare symbols really do show up less often.

#### T1.3: Scoring a spin
- **Depends on:** T1.2, T0.3 (payout rules)
- **Task:** Given a spin result, return how many points it's worth (singles, pairs, triples).
- **Suggestions:** A dictionary or `collections.Counter` makes counting matches easy.
- **Done when:** Tests cover no match, a pair, and three of a kind.

#### T1.4: Multipliers & bonuses
- **Depends on:** T1.3
- **Task:** Let scoring take modifiers into account (e.g. "7s score double").
- **Suggestions:** Pass in a dictionary of multipliers, so the upgrade system can just change numbers instead of changing your code.
- **Done when:** A test shows a spin scoring differently with and without a multiplier.

---

### Member 2: Skill Tree & Upgrades

#### T2.1: Upgrade list
- **Depends on:** T0.2
- **Task:** Define every upgrade: id, name, description, and prerequisites.
- **Suggestions:** Start with the four from the overview, plus one or two "level II" upgrades so the tree has some depth.

#### T2.2: Prerequisite graph
- **Depends on:** T2.1
- **Task:** Build the directed graph of which upgrades unlock which. Be able to answer "can the player take this upgrade yet?"
- **Suggestions:** An adjacency list (dictionary of lists). Owned upgrades in a set.
- **Done when:** Tests show a locked upgrade becoming available once its prerequisite is owned.

#### T2.3: Random upgrade offers
- **Depends on:** T2.2
- **Task:** Pick N random upgrades the player is eligible for (not owned, prerequisites met).
- **Done when:** Offers never include owned or locked upgrades, and it doesn't crash when fewer than N are left.

#### T2.4: Applying upgrade effects
- **Depends on:** T2.1, T1.1, T4.1
- **Task:** When an upgrade is chosen, actually change the game (more rolls, new weights, multipliers, etc.).
- **Suggestions:** Each upgrade could map to a small function, or to a description of what stat to change and by how much.
- **Done when:** Tests show each example upgrade changing the right value.

---

### Member 3: Graphics & UI

#### T3.1: Window & screen switching
- **Depends on:** T0.1
- **Task:** Set up the window and a simple way to switch between screens (title, gameplay, upgrade, game over).
- **Suggestions:** A state string to start, as shown in the pygame guide. Classes per screen if it gets messy.

#### T3.2: Draw the slot machine
- **Depends on:** T3.1, T0.2
- **Task:** Draw the machine body, reels, symbols, and a lever.
- **Suggestions:** Colored shapes + text labels (see `SYMBOL_STYLE` in the pygame guide). Use a hardcoded spin result while testing.

#### T3.3: HUD
- **Depends on:** T3.1
- **Task:** Show round, rolls left, current score, and quota.
- **Suggestions:** Use a fake `player_stats` dictionary until Member 4's is ready.

#### T3.4: Input: lever, buttons, upgrade cards
- **Depends on:** T3.2
- **Task:** Make the lever clickable (and/or spacebar), add Start / Restart / Quit buttons, and draw clickable upgrade cards.
- **Suggestions:** `Rect.collidepoint` for clicks. Have the UI *report* what was clicked rather than doing the game logic itself.
- **Done when:** You can click through every screen using fake data.

---

### Member 4: Game Progression & State

#### T4.1: Player stats
- **Depends on:** T0.2
- **Task:** Create, store, and reset the player's stats for a new run.
- **Suggestions:** A dictionary or a small class. Include a `reset()` for Restart.

#### T4.2: Rounds, rolls & quota
- **Depends on:** T4.1, T0.3 (quota scaling)
- **Task:** Track rolls remaining, add roll scores to the round score, and calculate the quota for each round.
- **Done when:** Tests show the quota rising each round and rolls running out correctly.

#### T4.3: Pass / fail & transitions
- **Depends on:** T4.2
- **Task:** When the last roll is used, decide pass or fail and move to the upgrade screen or game over.
- **Suggestions:** Keep track of a `state` value the UI can read.
- **Done when:** A test can simulate a whole run (with fake scores) from round 1 to game over.

#### T4.4: Integration tests
- **Depends on:** T5.1
- **Task:** Once everything is connected, write tests that run real spins, real upgrades, and real state together (no pygame needed).

---

### Phase 2: Integration (Shared)

#### T5.1: Main game loop
- **Owner:** Member 4 leads, everyone helps
- **Depends on:** T1.3, T2.3, T3.4, T4.3
- **Task:** In `main.py`, connect the UI's input to the game state, slot machine, and upgrades.
- **Done when:** You can play a full run from the title screen to game over and restart.

#### T5.2: Hook up upgrade effects
- **Owner:** Member 2
- **Depends on:** T5.1, T2.4
- **Task:** Make chosen upgrades actually change gameplay in the running game.

#### T5.3: Bug bash
- **Owner:** Everyone
- **Depends on:** T5.1
- **Task:** Everyone plays several runs and logs bugs as new tickets.

---

### Phase 3: Polish & Stretch Goals

Pick these up only once Phase 2 works. Owners are suggestions.

| Ticket | Task | Suggested Owner |
| ------ | ---- | --------------- |
| T6.1 | Balance quota, scores, and weights so runs feel fair but challenging | Members 1 & 4 |
| T6.2 | Add more upgrades and deeper tree branches | Member 2 |
| T6.3 | Reel spin and lever animations | Member 3 |
| T6.4 | Save a high score to a local file | Member 4 |
| T6.5 | Sprites and sound effects | Member 3 |
| T6.6 | Show the skill tree visually on the upgrade screen | Members 2 & 3 |
