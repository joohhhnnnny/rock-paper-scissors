import random

# Store previous moves
opponent_history = []

def player(prev_play, opponent_history=opponent_history):
    # Update opponent's history
    if prev_play:
        opponent_history.append(prev_play)

    # Not enough data to predict yet — play random
    if len(opponent_history) < 5:
        return random.choice(["R", "P", "S"])

    # Count 3-character sequences to find the most common pattern
    sequence_counts = {}
    for i in range(len(opponent_history) - 2):
        seq = "".join(opponent_history[i:i+3])
        if seq in sequence_counts:
            sequence_counts[seq] += 1
        else:
            sequence_counts[seq] = 1

    # Predict next move based on last 2 opponent moves
    last_two = "".join(opponent_history[-2:])
    prediction = "R"  # default prediction
    max_count = 0

    for move in ["R", "P", "S"]:
        seq = last_two + move
        if sequence_counts.get(seq, 0) > max_count:
            max_count = sequence_counts[seq]
            prediction = move

    # Counter the predicted move
    counters = {"R": "P", "P": "S", "S": "R"}
    return counters[prediction]
