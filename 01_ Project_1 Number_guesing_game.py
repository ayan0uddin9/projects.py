# import random

# print(" Welcome to Number Guessing Game!")
# number_to_guess = random.randint(1, 100)
# guess = None

# while guess != number_to_guess:
#     guess = int(input("Enter your guess (1-100): "))
    
#     if guess < number_to_guess:
#         print("Too low! Try again.")
#     elif guess > number_to_guess:
#         print("Too high! Try again.")
#     else:
#         print(" Correct! You guessed the number!")

# Inhanced version
# Features added: difficulty levels, attempt counter, and replay option.
import random

def play_game():
    print("\n🎯 Welcome to Number Guessing Game!")

    difficulty = input("Choose difficulty (easy/medium/hard): ").lower()
    if difficulty == "easy":
        max_number = 50
    elif difficulty == "hard":
        max_number = 200
    else:
        max_number = 100

    number_to_guess = random.randint(1, max_number)
    attempts = 0

    while True:
        try:
            guess = int(input(f"Enter your guess (1-{max_number}): "))
            attempts += 1
        except ValueError:
            print("⚠ Please enter a valid number.")
            continue
        
        if guess < number_to_guess:
            print("Too low! 📉")
        elif guess > number_to_guess:
            print("Too high! 📈")
        else:
            print(f"🎉 Correct! You guessed it in {attempts} tries!")
            break

while True:
    play_game()
    again = input("Play again? (y/n): ").lower()
    if again != "y":
        print("Thanks for playing! 👋")
        break






