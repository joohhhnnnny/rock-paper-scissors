import random

# In player() function
def player(prev_play):
    if len(my_history) < 5:
        move = random.choice(["R", "P", "S"])
        my_history.append(move)
        if prev_play:
            opponent_history.append(prev_play)
        return move

# Histories
opponent_history = []
my_history = []

# Define counter function
def counter(move):
    return {"R": "P", "P": "S", "S": "R"}[move]

# --- Strategies ---
def always_rock():
    return "R"

def frequency_strategy():
    if not opponent_history:
        return random.choice(["R", "P", "S"])
    most_common = max(set(opponent_history), key=opponent_history.count)
    return counter(most_common)

def rotate_strategy():
    if not opponent_history:
        return random.choice(["R", "P", "S"])
    last = opponent_history[-1]
    return counter(counter(last))  # Predicts counter of their last

def markov_strategy():
    if len(opponent_history) < 3:
        return random.choice(["R", "P", "S"])
    last_two = "".join(opponent_history[-2:])
    counts = {"R": 0, "P": 0, "S": 0}
    for i in range(len(opponent_history) - 2):
        if "".join(opponent_history[i:i+2]) == last_two:
            next_move = opponent_history[i+2]
            counts[next_move] += 1
    prediction = max(counts, key=counts.get, default=random.choice(["R", "P", "S"]))
    return counter(prediction)

# --- Combine strategies ---
strategies = [
    always_rock,
    frequency_strategy,
    rotate_strategy,
    markov_strategy
]
strategy_scores = [0 for _ in strategies]  # Initialize score for each

# --- Player Function ---
def player(prev_play):
    if prev_play:
        opponent_history.append(prev_play)

        if my_history:
            last_my_move = my_history[-1]
            for i, strat in enumerate(strategies):
                predicted = strat()
                expected = counter(prev_play)
                if predicted == expected:
                    strategy_scores[i] += 1

    # Pick strategy with best score
    best_strategy_index = strategy_scores.index(max(strategy_scores))
    move = strategies[best_strategy_index]()
    my_history.append(move)
    return move