#InputReader.py

import random

def readTxtFile(): # Input From FileText
    filepath = input("Please input your txt path: ")

    with open(filepath, 'r') as file: # Read File
        buffer_size = int(file.readline().strip()) 
        _, matrix_height  = map(int, file.readline().strip().split())

        matrix = []

        for i in range(matrix_height): # Directly input whole line to matrix
            currentRow  = file.readline().strip().split()
            matrix.append(currentRow)

        number_of_sequences = int(file.readline().strip())
        sequences = []
        sequence_rewards = []
        for i in range(number_of_sequences):
            sequence = file.readline().strip().split()
            sequences.append(sequence)
            sequence_reward = int(file.readline().strip())
            sequence_rewards.append(sequence_reward)

    file.close() # Free File 
    return buffer_size, matrix, sequences, sequence_rewards

def readDirectInput(): # Input From CLI or GUI 
    def createRandomMatrix(tokens, width, height): # tokens are unique_tokens from input
        random_tokens = [random.choice(tokens) for _ in range(width * height)] # Create Random Tokens from given unique tokens to fill all the matrix cells

        matrix = [[random_tokens.pop(0) for _ in range(height)] for _ in range(width)]  # Create Random matrix from random_tokens element

        return matrix

    def createRandomSequences(tokens, number_of_sequences, max_sequence_token): 

        # assumption: max_sequence_token > 2
        sequence_reward = [random.randint(0,100) for i in range(number_of_sequences)] # assumption sequence_reward is up to me, the maker :)
        
        sequences = []
        for _ in range(number_of_sequences):
            random_amount = random.randint(2,max_sequence_token)
            random_sequence = [random.choice(tokens) for i in range(random_amount)]
            sequences.append(random_sequence)

        return sequences, sequence_reward # sequences and sequence_reward not become one to make it easier to manipulate later

    unique_token = int(input("Input Unique amount of Token: ")) # amount of unique token
    input_token = input("Input Your Token: \n") # the unique token
    tokens = input_token.strip().split()

    while(not all(len(token) == 2 for token in tokens)): # Assumption : the all the alphanumeric token has to be in format of 55 7C (length of 2)

        print("All the Token Length has to Equal to 2")
        input_token = input("Please ReInput Your Token: \n") 
        tokens = input_token.strip().split()

    while(len(set(tokens)) != unique_token): # unique token input not the same as amount of unique token previously

        print("Too many Token !!!")
        input_token = input("Please ReInput Your Token: \n") 
        tokens = input_token.strip().split()
    
    buffer_size = int(input('buffer size: '))

    matrix_size_input = input("Please input Matrix Width and Height: ")
    matrix_width, matrix_height = map(int,matrix_size_input.strip().split())

    number_of_sequences = int(input("Masukkan jumlah Sequence: "))
    max_sequence_token = int(input("Masukkan Jumlah maksimal token yang ada pada Sequence: "))

    matrix = createRandomMatrix(tokens, matrix_width, matrix_height)

    for i in range(len(matrix)): # print matrix
        print(' '.join(map(str, matrix[i])))

    sequences, sequence_reward = createRandomSequences(tokens, number_of_sequences, max_sequence_token)

    for i in range(len(sequences)):
        print(f"Sequence {i+1}: ", ' '.join(map(str, sequences[i])))
        print(f'Reward: {sequence_reward[i]}')

    return buffer_size, matrix, sequences, sequence_reward

def inputDecision(): # CLI Input Decider for user to decide between using filetext or direct input
    print("Please Choose Between these Input : ")
    print("1. Input with TextFile (txt)")
    print("2. Input From CLI\n")
    decision = int(input(""))

    while decision not in [1,2]:
        print("Input Salah !!!\n")
        print("Masukkan Input yang Valid : ")
        print("1. Input with TextFile (txt)")
        print("2. Input From CLI\n")
        decision = int(input(""))

    if(decision == 1):
        buffer_size,matrix, sequences, sequence_reward = readTxtFile()
    else:
        buffer_size,matrix, sequences, sequence_reward = readDirectInput()

    return buffer_size,matrix, sequences, sequence_reward