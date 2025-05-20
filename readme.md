# Python Terminal Environment

A customizable terminal environment written in Python with built-in games and command-line tools.

## 🚀 Getting Started

### Prerequisites

- Python 3.6 or higher ([Download from python.org](https://www.python.org/downloads/))
- pip (Python package manager, usually comes with Python)

### Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd python-programs
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   > 💡 **Tip**: If `pip` doesn't work, try using `pip3` instead.

### Running the Application

```bash
python main.py
```

> 💡 **Tip**: On some systems, you might need to use `python3 main.py` instead.

## 🎮 Games

The environment comes with several built-in games:
- Tic-tac-toe (Text & GUI versions)
- Pong (Text & GUI versions)
- Snake
- Hangman
- Number Guessing Game
- Text Adventure

To play a game:
1. Start the application
2. Type `games` to see the list of available games
3. Type `games game_name` to play (e.g., `games snake`)

> 💡 **Tip**: You can also type the game name directly as a command (e.g., `snake`)

## ⚙️ Configuration

Customize your environment using the `config` command:

```bash
config                          # Show all settings
config setting_name            # Show specific setting
config setting_name value     # Change setting
```

Available settings:
- `prompt_style`: "default" or "minimal"
- `show_hidden_files`: true/false
- `color_output`: true/false
- `favorite_games`: comma-separated list
- `aliases`: command shortcuts

## 🔒 Sandbox Environment

The application runs in a secure sandbox environment ("system32") that:
- Prevents access to your actual system files
- Provides a safe space for experimenting
- Automatically creates required directories

## 🤝 Contributing

Want to add your own games or features? We welcome contributions!
1. Fork the repository
2. Create your feature branch
3. Add your changes
4. Submit a Pull Request

## 📝 To Do

- [x] Create comprehensive README
- [ ] Add more Unix-like commands
- [x] Implement classic games collection