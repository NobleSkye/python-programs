import os
import sys
import subprocess
import time
import datetime
import random
import socket
import readline
import json
from tqdm import tqdm
from getpass import getpass

# Games available in the system
GAMES = ['tictactoe', 'pong', 'snake', 'hangman', 'numguess', 'adventure', 'ttt-gui', 'pong-gui']

# Available commands for auto-completion
COMMANDS = ['exit', 'quit', 'cd', 'ls', 'pwd', 'clear', 'cat', 'echo', 'help', 'date', 'time',
           'whoami', 'hostname', 'uptime', 'ps', 'games', 'mkdir', 'touch', 'rm', 'cp', 'mv', 'config', 'su'] + GAMES

class Completer:
    def __init__(self, commands):
        self.commands = commands
        self.current_candidates = []

    def complete(self, text, state):
        if state == 0:
            # First time for this text, build a match list
            line = readline.get_line_buffer()
            begin = readline.get_begidx()
            end = readline.get_endidx()
            being_completed = line[begin:end]
            words = line.split()

            if not words:
                # Empty line, show all commands
                self.current_candidates = self.commands
            else:
                # If we're completing a command (first word)
                if begin == 0:
                    candidates = self.commands
                # If we're completing a game name after 'games' command
                elif words[0] == 'games' and len(words) <= 2:
                    candidates = GAMES
                # If we're completing a file path
                else:
                    # Get the directory part of the path being completed
                    path = os.path.dirname(being_completed)
                    if not path:
                        path = '.'
                    # Get all files/directories in that path
                    try:
                        candidates = os.listdir(path)
                    except OSError:
                        candidates = []

                # Filter candidates that match what the user has typed
                if being_completed:
                    self.current_candidates = [w for w in candidates
                                            if w.startswith(being_completed)]
                else:
                    self.current_candidates = candidates

            self.current_candidates.sort()

        try:
            return self.current_candidates[state]
        except IndexError:
            return None

# Set up readline configuration
completer = Completer(COMMANDS)
readline.set_completer(completer.complete)
readline.parse_and_bind('"\e[A": previous-history')  # Up arrow
readline.parse_and_bind('"\e[B": next-history')      # Down arrow
readline.parse_and_bind('"\e[C": forward-char')      # Right arrow
readline.parse_and_bind('"\e[D": backward-char')     # Left arrow
readline.parse_and_bind('tab: complete')             # Tab completion
readline.set_history_length(1000)  # Set history size

# Initialize history file
HISTFILE = os.path.join(os.path.expanduser("~"), ".python_shell_history")
try:
    readline.read_history_file(HISTFILE)
except FileNotFoundError:
    pass

def save_history():
    try:
        readline.write_history_file(HISTFILE)
    except Exception:
        pass

hostname = "system"
base_dir_name = "system32"
games_dir_name = "games"
base_dir_path = os.path.join(os.getcwd(), base_dir_name)
games_dir_path = os.path.join(base_dir_path, games_dir_name)
# Path to the central password file
sys_password_file = os.path.join(base_dir_path, ".sys")
global current_dir
current_dir = base_dir_path
start_time = time.time()

# Fake system info
fake_packages = ["python3", "git", "gcc", "nano", "vim"]
fake_processes = [
    ("systemd", "1", "root", "0.0", "1:23"),
    ("sshd", "892", "root", "0.1", "0:45"),
    ("bash", "1234", "user", "0.0", "0:32"),
    ("python", "1567", str(os.getpid()), "1.2", "0:15")
]
command_history = []

# Ensure the base directory exists
if not os.path.exists(base_dir_path):
    os.mkdir(base_dir_path)

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def loading(range_value, sleep_time):
    for _ in tqdm(range(range_value)):
        time.sleep(sleep_time)

def startup():
    clear()
    print("Welcome to the Python Terminal Environment!")
    print("1) Existing user\n2) New user")
    while True:
        choice = input("Select an option (1 or 2): ").strip()
        if choice in ("1", "2"):
            break
        print("Invalid choice. Please enter 1 or 2.")

    users_dir = os.path.join(base_dir_path, "users")
    if not os.path.exists(users_dir):
        os.makedirs(users_dir)

    # Load or create the central password file
    if not os.path.exists(sys_password_file):
        with open(sys_password_file, 'w') as f:
            f.write("")

    def get_passwords():
        passwords = {}
        with open(sys_password_file, 'r') as f:
            for line in f:
                if ':' in line:
                    u, p = line.strip().split(':', 1)
                    passwords[u] = p
        return passwords

    def set_password(username, password):
        passwords = get_passwords()
        passwords[username] = password
        with open(sys_password_file, 'w') as f:
            for u, p in passwords.items():
                f.write(f"{u}:{p}\n")

    if choice == "2":
        # New user signup
        while True:
            user = input("Choose a username: ").strip()
            if not user:
                print("Username cannot be empty.")
                continue
            if ' ' in user:
                print("Username cannot contain spaces.")
                continue
            break
        user_dir = os.path.join(users_dir, user)
        passwords = get_passwords()
        if user in passwords:
            print("User already exists. Please log in as an existing user.")
            input("Press Enter to continue...")
            clear()
            return startup()
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        password = getpass('Set password: ')
        set_password(user, password)
        print("Account created. Please log in as an existing user.")
        input("Press Enter to continue...")
        clear()
        return startup()
    else:
        # Existing user login
        user = input("Login: ").strip()
        user_dir = os.path.join(users_dir, user)
        passwords = get_passwords()
        if user not in passwords or not os.path.exists(user_dir):
            print("User does not exist. Please sign up as a new user.")
            input("Press Enter to continue...")
            clear()
            return startup()
        password = getpass('Password: ')
        if password != passwords[user]:
            print("Login failed. Try again.")
            input("Press Enter to continue...")
            clear()
            return startup()
    clear()
    command_loop(user, base_dir_path)

def list_directory(args):
    """List contents of a directory"""
    target = args[0] if args else '.'
    path = resolve_path(target)
    if path:
        try:
            for item in sorted(os.listdir(path)):
                if not config.get("show_hidden_files") and item.startswith('.'):
                    continue
                if os.path.isdir(os.path.join(path, item)):
                    print(f"{item}/")
                else:
                    print(item)
        except OSError as e:
            print(f"Error listing directory: {e}")

def change_directory(args):
    """Change current directory"""
    global current_dir
    if not args:
        current_dir = base_dir_path
        return
    
    path = resolve_path(args[0])
    if path and os.path.isdir(path):
        current_dir = path
    else:
        print("Directory not found or access denied.")

def cat_file(args):
    """Display contents of a file"""
    if not args:
        print("Error: No file specified")
        return

    path = resolve_path(args[0])
    if path:
        filename = os.path.basename(path)
        # Require sudo for .sys file
        if filename == ".sys":
            print("sudo password required to view this file.")
            sudo_password = getpass('Password: ')
            # Check password for current user
            def get_passwords():
                passwords = {}
                with open(sys_password_file, 'r') as f:
                    for line in f:
                        if ':' in line:
                            u, p = line.strip().split(':', 1)
                            passwords[u] = p
                return passwords
            passwords = get_passwords()
            current_user = os.environ.get('USER', 'user')
            if current_user not in passwords or sudo_password != passwords[current_user]:
                print("Sorry, try again. (sudo: incorrect password)")
                return
        try:
            with open(path, 'r') as f:
                print(f.read(), end='')
        except IOError as e:
            print(f"Error reading file: {e}")

def launch_game(args):
    """Launch a game from the games directory"""
    if not args:
        print("Available games:")
        for game in GAMES:
            print(f"  {game}")
        return
        
    game_name = args[0]
    if game_name not in GAMES:
        print(f"Unknown game: {game_name}")
        return
        
    game_path = os.path.join(games_dir_path, f"{game_name}.py")
    try:
        if os.path.exists(game_path):
            subprocess.run([sys.executable, game_path])
        else:
            print(f"Error: Game file not found at {game_path}")
    except Exception as e:
        print(f"Error launching game: {e}")

def resolve_path(path):
    """Resolve and validate a path"""
    if not path:
        return current_dir
        
    abs_path = os.path.abspath(os.path.join(current_dir, path))
    if abs_path.startswith(base_dir_path):
        return abs_path
    else:
        print("Access denied: Cannot access paths outside the system directory.")
        return None

def execute_command(cmd_parts, input_data=None, user=None):
    """Execute a single command and return its output"""
    if user is None:
        user = "user"  # fallback value
    users_dir = os.path.join(base_dir_path, "users")
    cmd = cmd_parts[0]
    args = cmd_parts[1:]
    
    # Capture output in a string buffer
    from io import StringIO
    import sys
    old_stdout = sys.stdout
    output_buffer = StringIO()
    sys.stdout = output_buffer
    
    try:
        su_user_result = None
        # Add direct game execution check before other commands
        if cmd in GAMES:
            launch_game([cmd])
        elif cmd == 'ls':
            list_directory(args)
        elif cmd == 'cd':
            change_directory(args)
        elif cmd == 'pwd':
            print(os.path.relpath(current_dir, base_dir_path))
        elif cmd == 'echo':
            print(' '.join(args))
        elif cmd == 'cat':
            cat_file(args)
        elif cmd == 'nano':
            # Only allow nano if not editing .sys, or require sudo for .sys
            if args and len(args) >= 1:
                filename = args[0]
                if os.path.basename(filename) == ".sys":
                    print("sudo password required to edit this file.")
                    sudo_password = getpass('Password: ')
                    def get_passwords():
                        passwords = {}
                        with open(sys_password_file, 'r') as f:
                            for line in f:
                                if ':' in line:
                                    u, p = line.strip().split(':', 1)
                                    passwords[u] = p
                        return passwords
                    passwords = get_passwords()
                    current_user = user if user else os.environ.get('USER', 'user')
                    if current_user not in passwords or sudo_password != passwords[current_user]:
                        print("Sorry, try again. (sudo: incorrect password)")
                        return output_buffer.getvalue(), None
            # Actually run nano
            try:
                subprocess.run(["nano"] + args)
            except Exception as e:
                print(f"Error running nano: {e}")
        elif cmd == 'games':
            launch_game(args)
        elif cmd == 'config':
            # Require sudo for config changes
            if args and len(args) == 2:
                # Editing config, require sudo
                print("sudo password required to edit config.")
                sudo_password = getpass('Password: ')
                def get_passwords():
                    passwords = {}
                    with open(sys_password_file, 'r') as f:
                        for line in f:
                            if ':' in line:
                                u, p = line.strip().split(':', 1)
                                passwords[u] = p
                    return passwords
                passwords = get_passwords()
                current_user = user if user else os.environ.get('USER', 'user')
                if current_user not in passwords or sudo_password != passwords[current_user]:
                    print("Sorry, try again. (sudo: incorrect password)")
                    return output_buffer.getvalue(), None
            handle_config_command(args)
        elif cmd == 'clear':
            clear()
        elif cmd == 'date':
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        elif cmd == 'time':
            print(datetime.datetime.now().strftime("%H:%M:%S"))
        elif cmd == 'whoami':
            print(user)
        elif cmd == 'hostname':
            print(hostname)
        elif cmd == 'su':
            if not args:
                print("su: Missing all arguments")
            else:
                su_user = args[0]
                su_user_dir = os.path.join(users_dir, su_user)
                su_password_file = os.path.join(su_user_dir, ".password")
                if not os.path.exists(su_user_dir) or not os.path.exists(su_password_file):
                    print("su: User does not exist")
                else:
                    su_password = getpass('Password: ')
                    with open(su_password_file, 'r') as f:
                        real_su_password = f.read().strip()
                    if su_password == real_su_password:
                        print(f"Switched to user: {su_user}")
                        su_user_result = su_user
                    else:
                        print("su: Authentication failure")

        elif cmd == 'uptime':
            uptime = time.time() - start_time
            hours = int(uptime // 3600)
            minutes = int((uptime % 3600) // 60)
            print(f"Up {hours} hours, {minutes} minutes")
        elif cmd == 'ps':
            for proc in fake_processes:
                print(f"{proc[0]:15} {proc[1]:6} {proc[2]:8} {proc[3]:5} {proc[4]}")
        elif cmd == 'mkdir':
            if not args:
                print("Error: No directory name specified")
            else:
                path = resolve_path(args[0])
                if path:
                    try:
                        os.mkdir(path)
                    except OSError as e:
                        print(f"Error creating directory: {e}")
        elif cmd == 'touch':
            if not args:
                print("Error: No file name specified")
            else:
                path = resolve_path(args[0])
                if path:
                    try:
                        with open(path, 'a'):
                            os.utime(path, None)
                    except OSError as e:
                        print(f"Error touching file: {e}")
        elif cmd == 'rm':
            if not args:
                print("Error: No file specified")
            else:
                path = resolve_path(args[0])
                if path:
                    try:
                        if os.path.isdir(path):
                            if '-r' in args or '--recursive' in args:
                                import shutil
                                shutil.rmtree(path)
                            else:
                                print("Error: Is a directory. Use -r to remove directories")
                        else:
                            os.remove(path)
                    except OSError as e:
                        print(f"Error removing: {e}")
        elif cmd == 'cp':
            if len(args) < 2:
                print("Error: Source and destination required")
            else:
                src = resolve_path(args[0])
                dst = resolve_path(args[1])
                if src and dst:
                    try:
                        if os.path.isdir(src):
                            if '-r' in args or '--recursive' in args:
                                import shutil
                                shutil.copytree(src, dst)
                            else:
                                print("Error: Is a directory. Use -r to copy directories")
                        else:
                            import shutil
                            shutil.copy2(src, dst)
                    except OSError as e:
                        print(f"Error copying: {e}")
        elif cmd == 'mv':
            if len(args) < 2:
                print("Error: Source and destination required")
            else:
                src = resolve_path(args[0])
                dst = resolve_path(args[1])
                if src and dst:
                    try:
                        import shutil
                        shutil.move(src, dst)
                    except OSError as e:
                        print(f"Error moving: {e}")
        elif cmd == 'help':
            print("Available commands:")
            print("  ls         - List directory contents")
            print("  cd         - Change directory")
            print("  pwd        - Print working directory")
            print("  echo       - Print text")
            print("  cat        - Print file contents")
            print("  clear      - Clear screen")
            print("  date       - Show current date and time")
            print("  time       - Show current time")
            print("  whoami     - Show current user")
            print("  hostname   - Show system hostname")
            print("  uptime     - Show system uptime")
            print("  ps         - List processes")
            print("  mkdir      - Create directory")
            print("  touch      - Create empty file")
            print("  rm [-r]    - Remove file or directory")
            print("  cp [-r]    - Copy file or directory")
            print("  mv         - Move/rename file or directory")
            print("  games      - List and launch games")
            print("  config     - View/edit configuration")
            print("  exit/quit  - Exit shell")
            print("  su [user]  - Switch user accounts")
        elif cmd in ['exit', 'quit']:
            print("Goodbye!")
            save_history()
            sys.exit(0)
        else:
            print(f"Unknown command: {cmd}")
            print("Type 'help' for a list of commands")
    finally:
        sys.stdout = old_stdout

    return output_buffer.getvalue(), su_user_result

def get_prompt(user, hostname, rel_path):
    """Get command prompt based on config"""
    if config.get("prompt_style") == "minimal":
        return "$ "
    return f"{user}@{hostname}:{rel_path}$ "

def handle_config_command(args):
    """Handle the config command"""
    if not args:
        # Show current config
        for key, value in config.settings.items():
            print(f"{key}={value}")
        return
        
    if len(args) == 1:
        # Show specific config value
        key = args[0]
        if key in config.settings:
            print(f"{key}={config.settings[key]}")
        else:
            print(f"Unknown config key: {key}")
        return
            
    if len(args) == 2:
        # Set config value
        key, value = args
        if key not in config.settings:
            print(f"Unknown config key: {key}")
            return
            
        # Convert string value to appropriate type
        if isinstance(config.settings[key], bool):
            value = value.lower() in ('true', 'yes', '1', 'on')
        elif isinstance(config.settings[key], list):
            value = value.split(',')
        elif isinstance(config.settings[key], dict):
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                print("Error: Invalid JSON for dictionary value")
                return
                
        config.set(key, value)
        print(f"Set {key}={value}")

def command_loop(user, initial_dir):
    global current_dir
    current_dir = initial_dir
    current_user = user
    while True:
        try:
            rel_path = os.path.relpath(current_dir, base_dir_path)
            prompt_path = '/' if rel_path == '.' else rel_path
            prompt = get_prompt(current_user, hostname, prompt_path)

            try:
                command = input(prompt).strip()
            except EOFError:
                print("\nUse 'exit' to quit.")
                continue

            if not command:
                continue

            # Add command to history
            readline.add_history(command)

            # Handle pipes and redirections
            commands = command.split('|')
            input_data = None

            # Process each command in the pipe
            for i, cmd in enumerate(commands):
                # Handle output redirection
                if '>' in cmd:
                    cmd_parts = cmd.split('>')
                    cmd = cmd_parts[0].strip()
                    outfile = cmd_parts[1].strip()
                    if not outfile:
                        print("Error: No output file specified")
                        break

                    # Execute the command
                    output, su_user_result = execute_command(cmd.split(), input_data, current_user)

                    # If su_user_result is not None, switch user
                    if su_user_result is not None:
                        current_user = su_user_result

                    # Write to file
                    try:
                        with open(os.path.join(current_dir, outfile), 'w') as f:
                            f.write(output)
                    except IOError as e:
                        print(f"Error writing to file: {e}")
                    break

                # Normal command or pipe
                output, su_user_result = execute_command(cmd.split(), input_data, current_user)
                if su_user_result is not None:
                    current_user = su_user_result
                if i < len(commands) - 1:
                    # This is not the last command, pass output as input to next command
                    input_data = output
                else:
                    # This is the last command, print output
                    print(output, end='')

            # Save history after each command
            save_history()

        except KeyboardInterrupt:
            print("\nUse 'exit' to quit.")
            continue
        except Exception as e:
            print(f"Error: {str(e)}")
            continue

class Config:
    def __init__(self):
        self.config_file = os.path.join(os.path.expanduser("~"), ".python_shell_config")
        self.defaults = {
            "prompt_style": "default",  # or "minimal"
            "show_hidden_files": False,
            "color_output": True,
            "favorite_games": [],
            "aliases": {}
        }
        self.settings = self.load_config()

    def load_config(self):
        try:
            with open(self.config_file, 'r') as f:
                return {**self.defaults, **json.load(f)}
        except FileNotFoundError:
            return self.defaults.copy()
        except json.JSONDecodeError:
            print("Warning: Config file corrupt, using defaults")
            return self.defaults.copy()

    def save_config(self):
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except IOError as e:
            print(f"Error saving config: {e}")

    def get(self, key):
        return self.settings.get(key, self.defaults.get(key))

    def set(self, key, value):
        if key in self.defaults:
            self.settings[key] = value
            self.save_config()
        else:
            print(f"Unknown config key: {key}")

# Initialize config
config = Config()

if __name__ == "__main__":
    startup()
