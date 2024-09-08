from tkinter import filedialog as fd

def choose_file():
    file_path = fd.askopenfilename(initialdir="/", title="Select a file", filetypes=(("Text file", "*.txt*"), ("CSV file", "*.csv*")))
    return file_path

def create_new_file():
    file_path = fd.asksaveasfilename(
        defaultextension=".txt",  # Default file extension
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        title="Save As"
    )
    return file_path

def read_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
        return data
 
def print_file(line_list):
    for line in line_list:
        print(line)
        
def write_file(file_path, data):
    open_file = open(file_path,'w')
    open_file.write(data + "\n")
    open_file.close()
    
def append_file(file_path, data):
    open_file = open(file_path,'a')
    open_file.write(data + "\n")
    open_file.close()
    
    
