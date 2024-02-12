# FileWriter.py
# notes: pre-made solution.txt is made on test/solutions/solution.txt

def rewrite_Txt(rewards, optimal_tokens, optimal_path, time_execution, message): # write solution into txt

    def rewrite_rewards(file,rewards):
        file.write(str(rewards) + '\n')
    
    def rewrite_tokens(file,optimal_tokens):
        for i, token in enumerate(optimal_tokens):
            file.write(token)
            if(i != (len(optimal_tokens) - 1)):
                file.write(' ')
        file.write('\n')
    
    def rewrite_path(file, optimal_path):
        for path in optimal_path:
            file.write(str(path)[1:-1] + '\n')
        file.write('\n')
    
    def rewrite_time(file, time_execution):
        file.write(str(int(time_execution * 1000)))
        file.write(' ms\n')
            

    filepath = input(message)
    try:
        with open(filepath, 'w') as file:
            rewrite_rewards(file,rewards)
            rewrite_tokens(file,optimal_tokens)
            rewrite_path(file,optimal_path)
            rewrite_time(file,time_execution)
        print("File successfully written")
    except FileNotFoundError:
        print("File Not Found")
        rewrite_Txt(rewards,optimal_tokens, optimal_path, time_execution, "Please Input Ulang path anda: ")