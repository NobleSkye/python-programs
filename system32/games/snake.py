import os
import random
import time
import keyboard

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def snake():
    width = 20
    height = 20
    snake_x = width // 2
    snake_y = height // 2
    snake_body = [(snake_x, snake_y)]
    food_x = random.randint(0, width - 1)
    food_y = random.randint(0, height - 1)
    direction = 'right'
    score = 0
    game_over = False

    print("Welcome to Snake!")
    print("Use arrow keys to move")
    print("Press Q to quit")
    time.sleep(2)

    def draw_board():
        clear()
        board = []
        for i in range(height):
            row = ['·' for _ in range(width)]
            board.append(row)
        
        # Draw snake
        for x, y in snake_body:
            if 0 <= x < width and 0 <= y < height:
                board[y][x] = '■'
        
        # Draw food
        board[food_y][food_x] = '●'
        
        print(f"Score: {score}")
        for row in board:
            print(''.join(row))

    try:
        while not game_over:
            draw_board()
            
            # Handle input
            if keyboard.is_pressed('left') and direction != 'right':
                direction = 'left'
            elif keyboard.is_pressed('right') and direction != 'left':
                direction = 'right'
            elif keyboard.is_pressed('up') and direction != 'down':
                direction = 'up'
            elif keyboard.is_pressed('down') and direction != 'up':
                direction = 'down'
            elif keyboard.is_pressed('q'):
                break

            # Move snake
            new_x = snake_body[0][0]
            new_y = snake_body[0][1]
            
            if direction == 'up':
                new_y -= 1
            elif direction == 'down':
                new_y += 1
            elif direction == 'left':
                new_x -= 1
            elif direction == 'right':
                new_x += 1

            # Check collision with walls
            if new_x < 0 or new_x >= width or new_y < 0 or new_y >= height:
                game_over = True
                break

            # Check collision with self
            if (new_x, new_y) in snake_body:
                game_over = True
                break

            snake_body.insert(0, (new_x, new_y))

            # Check if food eaten
            if new_x == food_x and new_y == food_y:
                score += 1
                food_x = random.randint(0, width - 1)
                food_y = random.randint(0, height - 1)
                while (food_x, food_y) in snake_body:
                    food_x = random.randint(0, width - 1)
                    food_y = random.randint(0, height - 1)
            else:
                snake_body.pop()

            time.sleep(0.1)

    except KeyboardInterrupt:
        pass

    print("\nGame Over!")
    print(f"Final Score: {score}")

if __name__ == "__main__":
    snake()
