import os
import time
import random
import sys
import tty
import termios
import select

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def get_key():
    """Get a single keypress without blocking"""
    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    # Check if there's input waiting
    if select.select([sys.stdin], [], [], 0.1)[0]:
        return _getch()
    return None

def pong():
    width = 40
    height = 20
    paddle_left_pos = height // 2
    paddle_right_pos = height // 2
    ball_x = width // 2
    ball_y = height // 2
    ball_dx = 1
    ball_dy = random.choice([-1, 1])
    score_left = 0
    score_right = 0

    print("Welcome to Terminal Pong!")
    print("Left player: W/S keys")
    print("Right player: Up/Down arrow keys")
    print("Press Q to quit")
    time.sleep(2)

    def draw_board():
        clear()
        board = []
        # Create empty board
        for i in range(height):
            row = [' ' for _ in range(width)]
            board.append(row)
        
        # Add paddles
        for i in range(-2, 3):
            if 0 <= paddle_left_pos + i < height:
                board[paddle_left_pos + i][0] = '|'
            if 0 <= paddle_right_pos + i < height:
                board[paddle_right_pos + i][width-1] = '|'
        
        # Add ball
        if 0 <= ball_y < height and 0 <= ball_x < width:
            board[ball_y][ball_x] = 'O'
        
        # Print board
        print(f"Score: {score_left} - {score_right}")
        for row in board:
            print(''.join(row))

    try:
        while True:
            # Handle input
            key = get_key()
            if key:
                key = key.lower()
                if key == 'w' and paddle_left_pos > 2:
                    paddle_left_pos -= 1
                elif key == 's' and paddle_left_pos < height - 3:
                    paddle_left_pos += 1
                elif key == '\x1b':  # ESC sequence
                    # Read the next two characters for arrow keys
                    next1, next2 = sys.stdin.read(2)
                    if next1 == '[':
                        if next2 == 'A' and paddle_right_pos > 2:  # Up arrow
                            paddle_right_pos -= 1
                        elif next2 == 'B' and paddle_right_pos < height - 3:  # Down arrow
                            paddle_right_pos += 1
                elif key == 'q':
                    break

            # Ball movement
            ball_x += ball_dx
            ball_y += ball_dy

            # Ball collisions
            if ball_y <= 0 or ball_y >= height - 1:
                ball_dy *= -1

            # Paddle collisions
            if ball_x == 1 and abs(ball_y - paddle_left_pos) <= 2:
                ball_dx *= -1
            elif ball_x == width - 2 and abs(ball_y - paddle_right_pos) <= 2:
                ball_dx *= -1

            # Scoring
            if ball_x <= 0:
                score_right += 1
                ball_x = width // 2
                ball_y = height // 2
                ball_dx = 1
                ball_dy = random.choice([-1, 1])
            elif ball_x >= width - 1:
                score_left += 1
                ball_x = width // 2
                ball_y = height // 2
                ball_dx = -1
                ball_dy = random.choice([-1, 1])

            draw_board()
            time.sleep(0.1)

    except KeyboardInterrupt:
        pass
    finally:
        # Restore terminal settings
        termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, termios.tcgetattr(sys.stdin.fileno()))

    print("\nGame Over!")
    print(f"Final Score: {score_left} - {score_right}")

if __name__ == "__main__":
    pong()
