import tkinter as tk
from tkinter import ttk, filedialog
from random import randint


window = tk.Tk()

def toggle_fullscreen(event = None):
    window.attributes("-fullscreen", not window.attributes("-fullscreen"))


def open_file():
    global filename
    global image_default_value
    global the_image
    global resized_image

    file_path = filedialog.askopenfilename(title="Sele", filetypes=[('Image files', '*.png *.jpg *.jpeg')])
    if file_path:
        filename.set(file_path)
        image_default_value = file_path
        # image_displayer.config(image=the_image)

def update_background_and_text(value):
    if value < 0.5:
        # Update to color A when slider moves to the left
        label_color.config(foreground="#0066CC")
        label_texture.config(foreground="#0066CC")
    else:
        # Update to color B when slider moves to the right
        label_color.config(foreground="#555555")
        label_texture.config(foreground="#555555")

def bg_color(color):
    window.configure(bg=color)

def update_selection():
    selection = slider.get()

    color_1 = '#7E7E7E'
    color_2 = '#8A8A8A' 
    if selection == 0:
        slider.configure(troughcolor=color_1)
        label_color.config(foreground=color_2)
        label_texture.config(foreground=color_2)
    else:
        slider.configure(troughcolor=color_2)
        label_color.config(foreground=color_1)
        label_texture.config(foreground=color_1)

def search(slider):
    #called when the search button is clicked
    global folderpath

def update_gui(event):
    print("test")
    window.update()

def get_color(color_name):
    return color_data.get(color_name)

def display_matrix(matrix):
    matrix_str = ""
    for row in matrix:
        row_str = " ".join(map(str,row)) + "\n"
        matrix_str += row_str
    return matrix_str

def display_sequence(sequences, sequence_reward):
    sequences_str = ""
    for i, item in enumerate(sequences):
        sequence_str = f"Sequence {i+1}: {' '.join(map(str,item))}\n"
        sequence_str += f"Reward {i+1}: {sequence_reward[i]}\n\n"
        sequences_str += sequence_str
    return sequences_str

window.geometry("1000x800")


def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

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

# folderpath = ""
# search_button = tk.Button(main_direct_input_container, text="Search", width=18, height=2,command= lambda : search(slider))

slider.bind("<ButtonRelease-1>", lambda event: update_selection())
slider.set(0)
update_selection()


# Second Container
second_container = ttk.Frame(main_direct_input_container)

# Buffer_Input
buffer_background = tk.Label(second_container,bg="#7C7C7C", height=15)
buffer_background.grid(row = 0, column = 0, sticky='w')
buffer_text = tk.Label(buffer_background, text="Entry Buffer: ",bg="#7E7E7E", font="Calibri 12", width=25, foreground='white', anchor='w')
buffer_text.grid(row=0, column=0, sticky='w')
buffer_entry = tk.Entry(buffer_background, width=7, font="Calibri 12")
buffer_entry.grid(pady=5, padx=5, row=1, column=0, sticky='w')

# Unique Token
Unique_token_background = tk.Label(second_container,bg="#7C7C7C", height=15)
Unique_token_background.grid(row = 1, column = 0, sticky='w', pady=(20,20))
Unique_token_text = tk.Label(Unique_token_background, text="Entry Unique token: ",bg="#7E7E7E", font="Calibri 12", width=25, foreground='white', anchor='w')
Unique_token_text.grid(row=0, column=0, sticky='w')
Unique_token_entry = tk.Entry(Unique_token_background, width=7, font="Calibri 12")
Unique_token_entry.grid(pady=5, padx=5, row=1, column=0, sticky='w')

# third container
third_container = ttk.Frame(main_direct_input_container)

# Max Unique Sequence Token
max_sequence_token_background = tk.Label(third_container,bg="#7C7C7C", height=15)
max_sequence_token_background.grid(row = 0, column = 0, sticky='w', pady=(10,20))
max_sequence_token_text = tk.Label(max_sequence_token_background, text="Entry Max Token in Sequences: ",bg="#7E7E7E", font="Calibri 12", width=25, foreground='white', anchor='w')
max_sequence_token_text.grid(row=0, column=0, sticky='w')
max_sequence_token_entry = tk.Entry(max_sequence_token_background, width=7, font="Calibri 12")
max_sequence_token_entry.grid(pady=5, padx=5, row=1, column=0, sticky='w')


# Max Sequence
Max_Sequence_background = tk.Label(third_container,bg="#7C7C7C", height=15)
Max_Sequence_background.grid(row = 0, column = 1, sticky='w', padx=20, pady=(10,20))
Max_Sequence_text = tk.Label(Max_Sequence_background, text="Entry Max Amount Of Sequence: ",bg="#7E7E7E", font="Calibri 12", width=25, foreground='white', anchor='w')
Max_Sequence_text.grid(row=0, column=0, sticky='w')
Max_Sequence_entry = tk.Entry(Max_Sequence_background, width=7, font="Calibri 12")
Max_Sequence_entry.grid(pady=5, padx=5, row=1, column=0, sticky='w')


fourth_container = tk.Frame(main_direct_input_container)
# Matrix Col
Matrix_Col_background = tk.Label(fourth_container,bg="#7C7C7C", height=15)
Matrix_Col_background.grid(row = 0, column = 0, sticky='w', pady=(10,20))
Matrix_Col_text = tk.Label(Matrix_Col_background, text="Matrix Col: ",bg="#7E7E7E", font="Calibri 12", width=25, foreground='white', anchor='w')
Matrix_Col_text.grid(row=0, column=0, sticky='w')
Matrix_Col_entry = tk.Entry(Matrix_Col_background, width=7, font="Calibri 12")
Matrix_Col_entry.grid(pady=5, padx=5, row=1, column=0, sticky='w')

# Matrix Row

Matrix_Row_background = tk.Label(fourth_container,bg="#7C7C7C", height=15)
Matrix_Row_background.grid(row = 0, column = 1, sticky='w', pady=(10,20), padx=20)
Matrix_Row_text = tk.Label(Matrix_Row_background, text="Matrix Row: ",bg="#7E7E7E", font="Calibri 12", width=25, foreground='white', anchor='w')
Matrix_Row_text.grid(row=0, column=0, sticky='w')
Matrix_Row_entry = tk.Entry(Matrix_Row_background, width=7, font="Calibri 12")
Matrix_Row_entry.grid(pady=5, padx=5, row=1, column=0, sticky='w')

# Calculate Button
Calculate_Button = tk.Button(frame, height=5, width=20)
Calculate_Label = tk.Label(Calculate_Button, text="Calculate Solution")
Calculate_Label.grid(row= 0, column=0)

#---------------- Middle Input  ----------------#
# show matrix, and sequences

# test
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

sequence = [
    ['BD','E9','1C'],
    ['BD','7A','BD'],
    ['BD','1C','BD','55']
]

reward = [15,20,30]

Fifth_Container = ttk.Frame(frame)

# show matrix 
matrix_str = display_matrix(matrix)
Matrix_Container = ttk.Frame(Fifth_Container)
Matrix_label = tk.Label(Matrix_Container, text="Generated Matrix: ", font=('Courier', 16))
Matrix_widget = tk.Text(Matrix_Container, width=30, height=15, bg="#EFEFEF", fg="black", font=("Courier", 10))



# Matrix configuration
Matrix_widget.config(state="normal")
Matrix_widget.insert("1.0", matrix_str)
Matrix_widget.config(state="disabled")


# show Sequence
Sequence_container = ttk.Frame(Fifth_Container)
sequence_str = display_sequence(sequence,reward)
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
Output_Container = ttk.Frame(frame)
Output_label = tk.Label(Output_Container, text="Generated Sequence: ", font=('Courier', 16))
Output_widget = tk.Text(Output_Container, width=80, height=30, bg="#EFEFEF", fg="black", font=("Courier", 10))

Output_label.grid(column=0,row=0)
Output_widget.grid(column=0,row=1)

# Save Button
SaveButton = ttk.Button(frame, width=15, text="Save Solutions")


# PACKERS
label_color.grid(row=0, column=0)
slider.grid(row=0, column=1)
label_texture.grid(row=0, column=2)

slider_container.pack(pady=(10, 20))


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
