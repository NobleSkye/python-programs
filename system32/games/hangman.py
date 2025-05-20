import random
import os

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def hangman():
    words = ["python", "programming", "computer", "algorithm", "database", "network", "software", "developer"]
    word = random.choice(words)
    word_letters = set(word)
    alphabet = set('abcdefghijklmnopqrstuvwxyz')
    used_letters = set()
    lives = 6

    # Hangman ASCII art states
    hangman_states = ['''
      +---+
      |   |
          |
          |
          |
          |
    =========''', '''
      +---+
      |   |
      O   |
          |
          |
          |
    =========''', '''
      +---+
      |   |
      O   |
      |   |
          |
          |
    =========''', '''
      +---+
      |   |
      O   |
     /|   |
          |
          |
    =========''', '''
      +---+
      |   |
      O   |
     /|\\  |
          |
          |
    =========''', '''
      +---+
      |   |
      O   |
     /|\\  |
     /    |
          |
    =========''', '''
      +---+
      |   |
      O   |
     /|\\  |
     / \\  |
          |
    =========''']

    print("Welcome to Hangman!")
    print("Guess the word by entering one letter at a time.")

    while len(word_letters) > 0 and lives > 0:
        clear()
        print(hangman_states[6 - lives])
        print('You have', lives, 'lives left.')
        print('Used letters:', ' '.join(used_letters))

        # Show current word state
        word_list = [letter if letter in used_letters else '_' for letter in word]
        print('Current word:', ' '.join(word_list))

        # Get user input
        user_letter = input('Guess a letter: ').lower()
        if user_letter in alphabet - used_letters:
            used_letters.add(user_letter)
            if user_letter in word_letters:
                word_letters.remove(user_letter)
            else:
                lives = lives - 1
                print('\nYour letter,', user_letter, 'is not in the word.')
        
        elif user_letter in used_letters:
            print('\nYou have already used that letter. Please try again.')
        
        else:
            print('\nThat is not a valid letter.')

    clear()
    print(hangman_states[6 - lives])
    if lives == 0:
        print('Sorry, you died. The word was', word)
    else:
        print('Congratulations! You guessed the word', word, '!!')

if __name__ == "__main__":
    hangman()
