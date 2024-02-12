# main.py
import InputReader
import CombinationGenerator
import FileWriter

buffer_size,matrix, sequences, sequence_reward = InputReader.inputDecision()



next_token = CombinationGenerator.get_all_possible_next_tokens(sequences)

combination_token, reward, timer, coordinate = CombinationGenerator.start_calculation(matrix,buffer_size, next_token, sequences, sequence_reward)

print("\nTotal Rewards:",str(reward))

print(' '.join(map(str,combination_token)))

for path in coordinate:
    print(str(path)[1:-1])


print(timer * 1000, 'ms\n')

choices = ['y','n']
print("Apakah anda ingin menyimpan solusi? (y/n)")
choice = input().lower()

while(choice not in choices):
    print("Masukkan Input yang benar (y/n)")
    choice = input().lower()

if(choice == 'y'):
    FileWriter.rewrite_Txt(reward, combination_token, coordinate, timer, "Masukkan Path txt untuk menyimpan solusi anda: ")
else:
    print("Nice Hacks !!!!")

