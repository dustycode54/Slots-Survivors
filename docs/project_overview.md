# Slots Survivors: Rogue-Like Survival Game

> A run-based slot machine game where the player tries to hit a rising score quota each round and builds up their machine with upgrades along the way.

---

## Overview

**Slots Survivors** is a single-player rogue-like built around a slot machine. There is no betting and no currency to lose. Each pull of the lever adds points based on the symbols rolled. Each round has a **quota**. If the player meets it, they survive to the next round and pick an upgrade. If they miss it, the run ends.

The game runs locally on the player's machine. No hosting, networking, or accounts are needed.

The project also **shows off core data structures** (sets, lists, dictionaries, and more), and each one is used where it fits a real gameplay system.

---

## Tech Stack

| Layer          | Technology | Purpose                                                    |
| -------------- | ---------- | ---------------------------------------------------------- |
| Language       | Python 3   | All game logic, state, and scoring                         |
| Rendering / UI | pygame     | Window, drawing shapes and text, input handling, game loop |
| Randomness     | `random` (stdlib) | Reel spins, weighted symbol selection, upgrade offers |

- **Platform:** Local desktop (macOS / Windows / Linux, wherever Python and pygame run)
- **Dependencies:** `pygame` only. Everything else comes from the Python standard library.
- **Assets:** None at first. All visuals are drawn with pygame primitives (rects, circles, polygons, text).

---

## Core Gameplay Loop

```
Start Run
   │
   ▼
┌───────────────────────────┐
│  Round N begins           │
│  Quota is shown           │
└───────────┬───────────────┘
            ▼
┌───────────────────────────┐
│  Pull lever (3 rolls)     │◄──┐
│  Reels spin and stop      │   │ rolls remaining
│  Score added              │───┘
└───────────┬───────────────┘
            ▼
     Score ≥ Quota?
      │          │
     Yes         No
      │          │
      ▼          ▼
 Choose an    Game Over
 upgrade      (Restart / Quit)
      │
      ▼
 Round N+1 (higher quota)
```

### Rounds & Rolls
- The player gets **3 rolls per round** by default. Upgrades can raise this.
- Each roll spins the reels and scores the result right away.
- The round score is the total of all rolls in that round.

### Quota
- Each round has a target score that the player must reach.
- The quota **goes up each round** so that upgrades become necessary to survive.
- *Open question:* how the quota scales (linear, exponential, or hand-tuned per round).

### Win / Lose Conditions
- **Pass:** round score ≥ quota, so the player moves to the upgrade screen and then the next round.
- **Fail:** round score < quota, so the run ends and the player can **Restart** or **Quit**.
- *Open question:* is there a final round or "victory" state, or is the run endless and played for a high score?

---

## The Slot Machine

### Reels & Symbols
- A row of reels (e.g. **3 reels**) that each land on one symbol.
- Example symbols: 🍒 Cherry, 🍋 Lemon, 🔔 Bell, 💎 Diamond, 7️⃣ Seven
- Each symbol has its own **base score** and **appearance weight** (how often it shows up).

### Scoring (initial idea)
- Matching symbols score more than mixed results (e.g. three of a kind > a pair > no match).
- Rarer symbols (like 7s and Diamonds) are worth more.
- *Open question:* the exact payout rules, i.e. whether only matches score or every symbol adds its own value.

---

## Upgrades & Skill Tree

After each round the player passes, they **choose one upgrade** from a small set of randomly offered options taken from a skill tree.

### Example Upgrades
| Upgrade              | Effect                                       |
| -------------------- | -------------------------------------------- |
| Extra Pull           | +1 roll per round                            |
| Lucky Sevens         | 7s score double                              |
| Diamond Mine         | Diamonds appear more frequently              |
| Cherry Picker        | Cherries are worth +X points                 |
| *(more to come)*     |                                              |

### Skill Tree Structure
- Some upgrades only unlock after the player owns earlier ones (e.g. *Lucky Sevens II* needs *Lucky Sevens*).
- Upgrades the player already owns (or that are maxed out) are left out of future offers.
- *Open question:* is it a true branching tree, or a pool of upgrades with prerequisites?

---

## Data Structures Showcase

A main goal of the project is to use a range of data structures, each in a place where it makes sense:

| Data Structure | Where It's Used | Why It Fits |
| -------------- | --------------- | ----------- |
| **Set**        | Player's unlocked upgrades | Fast membership checks ("does the player own X?"), no duplicates |
| **List**       | Reel strips, upgrade offers, random selection pools | Ordered, indexable, works well with `random.choice` / `random.choices` |
| **Dictionary** | Player stats (`rolls_per_round`, `score`, `round`), symbol stats (`{"7": {"score": 50, "weight": 2}}`) | Named lookups for values that change during a run |
| **Tree / Graph** *(possible)* | Upgrade skill tree and its prerequisites | Models the parent and child links between upgrades |
| **Queue / Stack** *(possible)* | Roll history, animation events, or an undo log | Ordered processing of events |

### Example Shapes

```python
player_stats = {
    "round": 1,
    "rolls_per_round": 3,
    "round_score": 0,
    "total_score": 0,
}

symbol_stats = {
    "cherry":  {"score": 5,  "weight": 10},
    "lemon":   {"score": 10, "weight": 8},
    "bell":    {"score": 20, "weight": 5},
    "diamond": {"score": 35, "weight": 3},
    "seven":   {"score": 50, "weight": 2},
}

unlocked_upgrades = {"extra_pull", "lucky_sevens"}
```

---

## Visuals & UI

### Initial Scope
- Simple visuals drawn with **pygame shapes and text**:
  - Slot machine body (rectangles)
  - Reels showing symbols as colored shapes or text labels
  - A lever the player clicks (or presses a key) to roll
  - HUD showing the current round, rolls left, round score, and quota
- Screens:
  1. **Title / Start**
  2. **Gameplay** (slot machine)
  3. **Upgrade Selection**
  4. **Game Over** (Restart / Quit)

### Stretch Goals
- Sprite-based symbols and machine art
- Reel spin animation and lever pull animation
- Sound effects and music
- Persistent high-score tracking (saved to a local file)
- Extra content: more symbols, more upgrades, special reel effects

---

## Open Questions

- How should the quota scale from round to round?
- Exact scoring and payout rules for matches and individual symbols
- Number of reels (3? 5?) and whether there are multiple paylines
- Endless mode or a fixed number of rounds?
- How many upgrade choices are offered per round?
