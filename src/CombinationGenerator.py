#CombinationGenerator.py

import time

def get_all_possible_next_tokens(sequences):
    # return a dictionary that exist of unique token as its key and the possible next_token of the unique token as the value

    def find_all_next_token(sequences, token): # find all next possible token of current token (only one token)
        next_token = []

        def idx_decider(sequence, idx):
            if(idx == (len(sequence)-1) and sequence[0] not in next_token):
                next_token.append(sequence[0])
            elif(idx < (len(sequence) -1) and sequence[idx+1] not in next_token):
                next_token.append(sequence[idx + 1])

        for sequence in sequences:
            for i, curr_token in enumerate(sequence):
                if(curr_token == token):
                    idx_decider(sequence,i)
        return next_token

    def get_all_unique_token(sequences):
        unique_token = []
        for sequence in sequences:
            for token in sequence:
                if(token not in unique_token):
                    unique_token.append(token)
        return unique_token

    all_possible_next_tokens = {}
    unique_tokens = get_all_unique_token(sequences)
    for token in unique_tokens:
        next_tokens = find_all_next_token(sequences, token)
        all_possible_next_tokens[token] = next_tokens
    return all_possible_next_tokens

def find_next_token_inpath(isVertical, row, col, matrix, next_token): # Find any possible next token in a path of certain coordinates
    # notes: next_token are used for the dictionary of all the possible next token (from get_all_possible_next_token function)

    next_possible_token = []
    dataIdx = [] # used to get all the possible next token index

    if(isVertical):
        for i in range(len(matrix)):
            if(matrix[i][col] in next_token and (i != row)):
                next_possible_token.append(matrix[i][col])
                dataIdx.append((i,col)) 
    else:
        for i in range(len(matrix[row])):
            if(matrix[row][i] in next_token and (i != col)):
                next_possible_token.append(matrix[row][i])
                dataIdx.append((row, i))

    return next_possible_token, dataIdx

def generate_combinations(matrix, buffer_size, current_path, current_token, isVertical, next_token_dictionary): # recursive helper to get all the combination 

    # base
    combinations, combination_token = [], []
    if len(current_path) == buffer_size:
        return [current_path], [current_token] 
         
    # recursion

    # get all possible next token and index in the current path
    next_possible_tokens, next_tokens_idx = find_next_token_inpath(isVertical, int(current_path[-1][0]), int(current_path[-1][1]), matrix, next_token_dictionary)

    # iterate over all the possible token
    for idx, next_token in enumerate(next_possible_tokens):

        next_path = current_path + [next_tokens_idx[idx]]
        next_token_incantination = current_token + [next_token]

        new_combinations , new_token_combinations = generate_combinations(matrix,buffer_size, next_path, next_token_incantination, not isVertical, next_token_dictionary)

        combinations.extend(new_combinations)
        combination_token.extend(new_token_combinations)

    return combinations, combination_token
        
    # main function to get all the combination
def start_calculation(matrix, buffer_size, next_token_dictionary, sequences, sequence_reward):
    startTimer = time.time() # start timer

    all_coordinate_combinations = []
    all_token_combination = []

    # iterate over first row
    # notes : path are saved in a format (row, col) inside a list
    for col,token in enumerate(matrix[0]):
        coordinates, combinations_token = generate_combinations(matrix, buffer_size,[(0,col)], [token], True, next_token_dictionary)
        all_coordinate_combinations.extend(coordinates)
        all_token_combination.extend(combinations_token)
    
    # get the highest reward combination of tokens
    # get the max_reward and its coordinate info
    best_combination, max_reward, coordinate = find_best_combination(all_token_combination, sequences, sequence_reward, all_coordinate_combinations)

    endtime = time.time()

    timer = endtime - startTimer # time counter
    coordinate = set_coordinate_data(coordinate) # fix coordinate format into col, row with increment on both side
    
    return best_combination, max_reward, timer, coordinate

    # get the highest token combination
def find_best_combination(combination_token, sequences, sequence_rewards, coordinate):
   
    max_reward = 0
    best_combination = []
    best_coordinate = []
    
    for i, combination in enumerate(combination_token):

        # check the reward of current token combination
        current_rewards = check_sequence_reward(combination,sequences,sequence_rewards)

        if(current_rewards > max_reward):
            max_reward = current_rewards
            best_combination = combination
            best_coordinate = coordinate[i]

    return best_combination, max_reward, best_coordinate

    # fix coordinate format into (col + 1, row + 1)
def set_coordinate_data(best_coordinate):
    for i in range(len(best_coordinate)):
        x, y = best_coordinate[i]
        x += 1
        y += 1
        best_coordinate[i] = (y,x)
    return best_coordinate
    
    # get total_reward of current token combination
def check_sequence_reward(combination, sequences, sequence_rewards):
    total_reward = 0
    sequence_check = []
    for sequence, reward in zip(sequences, sequence_rewards):
        sequence_length = len(sequence)
        for i in range(len(combination) - sequence_length + 1):

            # check for current combination element from i till i + current sequence length, then match it to current sequence
            # also check for no sequence used twice
            if combination[i:i+sequence_length] == sequence and (sequence not in sequence_check):
                total_reward += reward
                sequence_check.append(sequence)
                
    return total_reward