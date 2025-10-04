for i in {1..10}; do
    # Generate a random seed
    SEED=$((RANDOM))
    
    # Run the game with the random seed using Xvfb to avoid GUI
    python3 run_game.py --speed 100000 --seed $SEED
done