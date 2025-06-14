def player(prev_play, opponent_history=[]):
    """
    Rock Paper Scissors player that adapts to opponent patterns.
    Uses multiple strategies to beat different types of bots.
    """
    import random
    from collections import Counter, defaultdict
    
    # Initialize history on first call
    if not hasattr(player, 'initialized'):
        opponent_history.clear()
        player.initialized = True
        player.my_history = []
        player.pattern_memory = defaultdict(lambda: defaultdict(int))
        player.sequence_memory = defaultdict(lambda: defaultdict(int))
        player.frequency_memory = defaultdict(int)
        player.anti_frequency_memory = defaultdict(int)
    
    # Add previous play to history
    if prev_play:
        opponent_history.append(prev_play)
        
        # Update pattern memories
        if len(player.my_history) > 0:
            my_last = player.my_history[-1]
            player.pattern_memory[my_last][prev_play] += 1
        
        # Update frequency tracking
        player.frequency_memory[prev_play] += 1
        
        # Update sequence memory for patterns
        if len(opponent_history) >= 2:
            last_two = ''.join(opponent_history[-2:])
            if len(opponent_history) >= 3:
                player.sequence_memory[last_two][opponent_history[-1]] += 1
    
    # Strategy functions
    def counter_move(move):
        """Return the move that beats the given move"""
        if move == 'R': return 'P'
        elif move == 'P': return 'S'
        elif move == 'S': return 'R'
        return random.choice(['R', 'P', 'S'])
    
    def get_most_frequent():
        """Counter the most frequent opponent move"""
        if not opponent_history:
            return random.choice(['R', 'P', 'S'])
        most_common = max(player.frequency_memory.items(), key=lambda x: x[1])
        return counter_move(most_common[0])
    
    def get_pattern_prediction():
        """Predict based on response to my last move"""
        if not player.my_history or not opponent_history:
            return random.choice(['R', 'P', 'S'])
        
        my_last = player.my_history[-1]
        if my_last in player.pattern_memory and player.pattern_memory[my_last]:
            predicted = max(player.pattern_memory[my_last].items(), key=lambda x: x[1])
            return counter_move(predicted[0])
        return random.choice(['R', 'P', 'S'])
    
    def get_sequence_prediction():
        """Predict based on last sequence pattern"""
        if len(opponent_history) < 2:
            return random.choice(['R', 'P', 'S'])
        
        last_two = ''.join(opponent_history[-2:])
        if last_two in player.sequence_memory and player.sequence_memory[last_two]:
            predicted = max(player.sequence_memory[last_two].items(), key=lambda x: x[1])
            return counter_move(predicted[0])
        return random.choice(['R', 'P', 'S'])
    
    def get_anti_frequency():
        """Counter anti-frequency strategy (opponent counters our most frequent)"""
        if not player.my_history:
            return random.choice(['R', 'P', 'S'])
        
        my_counter = Counter(player.my_history)
        if my_counter:
            my_most_frequent = my_counter.most_common(1)[0][0]
            # If opponent counters our most frequent, we should counter their counter
            opponent_likely_counter = counter_move(my_most_frequent)
            return counter_move(opponent_likely_counter)
        return random.choice(['R', 'P', 'S'])
    
    def get_rotation_prediction():
        """Detect if opponent is rotating through moves"""
        if len(opponent_history) < 6:
            return random.choice(['R', 'P', 'S'])
        
        # Check for simple rotation patterns
        last_6 = opponent_history[-6:]
        if last_6 == ['R', 'P', 'S'] * 2 or last_6 == ['R', 'S', 'P'] * 2:
            # Predict next in rotation
            if opponent_history[-1] == 'R':
                if last_6[1] == 'P':
                    return counter_move('P')
                else:
                    return counter_move('S')
            elif opponent_history[-1] == 'P':
                if 'R' in last_6[last_6.index('P')+1:last_6.index('P')+2]:
                    return counter_move('S')
                else:
                    return counter_move('R')
            else:  # S
                if 'P' in last_6[last_6.index('S')+1:last_6.index('S')+2] if last_6.index('S') < 5 else []:
                    return counter_move('R')
                else:
                    return counter_move('P')
        
        return random.choice(['R', 'P', 'S'])
    
    def get_mirror_strategy():
        """Mirror or anti-mirror the opponent"""
        if not opponent_history:
            return random.choice(['R', 'P', 'S'])
        
        # Try anti-mirror (opposite of last move)
        last_move = opponent_history[-1]
        if last_move == 'R':
            return 'S'
        elif last_move == 'P':
            return 'R'
        else:
            return 'P'
    
    # Strategy selection based on game progress and patterns
    if len(opponent_history) < 10:
        # Early game: try different approaches
        strategies = [get_most_frequent, get_pattern_prediction, get_anti_frequency]
        my_move = random.choice(strategies)()
    elif len(opponent_history) < 50:
        # Mid game: focus on pattern detection
        strategies = [get_sequence_prediction, get_pattern_prediction, get_rotation_prediction]
        weights = [3, 2, 1]
        strategy = random.choices(strategies, weights=weights)[0]
        my_move = strategy()
    else:
        # Late game: use best performing strategies
        strategies = [
            get_sequence_prediction,
            get_pattern_prediction, 
            get_most_frequent,
            get_anti_frequency,
            get_mirror_strategy
        ]
        
        # Weight strategies based on recent performance
        if len(opponent_history) > 20:
            # Analyze last 20 moves to see what's working
            recent_opponent = opponent_history[-20:]
            recent_mine = player.my_history[-20:] if len(player.my_history) >= 20 else player.my_history
            
            # Simple heuristic: if opponent is very predictable, use sequence prediction more
            recent_counter = Counter(recent_opponent)
            if recent_counter and recent_counter.most_common(1)[0][1] > 12:  # >60% same move
                my_move = get_most_frequent()
            else:
                # Use weighted random selection of strategies
                weights = [4, 3, 2, 2, 1]  # Favor sequence and pattern prediction
                strategy = random.choices(strategies, weights=weights)[0]
                my_move = strategy()
        else:
            weights = [3, 2, 2, 1, 1]
            strategy = random.choices(strategies, weights=weights)[0]
            my_move = strategy()
    
    # Add some randomness to avoid being too predictable
    if random.random() < 0.05:  # 5% random moves
        my_move = random.choice(['R', 'P', 'S'])
    
    # Record our move
    player.my_history.append(my_move)
    
    return my_move