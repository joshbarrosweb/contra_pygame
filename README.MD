# Contra Pygame

This project is a recreation of the classic Contra game implemented in Python using the Pygame library.

## Special Thanks

Special thanks to the original Contra game developers for inspiring this project!

## Project Structure

The project has the following file and folder structure:

### `src`

This folder contains the source code files for the game:

- `main.py`: The main entry point of the game. It sets up the game, initiates the game loop, and manages the main game objects and logic.
- `bullet.py`: Contains the `Bullet` class which handles the behavior of bullets, including their movement and collision detection.
- `enemy.py`: Contains the `Enemy` class which represents the enemy entities in the game and defines their behavior and interactions with the player.
- `entity.py`: Contains the `Entity` class, a base class for all game characters, handling shared characteristics like movement, animation, health, and damage.
- `player.py`: Contains the `Player` class which represents the player character, handling player movement, shooting, health tracking, and input handling.
- `settings.py`: Contains global game settings and constants, such as window size and paths to assets.
- `tile.py`: Contains the `Tile` class which represents the tiles in the game world and their properties.
-  `overlay.py`: This file contains the `Overlay` class which manages the overlay displayed on the screen, such as the player's health bar.

### `resources`

This folder contains various resources used in the game:

- `graphics`: Contains the game's graphic files, organized into folders for different types of graphics, such as player, enemy, and backgrounds.
- `audio`: Contains the game's sound files, including sound effects and background music.

### `data`

This folder contains the game's data files:

- `map.tmx`: The game map file, specifying the layout of the game world, including tiles and entities.

## Instructions

To run the project, follow these steps:

1. Install Python 3 if you haven't already.
2. Install the Pygame library by running the command: `pip install pygame`.
3. Clone or download the project files to your local machine.
4. Navigate to the project directory.
5. Run the command: `python3 src/main.py`.

Make sure you have the required resources in the appropriate directories as shown in the folder structure.

Feel free to modify and explore the game to suit your needs.

Enjoy playing!
