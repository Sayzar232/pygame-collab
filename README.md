# Pygame Collab 🎮

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Library](https://img.shields.io/badge/library-pygame-green.svg)](https://www.pygame.org/)

**Pygame Collab** is an open-source collaborative game launcher built with Python and Pygame. It allows multiple developers to contribute their own mini-games to a shared arcade hub. 

Each game is isolated in its own folder, runs in its own process, and is automatically discovered and displayed in the launcher menu using a simple JSON manifest.

---

## 📋 Table of Contents

- [Features](#-features)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Launcher](#running-the-launcher)
- [How to Add Your Game (Contributing Guide)](#-how-to-add-your-game-contributing-guide)
  - [1. Directory Setup](#1-directory-setup)
  - [2. Metadata Specification (`metadata.json`)](#2-metadata-specification-metadatajson)
  - [3. Icon Guidelines](#3-icon-guidelines)
  - [4. Game Code Guidelines](#4-game-code-guidelines)
  - [5. Submitting Your Game](#5-submitting-your-game)
- [Architecture & Design Details](#-architecture--design-details)
- [License](#-license)

---

## ✨ Features

- **Automatic Game Discovery:** Automatically scans the `games/` directory and generates interactive game cards.
- **Process Isolation:** Games run via independent subprocesses using `sys.executable`. If a game crashes or calls `pygame.quit()`, the main launcher stays open.
- **Independent Window Sizes:** Each game can configure its own window resolution, FPS, and display modes without conflicting with the launcher.
- **Safe Asset Resolution:** The working directory (`cwd`) is automatically set to the game's folder when launched, so relative paths like `pygame.image.load("icon.png")` work out of the box.
- **Robust Validation & Fallbacks:** Validates metadata and paths, includes graceful fallbacks for missing/corrupted icons, and formats text cleanly with auto-wrap and truncation.


## 📁 Project Structure

```text
pygame_collab/
│
├── launcher.py          # Launcher engine (menu, card rendering, game discovery)
├── main.py              # Main entry point to start the launcher
├── README.md            # Project documentation and contributor guide
│
└── games/               # Directory containing all contributed games
    └── snake/           # Example game directory
        ├── metadata.json# Game manifest
        ├── icon.png     # Game icon
        └── main.py      # Entry point script
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+**
- **pip** package manager

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Sayzar232/pygame-collab.git
   cd pygame_collab
   ```

2. **Create and activate a virtual environment (recommended):**
   - **Windows:**
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - **Linux / macOS:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies:**
   ```bash
   pip install pygame
   ```

### Running the Launcher

To launch the menu:
```bash
python main.py
```

Click on any game card to launch it!

---

## 🛠️ How to Add Your Game (Contributing Guide)

We welcome contributions from developers of all skill levels! Follow the steps below to add your game.

### 1. Directory Setup

Create a new folder inside `games/` with a unique, concise name (use lowercase letters, numbers, or underscores):

```text
games/my_awesome_game/
├── metadata.json
├── icon.png
└── main.py
```


### 2. Metadata Specification (`metadata.json`)

Every game folder must include a `metadata.json` file in UTF-8 encoding:

```json
{
    "name": "My Awesome Game",
    "author": "YourGitHubUsername",
    "description": "A fun retro arcade game where you avoid obstacles.",
    "version": "1.0.0",
    "icon": "icon.png",
    "entry_point": "main.py"
}
```

#### Field Specifications:

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `name` | string | **Yes** | — | Display title of the game. |
| `author` | string | **Yes** | — | Author's name or GitHub username. |
| `description` | string | **Yes** | — | Short description (1-3 sentences). |
| `icon` | string | **Yes** | — | Relative filename of the icon (e.g. `icon.png`). |
| `entry_point` | string | No | `"main.py"` | Relative script file executed on launch. |
| `version` | string | No | `"1.0.0"` | Current version string. |

### 3. Icon Guidelines

- **Dimensions:** Square image, preferably `250x250` pixels (or higher, e.g. `512x512`).
- **Format:** PNG or JPG.
- **Safety:** If the icon is missing or cannot be loaded, the launcher automatically renders a styled fallback card placeholder.

### 4. Game Code Guidelines

1. **Standalone Execution:** Make sure your game can be run directly from its own directory:
   ```bash
   python games/my_awesome_game/main.py
   ```
2. **Relative File Paths:** Because the launcher runs your game with `cwd` set to your game's directory, you can load images, sounds, and fonts with local paths:
   ```python
   # Correct:
   image = pygame.image.load("assets/player.png")
   ```
3. **Clean Exit:** Handle the `pygame.QUIT` event properly by breaking your main game loop and exiting cleanly:
   ```python
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           running = False
   ```
4. **Dependencies:** Stick to the Python standard library and `pygame`. If your game requires extra third-party libraries, note them in your pull request so they can be reviewed.

### 5. Submitting Your Game

1. **Fork** the repository.
2. Create a new feature branch:
   ```bash
   git checkout -b game/my-awesome-game
   ```
3. Commit your changes:
   ```bash
   git add games/my_awesome_game
   git commit -m "Add My Awesome Game"
   ```
4. Push to your branch and open a **Pull Request**.

---

## 🏗️ Architecture & Design Details

- **Subprocess Execution:**
  Instead of importing each game as a dynamic module, the launcher executes:
  ```python
  subprocess.Popen([sys.executable, entry_file.name], cwd=str(game_path))
  ```
  This guarantees that:
  - Global Pygame states (fonts, audio channels, display surfaces) never pollute the launcher.
  - A crash or `sys.exit()` in one game will never bring down the launcher.
  - Games run smoothly in parallel or independently while the menu remains responsive.

- **Security & Path Resolution:**
  All paths (`icon`, `entry_point`) are resolved and verified to prevent path traversal outside the game folder.

---

