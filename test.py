import subprocess
import random
import os

def run_game_with_seed(seed, speed):

    os.environ['SDL_VIDEODRIVER'] = 'dummy'

    # Command to run the game with a specific seed
    command = ['python3', 'run_game.py', f'--speed', str(speed),f'--seed', str(seed)]
    
    # Run the command and capture the output
    result = subprocess.run(command, capture_output=True, text=True)
    
    # Print the terminal output
    print("SEED: " + str(seed))
    print(result.stdout)
    print(result.stderr)

def main():
    speed = 100000
    # Run the game 10 times with random seeds
    for _ in range(10):
        random_seed = random.randint(1, 10000)  # Generate a random seed
        run_game_with_seed(random_seed, speed)

if __name__ == "__main__":
    main()
