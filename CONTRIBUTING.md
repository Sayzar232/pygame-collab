# Contributing to Pygame Collab 🎮

Thank you for your interest in contributing to **Pygame Collab**! We welcome games and contributions from developers of all skill levels. Whether you have built a small arcade clone, a puzzle game, or something totally unique, we would love to have it included in our launcher!

---

## 📑 Table of Contents

- [Getting Started](#-getting-started)
- [Step-by-Step: Adding a New Game](#-step-by-step-adding-a-new-game)
  - [1. Fork & Clone](#1-fork--clone)
  - [2. Create a Game Directory](#2-create-a-game-directory)
  - [3. Configure `metadata.json`](#3-configure-metadatajson)
  - [4. Add Game Code & Entry Point](#4-add-game-code--entry-point)
  - [5. Add an Icon (Optional but Recommended)](#5-add-an-icon-optional-but-recommended)
  - [6. Test Your Game](#6-test-your-game)
  - [7. Commit & Submit a Pull Request](#7-commit--submit-a-pull-request)
- [Game Development Guidelines](#-game-development-guidelines)
  - [Execution & Working Directory](#execution--working-directory)
  - [Graceful Exit](#graceful-exit)
  - [Dependencies & Third-Party Packages](#dependencies--third-party-packages)
  - [Screen Resolution & Display](#screen-resolution--display)
- [Manifest Reference (`metadata.json`)](#-manifest-reference-metadatajson)
- [Questions or Need Help?](#-questions-or-need-help)

---

## 🚀 Getting Started

1. Ensure you have **Python 3.10+** installed.
2. Clone your fork and set up dependencies:
   ```bash
   pip install pygame
   ```
3. Test that the launcher runs locally:
   ```bash
   python main.py
   ```

---

## 🕹️ Step-by-Step: Adding a New Game

### 1. Fork & Clone

Fork the repository on GitHub, then clone your fork locally:
```bash
git clone https://github.com/<your-username>/pygame-collab.git
cd pygame-collab
git checkout -b game/your-game-name
```

### 2. Create a Game Directory

Create a folder inside `games/` using lowercase alphanumeric characters and underscores (e.g., `games/pong`, `games/space_invaders`):

```text
games/
└── your_game_name/
    ├── metadata.json       # Required manifest file
    ├── main.py             # Entry point script
    ├── icon.png            # Optional cover image
    └── assets/             # Sounds, sprites, fonts, etc.
```

> **Note:** Keep all your assets, extra Python modules, and files contained inside your game's folder!

### 3. Configure `metadata.json`

Every game **must** contain a `metadata.json` file in its root directory with valid UTF-8 encoding:

```json
{
  "name": "Super Space Dodger",
  "author": "YourGitHubUsername",
  "description": "Dodge incoming asteroids and score points in space!",
  "version": "1.0.0",
  "icon": "icon.png",
  "entry_point": "main.py"
}
```

#### Fields Description:
- `name` *(string, required)*: The title displayed on the launcher card.
- `author` *(string, required)*: Your name or GitHub username.
- `description` *(string, required)*: A short description of your game (1-3 sentences).
- `icon` *(string, optional)*: Relative path to your icon image (e.g. `icon.png`). If omitted or missing, a styled placeholder is displayed.
- `entry_point` *(string, optional)*: Main Python file to run (defaults to `"main.py"`).
- `version` *(string, optional)*: Version tag (defaults to `"1.0.0"`).

### 4. Add Game Code & Entry Point

Place your game logic in the entry point file specified in `metadata.json` (usually `main.py`).

Example minimal entry point:

```python
import pygame
import sys

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Super Space Dodger")
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        screen.fill((20, 20, 30))
        # Draw your game here
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
```

### 5. Add an Icon (Optional but Recommended)

- **Resolution:** A square image, ideally `250x250` pixels (or higher like `512x512`).
- **Format:** PNG or JPG.
- **Location:** Put it in your game folder (e.g. `games/your_game_name/icon.png`) and specify the filename in `metadata.json`.

### 6. Test Your Game

1. **Standalone Test:** Run your game directly:
   ```bash
   python games/your_game_name/main.py
   ```
2. **Launcher Test:** Run the launcher and launch your game by clicking its card:
   ```bash
   python main.py
   ```
3. Check the console for any errors or warnings.

### 7. Commit & Submit a Pull Request

```bash
git add games/your_game_name
git commit -m "Add <Game Name> by @your-username"
git push origin game/your-game-name
```

Then visit GitHub and open a **Pull Request** to the `main` branch.

---

## 🎯 Game Development Guidelines

### Execution & Working Directory
The launcher launches games as separate subprocesses:
```python
subprocess.Popen([sys.executable, entry_point], cwd=game_directory)
```
- The current working directory (`cwd`) is automatically set to your game's directory.
- Always load assets using relative paths, for example: `pygame.image.load("assets/player.png")`.
- Do not hardcode absolute paths or assume the working directory is the repository root.

### Graceful Exit
- Always listen for `pygame.QUIT` and quit cleanly:
  ```python
  if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
  ```
- It is good practice to allow players to return to the launcher by pressing `ESC` or a Pause/Menu button.
- Because each game runs in its own process, closing the game will not terminate the launcher.

### Dependencies & Third-Party Packages
- **Pygame** and the Python Standard Library are supported out of the box.
- Avoid introducing heavy third-party dependencies. If your game requires an extra library, mention it in your Pull Request description so maintainers can review it.

### Screen Resolution & Display
- You can set any screen resolution and FPS suitable for your game.
- Fullscreen mode is allowed, but ensure players have an intuitive way to exit (e.g. `ESC`).

---

## 📋 Manifest Reference (`metadata.json`)

| Field | Type | Required? | Default | Description |
|---|---|---|---|---|
| `name` | string | **Yes** | — | Display title of the game. |
| `author` | string | **Yes** | — | Author's name or GitHub username. |
| `description` | string | **Yes** | — | 1-3 sentence summary of the game. |
| `entry_point` | string | No | `"main.py"` | Python script to execute on launch. |
| `icon` | string | No | — | Relative filename of the cover image. |
| `version` | string | No | `"1.0.0"` | Game release version. |

---

## 💬 Questions or Need Help?

Feel free to open an **Issue** or start a **Discussion** on GitHub if you need assistance or have ideas to improve Pygame Collab. Happy coding!

