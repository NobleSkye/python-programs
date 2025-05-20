import random
import os

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def number_guess():
    number = random.randint(1, 100)
    attempts = 0
    max_attempts = 10

    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")
    print(f"You have {max_attempts} attempts to guess it.\n")

    while attempts < max_attempts:
        try:
            guess = int(input(f"Attempt {attempts + 1}/{max_attempts}. Enter your guess: "))
            attempts += 1

            if guess < 1 or guess > 100:
                print("Please enter a number between 1 and 100.")
                continue

            if guess < number:
                print("Too low!")
            elif guess > number:
                print("Too high!")
            else:
                print(f"\nCongratulations! You guessed it in {attempts} attempts!")
                return

            if attempts < max_attempts:
                print(f"You have {max_attempts - attempts} attempts left.\n")
            
        except ValueError:
            print("Please enter a valid number.")

    print(f"\nGame Over! The number was {number}.")

if __name__ == "__main__":
    number_guess()
