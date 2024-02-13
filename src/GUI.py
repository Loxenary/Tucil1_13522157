import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import CombinationGenerator
import InputReader

window = tk.Tk()

def toggle_fullscreen(event = None):
    window.attributes("-fullscreen", not window.attributes("-fullscreen"))

def open_txt_file(filepath):
    if(not filepath):
        raise_error("Input your txt file First!!!")

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

    file.close()
    return buffer_size, matrix, sequences, sequence_rewards

def raise_good_job(message):
    messagebox.showinfo(message)

def open_file():
    global filename

    file_path = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[("Text files", "*.txt")])

    if file_path:
        filename.set(file_path)

def raise_error(message):
    messagebox.showerror("Error: ", message)

def bg_color(color):
    window.configure(bg=color)

def update_selection():
    selection = slider.get()
    global isDirectInput
    color_1 = '#7E7E7E'
    color_2 = 'red' 
    if selection == 0:
        slider.configure(troughcolor=color_1)
        label_color.config(foreground=color_2)
        label_texture.config(foreground=color_2)        
    else:
        slider.configure(troughcolor=color_2)
        label_color.config(foreground=color_1)
        label_texture.config(foreground=color_1)


def update_gui(event):
    print("test")
    window.update()

def get_color(color_name):
    return color_data.get(color_name)

def display_matrix(matrix):
    if(not matrix):
        return ""
    matrix_str = ""
    for row in matrix:
        row_str = " ".join(map(str,row)) + "\n"
        matrix_str += row_str
    return matrix_str

def display_sequence(sequences, sequence_reward):
    if(not sequences or not sequence_reward):
        return ""
    sequences_str = ""
    for i, item in enumerate(sequences):
        sequence_str = f"Sequence {i+1}: {' '.join(map(str,item))}\n"
        sequence_str += f"Reward {i+1}: {sequence_reward[i]}\n\n"
        sequences_str += sequence_str
    return sequences_str

window.geometry("1000x800")


def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

def validate_input(action, value_if_allowed) :
    if action == '1':
        if value_if_allowed.isdigit() and int(value_if_allowed) <= 10 and int(value_if_allowed) > 0:
            return True
        else:
            return False
    else:
        return True

def get_buffer():
    buffer_value = buffer_entry.get()
    return buffer_value

def get_unique_token():
    tokens = Unique_token_entry.get().split()
    valid_tokens = all(len(token) == 2 for token in tokens)
    if valid_tokens:
        return tokens
    else:
        raise_error("All token's Lenght have to be 2 !!!")

def get_max_sequence_token():
    return max_sequence_token_entry.get()

def get_max_num_sequence():
    return Max_Sequence_entry.get()

def get_col_and_row_matrix():
    return int(Matrix_Col_entry.get()), int(Matrix_Row_entry.get())

def get_all_data():
    buffer = int(get_buffer())
    unique_token = get_unique_token()
    max_sequence_token = int(get_max_sequence_token())
    max_sequence_number = int(get_max_num_sequence())
    col, row = get_col_and_row_matrix()
    if(buffer and unique_token and max_sequence_token and max_sequence_number and col and row):
        return buffer, unique_token, max_sequence_token, max_sequence_number, col, row
    else:
        raise_error("Please Fill all the Input Correctly !!!")

def generate_random_matrix():
    global global_matrix

    global_matrix = get_random_matrix()
    
    save_and_display_matrix(global_matrix)

def generate_random_sequence():
    global random_sequence, random_reward_seqeunce

    random_sequence, random_reward_seqeunce = get_random_sequences()

    save_and_display_sequences(random_sequence, random_reward_seqeunce)

def save_and_display_matrix(global_matrix):
    matrix_str = display_matrix(global_matrix)
    Matrix_widget.config(state="normal")
    Matrix_widget.delete("1.0", tk.END) 
    Matrix_widget.insert("1.0", matrix_str)
    Matrix_widget.config(state="disabled")

def save_and_display_sequences(random_sequences, sequence_reward):
    sequence_str = display_sequence(random_sequences, sequence_reward)
    Sequence_widget.config(state="normal")
    Sequence_widget.delete("1.0", tk.END)
    Sequence_widget.insert("1.0", sequence_str)
    Sequence_widget.config(state="disabled")

def get_random_matrix():
    _, unique_token, _, _, col, row = get_all_data()

    return InputReader.createRandomMatrix(unique_token, col, row)

def get_random_sequences():
    _, unique_token, max_sequence_token, max_sequence_number, _, _= get_all_data()

    return InputReader.createRandomSequences(unique_token, max_sequence_number, max_sequence_token)

def get_output_data(reward, combination_token, coordinate, timer):
    if(not reward or not combination_token or not coordinate or not timer):
        return
    output_str = "\nTotal Rewards" + str(reward) + "\n"
    output_str += " ".join(map(str,combination_token)) + "\n"
    for path in coordinate:
        output_str += (str(path)[1:-1] + '\n')
    output_str += str(int(timer * 1000)) + 'ms\n'
    return output_str

def update_output(output_text):
    Output_widget.config(state="normal")
    
    Output_widget.delete("1.0", "end")  
    Output_widget.insert("1.0", output_text)  
    Output_widget.config(state="disabled")



def calculation(slider):
    global global_matrix, random_sequence, random_reward_seqeunce
    if(slider.get() == 0):
        buffer_size, global_matrix, random_sequence,random_reward_seqeunce = open_txt_file(filename.get())
        save_and_display_matrix(global_matrix)
        save_and_display_sequences(random_sequence, random_reward_seqeunce)
    else:
        
        if global_matrix is None:
            generate_random_matrix()
        if random_sequence is None:
            generate_random_sequence()
        
        buffer_size, _, _, _, _, _= get_all_data()
        
    next_token = CombinationGenerator.get_all_possible_next_tokens(random_sequence)

    combination_token, reward, timer, coordinate = CombinationGenerator.start_calculation(global_matrix ,buffer_size, next_token, random_sequence, random_reward_seqeunce)

    global tokens, rewards, times, paths

    tokens = combination_token
    rewards = reward
    times = timer
    paths = coordinate

    output_Str = get_output_data(reward, combination_token, coordinate, timer)
    update_output(output_Str)

def save_solutions():
    if (not rewards and not tokens and not paths and not times):
        return

    file_path = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[("Text files", "*.txt")])

    if not file_path:
        return
    
    with open(file_path, 'w') as file:
        rewrite_rewards(file,rewards)
        rewrite_tokens(file,tokens)
        rewrite_path(file,paths)
        rewrite_time(file,times)
    file.close()
    raise_good_job("File save Successfully")

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

color_data = {
    'Cream_1' : '#D9D9D9'
}


# Canvas
canvas = tk.Canvas(window)
canvas.pack(side="left", fill="both", expand=True)

# Scrollbar
scrollbar = ttk.Scrollbar(window, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.place(relx = 1, rely = 0, relheight= 1, anchor='ne')

# Frame
frame = ttk.Frame(canvas)

canvas.create_window((0, 0), window=frame, anchor="nw")

frame.bind("<Configure>", on_configure)

# mouse scroll down and up
canvas.bind('<MouseWheel>', lambda event: canvas.yview_scroll(-int(event.delta / 60), "units"))

# scroll bar horizontal
scrollbar_bottom = ttk.Scrollbar(window, orient='horizontal', command=canvas.xview)
canvas.configure(xscrollcommand= scrollbar_bottom.set)
scrollbar_bottom.place(relx = 0, rely = 1, relwidth=  1, anchor= 'sw')

# ctrl + mouse scroll
canvas.bind('<Control MouseWheel>', lambda event: canvas.xview_scroll(-int(event.delta / 60), "units"))


# full screen button
fullscreen_button = tk.Button(frame, text="Fullscreen",padx=5,pady=5, command=toggle_fullscreen)

fullscreen_button.place(relx=1.0, rely=0, anchor='ne')

window.bind("<F12>", toggle_fullscreen)
window.bind("<Escape>", toggle_fullscreen)

# title

title = ttk.Label(master=frame, text="Cyberpunk 2077 Breach Protocol", font="Calibri 20", padding= (10,10,10,10))
title.pack()

# line after text

first_canvas = tk.Canvas(frame, width=window.winfo_screenwidth(), height= 30)
first_canvas.pack(fill=tk.Y, expand=False)
first_line = first_canvas.create_line(0,30,window.winfo_screenwidth(),30, width=4)


# main container
main_direct_input_container = ttk.Frame(frame)


# SLIDER
slider_container = ttk.Frame(master=frame)
label_color = tk.Label(slider_container, text="Txt Input", font="Calibri 16", width=10)

slider = tk.Scale(slider_container, from_=0, to=1, orient="horizontal", length=70, sliderlength=20, showvalue=False, width=20)

label_texture = tk.Label(slider_container, text="Direct Input", font="Calibri 16", width=10)



# PACKERS
label_color.grid(row=0, column=0)
slider.grid(row=0, column=1)
label_texture.grid(row=0, column=2)

slider_container.pack(pady=(10, 20))
slider.bind("<ButtonRelease-1>", lambda event: update_selection())

slider.set(0)
update_selection()


# Second Container
second_container = ttk.Frame(main_direct_input_container)


#global variable
global_matrix = None
random_sequence = None
buffer_size = None
random_reward_seqeunce = None
rewards, tokens, paths, times = None, None, None, None
isDirectInput = False


# validator            
validate_number = window.register(validate_input)

# Input TXT

input_container = ttk.Frame(second_container)
filename = tk.StringVar(value="No File Chosen")

input_text = ttk.Label(input_container, text="Input File")
file_chooser = tk.Button(input_container, text="Input txt", command=lambda: open_file(), width=15, height=2)

file_path_text = ttk.Label(input_container, text="No File Choosen", textvariable=filename)

input_text.grid(row=0, column=0, sticky='w', pady=(0, 1))
file_chooser.grid(row=1, column=0, sticky='w')
file_path_text.grid(row=2, column=0, sticky='w', columnspan=2)

input_container.grid(row=0,column=1, padx=40)


# Buffer_Input
buffer_background = tk.Label(second_container,bg="#7C7C7C", height=15)
buffer_background.grid(row = 0, column = 0, sticky='w')
buffer_text = tk.Label(buffer_background, text="Entry Buffer: ",bg="#7E7E7E", font="Calibri 12", width=25, foreground='white', anchor='w')
buffer_text.grid(row=0, column=0, sticky='w')
buffer_entry = tk.Entry(buffer_background, width=7, font="Calibri 12", validate="key", validatecommand=(validate_number, '%d', '%P'))
buffer_entry.grid(pady=5, padx=5, row=1, column=0, sticky='w')


# Unique Token
Unique_token_background = tk.Label(second_container,bg="#7C7C7C", height=15)
Unique_token_background.grid(row = 1, column = 0, sticky='w', pady=(20,20))
Unique_token_text = tk.Label(Unique_token_background, text="Entry Unique token: ",bg="#7E7E7E", font="Calibri 12", width=25, foreground='white', anchor='w')
Unique_token_text.grid(row=0, column=0, sticky='w')
Unique_token_entry = tk.Entry(Unique_token_background, width=25, font="Calibri 12")
Unique_token_entry.grid(pady=5, padx=5, row=1, column=0, sticky='w')


# third container
third_container = ttk.Frame(main_direct_input_container)

# Max Unique Sequence Token
max_sequence_token_background = tk.Label(third_container,bg="#7C7C7C", height=15)
max_sequence_token_background.grid(row = 0, column = 0, sticky='w', pady=(10,20))
max_sequence_token_text = tk.Label(max_sequence_token_background, text="Entry Max Token in Sequences: ",bg="#7E7E7E", font="Calibri 12", width=25, foreground='white', anchor='w')
max_sequence_token_text.grid(row=0, column=0, sticky='w')
max_sequence_token_entry = tk.Entry(max_sequence_token_background, width=7, font="Calibri 12", validate='key', validatecommand=(validate_number,'%d','%P'))
max_sequence_token_entry.grid(pady=5, padx=5, row=1, column=0, sticky='w')


# Max Sequence
Max_Sequence_background = tk.Label(third_container,bg="#7C7C7C", height=15)
Max_Sequence_background.grid(row = 0, column = 1, sticky='w', padx=20, pady=(10,20))
Max_Sequence_text = tk.Label(Max_Sequence_background, text="Entry Max Amount Of Sequence: ",bg="#7E7E7E", font="Calibri 12", width=25, foreground='white', anchor='w')
Max_Sequence_text.grid(row=0, column=0, sticky='w')
Max_Sequence_entry = tk.Entry(Max_Sequence_background, width=7, font="Calibri 12", validate='key', validatecommand=(validate_number,'%d','%P'))
Max_Sequence_entry.grid(pady=5, padx=5, row=1, column=0, sticky='w')


fourth_container = tk.Frame(main_direct_input_container)
# Matrix Col
Matrix_Col_background = tk.Label(fourth_container,bg="#7C7C7C", height=15)
Matrix_Col_background.grid(row = 0, column = 0, sticky='w', pady=(10,20))
Matrix_Col_text = tk.Label(Matrix_Col_background, text="Matrix Col: ",bg="#7E7E7E", font="Calibri 12", width=25, foreground='white', anchor='w')
Matrix_Col_text.grid(row=0, column=0, sticky='w')
Matrix_Col_entry = tk.Entry(Matrix_Col_background, width=7, font="Calibri 12",validate='key', validatecommand=(validate_number,'%d','%P'))
Matrix_Col_entry.grid(pady=5, padx=5, row=1, column=0, sticky='w')

# Matrix Row

Matrix_Row_background = tk.Label(fourth_container,bg="#7C7C7C", height=15)
Matrix_Row_background.grid(row = 0, column = 1, sticky='w', pady=(10,20), padx=20)
Matrix_Row_text = tk.Label(Matrix_Row_background, text="Matrix Row: ",bg="#7E7E7E", font="Calibri 12", width=25, foreground='white', anchor='w')
Matrix_Row_text.grid(row=0, column=0, sticky='w')
Matrix_Row_entry = tk.Entry(Matrix_Row_background, width=7, font="Calibri 12",validate='key', validatecommand=(validate_number,'%d','%P'))
Matrix_Row_entry.grid(pady=5, padx=5, row=1, column=0, sticky='w')

# Calculate Button
Calculate_Button = tk.Button(frame, height=5, width=20, command=lambda: calculation(slider), text="Calculate Button")

#---------------- Middle Input  ----------------#
# show matrix, and sequences


Fifth_Container = ttk.Frame(frame)

# show matrix 
matrix_str = display_matrix(global_matrix)
Matrix_Container = ttk.Frame(Fifth_Container)
Matrix_label = tk.Label(Matrix_Container, text="Generated Matrix: ", font=('Courier', 16))
Matrix_widget = tk.Text(Matrix_Container, width=30, height=15, bg="#EFEFEF", fg="black", font=("Courier", 10))



# Matrix configuration
Matrix_widget.config(state="normal")
Matrix_widget.insert("1.0", matrix_str)
Matrix_widget.config(state="disabled")


# show Sequence
Sequence_container = ttk.Frame(Fifth_Container)
sequence_str = display_sequence(random_sequence,random_reward_seqeunce)
print(sequence_str)
Sequence_label = tk.Label(Sequence_container, text="Generated Sequence: ", font=('Courier', 16))
Sequence_widget = tk.Text(Sequence_container, width=30, height=15, bg="#EFEFEF", fg="black", font=("Courier", 10))

Matrix_label.grid(pady=10, padx=20, column=0 , row=0)
Matrix_widget.grid(pady=10, padx=20, column=0 , row=1)
Sequence_label.grid(pady=10, padx=20, column=0 , row=0)
Sequence_widget.grid(pady=10, padx=20, column=0 , row=1)

Sequence_widget.config(state="normal")
Sequence_widget.insert("1.0", sequence_str)
Sequence_widget.config(state="disabled")


Matrix_Container.grid(row = 0, column= 0)
Sequence_container.grid(row=0, column=1)

# canvas = tk.Canvas(frame, width=800, height=400)
# canvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

# frame = tk.Frame(canvas)
# canvas.create_window((0, 0), anchor=tk.NW, frame=frame)

# frame.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))

# Output
output_str = get_output_data(None, None,None,None)
Output_Container = ttk.Frame(frame)
Output_label = tk.Label(Output_Container, text="Generated Sequence: ", font=('Courier', 16))
Output_widget = tk.Text(Output_Container, width=80, height=30, bg="#EFEFEF", fg="black", font=("Courier", 10))

Output_widget.config(state="disabled")

Output_label.grid(column=0,row=0)
Output_widget.grid(column=0,row=1)

# Save Button
SaveButton = ttk.Button(frame, width=15, text="Save Solutions", command=save_solutions)


# third_container.grid(row=0, column=1, padx=10, sticky='ne', pady=(30, 0))
second_container.grid(row=1, column=0, pady=(20,10), sticky='w')
third_container.grid(row = 2, column= 0, pady=(10,10), sticky='w')
fourth_container.grid(row = 3, column = 0,sticky='n', pady=(10,10))
main_direct_input_container.pack(anchor='n')
Calculate_Button.pack(pady=(10, 10), anchor='n')

Fifth_Container.pack(padx=20, anchor='n')

Output_Container.pack(padx=40)
SaveButton.pack(pady=20)


toggle_fullscreen()
window.mainloop()
