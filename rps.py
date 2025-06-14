import random
from collections import defaultdict

opponent_history = []
my_history = []
strategies = {
    "quincy": ["P"],  # Quincy always plays "P"
    "mirror": [],     # Tracks and mirrors your last move
    "rotate": ["R", "P", "S"],
}

score = defaultdict(int)
round_number = 0

def beat_move(move):
    return {"R": "P", "P": "S", "S": "R"}[move]

def player(prev_play, opponent_history=opponent_history):
    global round_number, my_history

    if prev_play:
        opponent_history.append(prev_play)

    round_number += 1

    if round_number <= 5:
        move = random.choice(["R", "P", "S"])
        my_history.append(move)
        return move

    # Strategy 1: Assume opponent mirrors your last move
    mirror_guess = my_history[-1] if my_history else "R"
    counter_mirror = beat_move(mirror_guess)

    # Strategy 2: Look at most common move from opponent
    freq = {"R": 0, "P": 0, "S": 0}
    for move in opponent_history:
        freq[move] += 1
    most_common = max(freq, key=freq.get)
    counter_common = beat_move(most_common)

    # Strategy 3: Use last two moves to predict next
    prediction = "R"
    seq = "".join(opponent_history[-2:])
    counts = {"R": 0, "P": 0, "S": 0}
    for i in range(len(opponent_history) - 2):
        if opponent_history[i:i+2] == list(seq):
            next_move = opponent_history[i+2]
            counts[next_move] += 1
    if sum(counts.values()) > 0:
        prediction = max(counts, key=counts.get)
    counter_seq = beat_move(prediction)

    # Choose best strategy this round (simulate scores)
    simulated_results = {
        counter_mirror: 0,
        counter_common: 0,
        counter_seq: 0,
    }

    for strat_move in simulated_results:
        if opponent_history:
            last = opponent_history[-1]
            if strat_move == beat_move(last):
                simulated_results[strat_move] += 1

    best = max(simulated_results, key=simulated_results.get)

    my_history.append(best)
    return best