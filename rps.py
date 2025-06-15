def player(prev_play, opponent_history=[]):
    import random

    if not hasattr(player, "initialized"):
        player.my_history = []
        player.opponent_history = []
        player.counter = 0
        player.detected_bot = None
        player.initialized = True

    # Record moves
    if prev_play:
        player.opponent_history.append(prev_play)

    # Detect bot in first few moves (bot fingerprinting)
    def detect_bot():
        if len(player.opponent_history) < 20:
            return None

        pattern = ''.join(player.opponent_history[:10])
        unique_counts = len(set(player.opponent_history))

        if player.opponent_history[:10] == ['R', 'R', 'P', 'P', 'S'] * 2:
            return 'quincy'
        elif unique_counts <= 2:
            return 'mrugesh'
        elif all(player.opponent_history[i] == counter_move(player.my_history[i-1]) for i in range(1, len(player.my_history))):
            return 'kris'
        elif len(player.opponent_history) > 2:
            return 'abbey'
        return None

    def counter_move(move):
        return {'R': 'P', 'P': 'S', 'S': 'R'}.get(move, random.choice(['R', 'P', 'S']))

    # Strategies for specific bots
    def vs_quincy():
        # Hard-coded counter to quincy's pattern
        cycle = ['R', 'R', 'P', 'P', 'S']
        idx = len(player.opponent_history) % 5
        next_move = cycle[idx]
        return counter_move(next_move)

    def vs_mrugesh():
        # Counter what Mrugesh predicts: your most frequent move
        my_freq = {'R': 0, 'P': 0, 'S': 0}
        for m in player.my_history:
            my_freq[m] += 1
        if not any(my_freq.values()):
            return random.choice(['R', 'P', 'S'])
        my_most = max(my_freq, key=my_freq.get)
        return counter_move(counter_move(my_most))

    def vs_kris():
        # Kris always counters your last move => play what counters their counter
        if not player.my_history:
            return random.choice(['R', 'P', 'S'])
        last = player.my_history[-1]
        predicted = counter_move(last)
        return counter_move(predicted)

    def vs_abbey():
        # Abbey uses your last two moves to predict your next
        if len(player.my_history) < 2:
            return random.choice(['R', 'P', 'S'])

        last_two = ''.join(player.my_history[-2:])
        freq = {'R': 0, 'P': 0, 'S': 0}

        # Build frequency of what YOU played after YOUR last_two
        for i in range(len(player.my_history) - 2):
            if ''.join(player.my_history[i:i+2]) == last_two:
                next_move = player.my_history[i+2]
                freq[next_move] += 1

        # Abbey will predict your most likely next move
        if sum(freq.values()) == 0:
            predicted = random.choice(['R', 'P', 'S'])
        else:
            predicted = max(freq, key=freq.get)

        # Abbey will counter your predicted move => you counter Abbey's counter
        return counter_move(counter_move(predicted))


    # Detect bot if not yet known
    if player.detected_bot is None:
        player.detected_bot = detect_bot()

    # Apply tailored strategy if bot detected
    if player.detected_bot == 'quincy':
        move = vs_quincy()
    elif player.detected_bot == 'mrugesh':
        move = vs_mrugesh()
    elif player.detected_bot == 'kris':
        move = vs_kris()
    elif player.detected_bot == 'abbey':
        move = vs_abbey()
    else:
        # Early game: play random until bot is detected
        move = random.choice(['R', 'P', 'S'])

    player.my_history.append(move)
    return move
