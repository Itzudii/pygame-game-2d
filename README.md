# 2D Platformer Game

A 2D platformer game built with **Python and Pygame**, using **Tiled** for level design.

The game focuses on platforming, movement, exploration, collectibles, traps, and progressively challenging levels.

> **Note:** The game does not currently contain all 50 designed levels. The goal is to support creating and adding levels through Tiled.

---

## 🎮 Game Concept

The player travels through platforming levels using movement abilities and environmental objects.

The main gameplay loop is:

```text
Explore
   ↓
Navigate platforms
   ↓
Avoid traps
   ↓
Collect fruits
   ↓
Reach the end
```

Levels are designed to gradually introduce new mechanics and then combine previously learned mechanics.

---

# 🧑 Player

The player currently has the following movement abilities:

* Move right
* Move left
* Jump
* Double jump
* Slide on walls
* Wall slide on both sides
* Wall jump from either side
* Use wall-jump mechanics to climb vertical areas

The movement system is an important part of level design, so levels can contain both horizontal and vertical challenges.

---

# 🍎 Fruits

Fruits are collectible objects.

The player collects a fruit by touching it.

Fruits can be placed:

* Along the main route
* On elevated platforms
* In difficult areas
* In optional routes
* In areas that encourage exploration

Fruits are mainly used to encourage exploration and reward skilled movement.

---

# ⚠️ Traps & Gameplay Objects

## Arrow

The arrow launches the player when the player collides with it.

Features:

* Configurable jump/launch power
* Activates when the player touches it
* Disappears after activation
* Single-use

---

## Trampoline

The trampoline also launches the player upward.

Features:

* Launches the player
* Does not disappear
* Can be used repeatedly
* Useful for vertical movement and reaching higher platforms

---

## Saw

The saw is a moving damaging obstacle.

Features:

* Moves along a custom path
* Damages the player when active/contacted
* Path is defined separately in the Tiled map

---

## Moving Platform

Moving platforms follow custom paths.

Features:

* Custom movement path
* Can move horizontally
* Can move vertically
* Can be used to cross gaps
* Can be combined with other traps

---

## Falling Platform

The falling platform is a temporary platform.

Features:

* Static before activation
* Player stands on it
* Platform falls
* Platform disappears
* Can only be used once

---

## Fan

The fan provides upward movement.

Features:

* Player above the fan is levitated upward
* Useful for vertical level sections
* Can be combined with platforms, walls, and other traps

---

## Fire

Fire is a timing-based damaging obstacle.

It has two states:

### Idle

The fire is inactive and does not damage the player.

### Fire

The fire becomes active and damages the player.

This allows fire to work as:

* A timing obstacle
* A temporary gate
* A repeated hazard

---

## Spikes

Spikes are static damaging obstacles.

Features:

* Do not move
* Damage the player on collision
* Can be placed on floors or other surfaces

---

# 🗺️ Level Design

Levels are created using **Tiled Map Editor**.

The game is designed to support many levels, with the long-term goal of creating approximately **50 levels**.

The 50-level progression is planned around gradually introducing mechanics.

## Planned Progression

```text
1–6    → Player movement
7–10   → Spikes
11–15  → Falling platforms
16–20  → Moving platforms
21–25  → Trampolines
26–30  → Arrows
31–35  → Fans
36–40  → Saws
41–45  → Fire
46–50  → Combined mechanics / mastery
```

The actual levels can be designed and created by the developer in Tiled.

The progression is intended to follow:

```text
Introduce
    ↓
Learn
    ↓
Practice
    ↓
Combine
    ↓
Master
```

The game should avoid making levels repetitive by simply adding more traps.

Instead, previously introduced mechanics should be reused in new situations.

---

# 🧩 Tiled Map Structure

Every map must contain the following layers:

```python
layers = {
    "normal_tile": Layer.NORMAL,
    "background_tile": Layer.NORMAL,
    "collision_normal_tile": Layer.COLLIDE,
    "decoration_object_layer": Layer.DECORATION,
    "decoration_object_layer_foreground": Layer.DECORATION,
    "object_layer": Layer.OBJECT,
    "traps_layer": Layer.OBJECT,
    "paths_layer": Layer.SHAPE,
    "buttons": Layer.OBJECT,
}
```

These layer names are part of the map structure and should be present in each level.

---

# 📐 Layer Responsibilities

## `normal_tile`

Contains the normal visual tiles of the level.

```text
Purpose:
Visual rendering only
```

Normal tiles are **not automatically collision objects**.

---

## `background_tile`

Contains background tiles.

```text
Purpose:
Background visuals
```

These tiles are used for the visual background and do not represent gameplay collision.

---

## `collision_normal_tile`

Contains the actual collision geometry.

```text
Purpose:
Player/environment collision
```

The collision layer uses **rectangles** to define solid areas.

For example:

```text
x = 16
y = 80
width = 48
height = 16
```

This means the visual tiles and collision geometry are separated.

The map can therefore contain decorative/visual tiles without making them automatically solid.

---

## `decoration_object_layer`

Contains background decoration objects.

```text
Purpose:
Decoration behind gameplay
```

These objects are visual and are not intended to control gameplay.

---

## `decoration_object_layer_foreground`

Contains foreground decoration objects.

```text
Purpose:
Decoration drawn in front of gameplay
```

This can be used for objects that visually appear in front of the player.

---

## `object_layer`

Contains normal game objects.

Examples include:

```text
Start
End
Flag
Fruits
Other gameplay objects
```

The uploaded map already uses this layer for objects such as `start`, `end`, `flag`, and different fruits.

---

## `traps_layer`

Contains traps and gameplay hazards.

Examples:

```text
Arrow
Trampoline
Saw
Moving Platform
Falling Platform
Fan
Fire
Spikes
```

Traps can also contain custom properties.

For example, a saw can reference a path:

```text
path → path object ID
```

---

## `paths_layer`

Contains paths used by moving objects.

Paths are created as Tiled shape objects, such as polylines.

For example:

```text
Start point ───────────────→ End point
```

The moving object references the corresponding path object.

The current map uses this system for saws and moving platforms.

---

## `buttons`

Contains button objects.

```text
Purpose:
Buttons / future interactive mechanics
```

The layer is currently part of the required map structure so button-based mechanics can be added without changing the map architecture.

---

# 🏗️ Map Architecture

The level system separates **visuals, collision, objects, traps, and movement paths**.

```text
                 TILED MAP
                     │
        ┌────────────┼────────────┐
        │            │            │
     Visuals      Collision     Objects
        │            │            │
   ┌────┴────┐       │       ┌────┴────┐
   │         │       │       │         │
Normal    Background │     Start     Fruits
Tiles      Tiles     │      End       Flags
                     │
               Rectangles
                     │
                     ▼
                 Player
                 Collision

              Traps / Hazards
                     │
              ┌──────┴──────┐
              │             │
           Traps          Paths
              │             │
        Saw / Platform ─────┘
```

---

# 🎨 Level Creation Workflow

Levels are created manually using Tiled.

Recommended workflow:

```text
1. Create the map
       ↓
2. Design background
       ↓
3. Add normal visual tiles
       ↓
4. Add collision rectangles
       ↓
5. Add start/end objects
       ↓
6. Add fruits
       ↓
7. Add traps
       ↓
8. Create paths for moving objects
       ↓
9. Add decorations
       ↓
10. Test the level in the game
```

---

# 📋 Level Design Principles

Each level should have a clear purpose.

Examples:

```text
Level 1
Basic movement

Level 2
Jumping / double jump

Level 3
Double-jump exploration

Level 4
Wall movement

...

Later levels
Combine previously learned mechanics
```

A new mechanic should not immediately be combined with every other mechanic.

Instead:

```text
New mechanic
     ↓
Simple introduction
     ↓
Practice
     ↓
More difficult use
     ↓
Combination with older mechanics
```

This keeps the player's journey interesting and prevents the game from becoming repetitive.

---

# 🎯 Long-Term Goal

The game aims to provide a **50-level platforming journey** where players gradually discover and master:

* Movement
* Double jump
* Wall movement
* Fruits
* Spikes
* Falling platforms
* Moving platforms
* Trampolines
* Arrows
* Fans
* Saws
* Fire
* Combined challenges

The level system is designed so that **new levels can be created directly in Tiled without changing the fundamental map architecture**.

---

# 🛠️ Technology

* **Python**
* **Pygame**
* **Tiled Map Editor**
* **TMJ/TMX map format**
* **PyTMX / custom Tiled map handling**

---

# 📌 Current Status

### Implemented concepts

* Player movement
* Double jump
* Wall slide
* Wall jump
* Fruits
* Arrow
* Trampoline
* Saw
* Moving platforms
* Falling platforms
* Fan
* Fire
* Spikes
* Tiled-based maps
* Separate collision layer
* Separate object layer
* Separate trap layer
* Custom paths
* Decoration layers
* Button layer

### Level status

The game is **not currently limited to a fixed set of 50 levels**.

The 50-level structure is a **planned progression**. Individual levels can be created and designed using Tiled while following the required layer structure.
