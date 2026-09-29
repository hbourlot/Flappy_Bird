# Flappy Bird

A small Flappy Bird clone written in Python with [pygame](https://www.pygame.org/). Fly through the pipes, avoid crashing, and try to beat your high score.

## Requirements

- Python 3.8+
- pygame (includes `pygame.mixer`, used for sound)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/hbourlot/Flappy_Bird.git
    cd Flappy_Bird
    ```

2. Create a virtual environment and install the dependencies:

    ```bash
    python3 -m venv myvenv
    source myvenv/bin/activate      # macOS / Linux
    # myvenv\Scripts\activate       # Windows

    pip install -r requirements.txt
    ```

    Or, if you don't want a virtual environment:

    ```bash
    pip install pygame
    ```

## Run the game

```bash
python game.py
```

## Controls

| Key     | Action      |
| ------- | ----------- |
| `Space` | Flap / jump |
| `Esc`   | Quit        |

## Project structure

```
.
├── game.py            # entry point, run this file
├── configs.py         # game settings (window size, speeds, etc.)
├── src/               # game source code
├── assets/            # images and sounds
├── requirements.txt   # dependencies
└── README.md
```

## Troubleshooting

- **`ModuleNotFoundError: No module named 'pygame'`**: activate your virtual environment (`source myvenv/bin/activate`) or run `pip install pygame`.
- **No sound / mixer error**: make sure your system has an audio output device available. `pygame.mixer` needs one to initialize.

## License

Feel free to use and modify this project. Add a license file if you want to make the terms explicit.
