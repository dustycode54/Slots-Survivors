# pygame Study Guide

> A quick reference for how pygame works, with examples aimed at **Slots Survivors**.

---

## What is pygame?

**pygame** is a Python library for making 2D games. It wraps **SDL** (Simple DirectMedia Layer) and gives you:

- A **window** to draw into
- **Drawing** tools for shapes, images and text
- **Input** handling for the keyboard, mouse and window events
- **Timing** tools to control the frame rate
- **Sound** playback (a stretch goal for us)

pygame does **not** give you a game engine, scenes, or UI widgets. You write the game loop and manage state yourself. That suits this project, because the game state lives in our own data structures.

### Install

```bash
pip install pygame
python -m pygame.examples.aliens   # optional: run a demo to check the install
```

---

## Core Concepts

### 1. Initialization & the Window

```python
import pygame

pygame.init()                                   # start all pygame modules
screen = pygame.display.set_mode((800, 600))    # create the window, returns a Surface
pygame.display.set_caption("Slots Survivors")
```

- `pygame.init()` must run before you use most other pygame features.
- `set_mode()` returns the **display Surface**, the "canvas" that appears on screen.

### 2. Surfaces

A **Surface** is a 2D image you can draw on. The screen is a Surface, and so are loaded images and rendered text.

```python
panel = pygame.Surface((200, 100))   # a blank off-screen surface
panel.fill((40, 40, 60))             # fill it with a color
screen.blit(panel, (300, 250))       # copy (blit) it onto the screen at (x, y)
```

- **Coordinates:** `(0, 0)` is the **top-left**. **x** increases to the right and **y** increases **downward**.
- **Colors** are `(R, G, B)` tuples with values from 0 to 255.

### 3. The Game Loop

Every pygame program is built around a loop that runs many times per second:

```
┌──────────────────────────┐
│ 1. Handle events (input) │
│ 2. Update game state     │
│ 3. Draw everything       │
│ 4. Flip display          │
│ 5. Tick the clock        │
└────────────┬─────────────┘
             └──── repeat ────┘
```

```python
clock = pygame.time.Clock()
running = True

while running:
    # 1. Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. Update
    # ... change game state here ...

    # 3. Draw
    screen.fill((20, 20, 30))         # clear the frame
    # ... draw things here ...

    # 4. Show the frame
    pygame.display.flip()

    # 5. Limit to 60 frames per second
    clock.tick(60)

pygame.quit()
```

> **Key idea:** you redraw the **whole screen every frame**. Nothing stays on screen unless you draw it again.

### 4. Events & Input

pygame puts input in an **event queue**. You read it with `pygame.event.get()`.

| Event Type                 | When it fires                 | Useful attributes        |
| -------------------------- | ----------------------------- | ------------------------ |
| `pygame.QUIT`              | Window close button clicked   | none                     |
| `pygame.KEYDOWN` / `KEYUP` | A key is pressed or released  | `event.key` (e.g. `pygame.K_SPACE`) |
| `pygame.MOUSEBUTTONDOWN`   | A mouse button is pressed     | `event.pos`, `event.button` |
| `pygame.MOUSEMOTION`       | The mouse moves               | `event.pos`              |

```python
for event in pygame.event.get():
    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        print("Space pressed!")
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:   # left click
        print("Clicked at", event.pos)
```

You can also check what is held down **right now** (rather than reacting to an event):

```python
keys = pygame.key.get_pressed()
if keys[pygame.K_SPACE]:
    ...
```

### 5. Drawing Shapes (`pygame.draw`)

All of our first visuals will use these:

```python
pygame.draw.rect(screen, (200, 50, 50), (100, 100, 150, 80))           # filled rectangle
pygame.draw.rect(screen, (255, 255, 255), (100, 100, 150, 80), 3)      # outline only (width 3)
pygame.draw.rect(screen, (90, 90, 90), (100, 100, 150, 80), border_radius=12)  # rounded corners
pygame.draw.circle(screen, (255, 215, 0), (400, 300), 25)              # circle: center, radius
pygame.draw.line(screen, (255, 255, 255), (0, 0), (800, 600), 2)       # line
pygame.draw.polygon(screen, (0, 200, 255), [(400, 250), (430, 300), (400, 350), (370, 300)])  # diamond
```

### 6. Rects

`pygame.Rect` stores a position and size. It is used everywhere for placing things and for hit detection.

```python
lever = pygame.Rect(650, 200, 40, 160)   # x, y, width, height

lever.center        # (670, 280)
lever.topleft       # (650, 200)
lever.collidepoint(mouse_pos)   # True if a point is inside the rect
lever.colliderect(other_rect)   # True if two rects overlap
```

### 7. Text (`pygame.font`)

Text is **rendered to a Surface** first and then blitted onto the screen:

```python
font = pygame.font.SysFont("arial", 32)                  # or pygame.font.Font(None, 32) for the default font
text_surf = font.render("Quota: 500", True, (255, 255, 255))   # text, antialias, color
screen.blit(text_surf, (20, 20))

# Centering text inside a rect:
text_rect = text_surf.get_rect(center=lever.center)
screen.blit(text_surf, text_rect)
```

> **Tip:** create your `Font` objects **once** at startup, not every frame. Loading a font is slow.

### 8. Time & Frame Rate

```python
clock = pygame.time.Clock()
dt = clock.tick(60) / 1000   # caps at 60 FPS; returns ms since the last frame, here converted to seconds

pygame.time.get_ticks()      # ms since pygame.init(), handy for timers
```

Use `dt` (delta time) to make animations run at the same speed regardless of frame rate.

### 9. Images & Sound (Stretch Goals)

```python
seven_img = pygame.image.load("assets/seven.png").convert_alpha()
screen.blit(seven_img, (x, y))

pull_sound = pygame.mixer.Sound("assets/lever.wav")
pull_sound.play()
```

---

## Applying pygame to Slots Survivors

### Game States (Screens)

The game has several screens. A simple approach is to track a **state** string and branch on it in the loop:

```python
state = "title"   # "title" | "playing" | "upgrade" | "game_over"

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif state == "title":
            handle_title_input(event)
        elif state == "playing":
            handle_play_input(event)
        # ...

    if state == "title":
        draw_title(screen)
    elif state == "playing":
        draw_machine(screen)
    # ...
```

> Later on, each screen could become its own **class** with `handle_event()`, `update()` and `draw()` methods. That keeps the main loop small.

### Drawing Symbols with Shapes

Before we have sprites, each symbol can be a colored shape plus a label. A **dictionary** maps each symbol to how it is drawn:

```python
SYMBOL_STYLE = {
    "cherry":  {"color": (220, 30, 60),  "label": "CH"},
    "lemon":   {"color": (250, 230, 60), "label": "LE"},
    "bell":    {"color": (240, 180, 40), "label": "BE"},
    "diamond": {"color": (80, 200, 255), "label": "DI"},
    "seven":   {"color": (255, 60, 60),  "label": "7"},
}

def draw_symbol(screen, symbol, rect, font):
    style = SYMBOL_STYLE[symbol]
    pygame.draw.rect(screen, style["color"], rect, border_radius=10)
    label = font.render(style["label"], True, (0, 0, 0))
    screen.blit(label, label.get_rect(center=rect.center))
```

### Drawing the Reels

```python
REEL_SIZE = 120
REEL_GAP = 20
REEL_Y = 220

def reel_rects(num_reels, start_x=100):
    return [
        pygame.Rect(start_x + i * (REEL_SIZE + REEL_GAP), REEL_Y, REEL_SIZE, REEL_SIZE)
        for i in range(num_reels)
    ]

def draw_reels(screen, results, font):
    for symbol, rect in zip(results, reel_rects(len(results))):
        pygame.draw.rect(screen, (240, 240, 240), rect.inflate(10, 10), border_radius=12)  # reel frame
        draw_symbol(screen, symbol, rect, font)
```

### Clicking the Lever

```python
lever_rect = pygame.Rect(600, 200, 40, 160)

if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
    if lever_rect.collidepoint(event.pos) and player_stats["rolls_left"] > 0:
        results = spin_reels()
        player_stats["round_score"] += score_roll(results)
        player_stats["rolls_left"] -= 1
```

The space bar could also roll: `event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE`.

### Weighted Random Spins

This links pygame to our data structures: the **symbol_stats dictionary** sets the odds, and **lists** feed `random.choices`:

```python
import random

def spin_reels(num_reels=3):
    symbols = list(symbol_stats.keys())
    weights = [symbol_stats[s]["weight"] for s in symbols]
    return random.choices(symbols, weights=weights, k=num_reels)
```

An upgrade like *Diamond Mine* only needs to change the data: `symbol_stats["diamond"]["weight"] += 2`.

### Drawing the HUD

```python
def draw_hud(screen, font, stats, quota):
    lines = [
        f"Round: {stats['round']}",
        f"Rolls left: {stats['rolls_left']}",
        f"Score: {stats['round_score']} / {quota}",
    ]
    for i, line in enumerate(lines):
        screen.blit(font.render(line, True, (255, 255, 255)), (20, 20 + i * 36))
```

### Upgrade Selection Cards

Show 3 random upgrade options as clickable cards:

```python
def draw_upgrade_cards(screen, font, offers):
    cards = []
    for i, upgrade in enumerate(offers):
        rect = pygame.Rect(80 + i * 220, 200, 200, 260)
        pygame.draw.rect(screen, (50, 50, 80), rect, border_radius=14)
        pygame.draw.rect(screen, (200, 200, 255), rect, 3, border_radius=14)
        title = font.render(upgrade["name"], True, (255, 255, 255))
        screen.blit(title, title.get_rect(midtop=(rect.centerx, rect.y + 20)))
        cards.append((rect, upgrade))
    return cards   # check these with collidepoint on click
```

### A Simple Spin Animation (Stretch)

Swap in random symbols each frame for a short time, then show the real result:

```python
SPIN_DURATION = 800   # ms
spin_start = None

# when the lever is pulled:
spin_start = pygame.time.get_ticks()
final_results = spin_reels()

# each frame:
if spin_start is not None:
    if pygame.time.get_ticks() - spin_start < SPIN_DURATION:
        shown = random.choices(list(symbol_stats), k=3)   # flicker effect
    else:
        shown = final_results
        spin_start = None
```

---

## Common Gotchas

- **Forgetting `pygame.display.flip()`:** nothing appears on screen.
- **Not clearing the screen** (`screen.fill(...)`) each frame: old drawings smear across the window.
- **Not handling `pygame.QUIT`:** the window can't be closed.
- **Creating fonts or loading images inside the loop:** the game becomes slow.
- **Not calling `clock.tick()`:** the loop runs as fast as it can and uses 100% CPU.
- **y-axis direction:** larger y values are **lower** on the screen.
- **macOS:** the window may need focus before it receives keyboard events.

---

## Useful Resources

- Official docs: https://www.pygame.org/docs/
- `pygame.draw` reference: https://www.pygame.org/docs/ref/draw.html
- `pygame.Rect` reference: https://www.pygame.org/docs/ref/rect.html
- Built-in examples: `python -m pygame.examples.<name>` (e.g. `aliens`, `chimp`)
