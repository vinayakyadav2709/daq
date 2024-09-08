import sys
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, END
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.simpledialog import askinteger
import serial
import threading
import time

# Adjust static path for now
# sys.path.append(r'C:\Users\Lenovo\Desktop\DAQPersonal-main\DAQPersonal-main\hostui')
from utils import file_utils

class DAQFileUI:
    def __init__(self, root):
        self.root = root
        self.file_path = None  # Initialize file_path
        self.serial_port = None  # Initialize serial port
        self.interval = 1  # Default interval (in seconds)
        self.thread = None  # Initialize the thread for sending data
        self.init_ui()

    def init_ui(self):
        self.create_frames()
        self.create_labels()
        self.create_textboxes()
        self.create_buttons()
        self.create_text_displayer()
        self.pack_frames()

    def create_frames(self):
        self.frame1 = ttk.Frame(self.root)
        self.frame2 = ttk.Frame(self.root)
        self.frame3 = ttk.Frame(self.root)
        self.frame4 = ttk.Frame(self.root)
        self.frame5 = ttk.Frame(self.root)
        self.frame6 = ttk.Frame(self.root)

    def create_labels(self):
        ttk.Label(self.frame2, text="Function code", font='Calibri 16').pack(side='left', padx=20)
        ttk.Label(self.frame2, text="First Byte", font='Calibri 16').pack(side='left', padx=20)
        ttk.Label(self.frame2, text="Second Byte", font='Calibri 16').pack(side='left', padx=20)

    def create_textboxes(self):
        self.t1_data = ttk.StringVar()
        self.t2_data = ttk.StringVar()
        self.t3_data = ttk.StringVar()

        ttk.Entry(self.frame3, textvariable=self.t1_data).pack(side="left", padx=5)
        ttk.Entry(self.frame3, textvariable=self.t2_data).pack(side="left", padx=5)
        ttk.Entry(self.frame3, textvariable=self.t3_data).pack(side="left", padx=5)

    def create_buttons(self):
        ttk.Button(self.frame1, text="Load file into displayer", command=self.load_file).pack(side="left", padx=10)
        ttk.Button(self.frame1, text="Create file for displayer data", command=self.create_file).pack(side="right", padx=10)
        ttk.Button(self.frame4, text="Append data to file", command=self.append_data).pack(side="right", padx=10)
        ttk.Button(self.frame4, text="Sync displayer with file", command=self.sync_fd).pack(side="right", padx=10)
        ttk.Button(self.frame4, text="Sync file with displayer", command=self.sync_df).pack(side="right", padx=10)
        ttk.Button(self.frame4, text="Send Data to Micro Controller", command=self.send_data).pack(side="right", padx=10)
        # ttk.Button(self.frame6, text="Send data to microcontroller", command=self.send_data).pack(side="right", padx=10)
        

    def create_text_displayer(self):
        self.data_displayer = ttk.Text(self.frame5, height=30, width=150)
        self.data_displayer.pack()

    def pack_frames(self):
        self.frame1.pack(pady=10)
        self.frame2.pack(pady=5)
        self.frame3.pack(pady=20)
        self.frame4.pack(pady=10)
        self.frame5.pack(pady=30)
        self.frame6.pack(pady=10)

    def load_file(self):
        self.file_path = askopenfilename(filetypes=[("Text Files", "*.txt")])
        if self.file_path:
            self.sync_fd()
        else:
            messagebox.showerror("File Error", "No file selected")

    def create_file(self):
        data = self.data_displayer.get("1.0", END).strip()
        if data:
            file_path = asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
            if file_path:
                file_utils.write_file(file_path, data)
        else:
            messagebox.showwarning("No content error", "Cannot create an empty file, add some data to the displayer first")

    def sync_fd(self):  # Load content from file to displayer
        if self.file_path:
            content = file_utils.read_file(self.file_path)
            self.data_displayer.delete('1.0', END)
            self.data_displayer.insert(END, content)
        else:
            messagebox.showerror("No file error", "Please select a file first")

    def sync_df(self):  # Save content from displayer to file
        if self.file_path:
            data = self.data_displayer.get("1.0", END).strip()
            if data:
                file_utils.write_file(self.file_path, data)
            else:
                messagebox.showwarning("No content error", "Cannot save an empty file, add some data to the displayer first")
        else:
            messagebox.showerror("No file error", "Please select a file first   ")

    def append_data(self):
        if self.file_path:
            data = self.t1_data.get() + self.t2_data.get() + self.t3_data.get()
            if data.strip():
                file_utils.append_file(self.file_path, data + '\n')  # Ensure each append is on a new line
                self.sync_fd()  # Optionally sync the displayer after appending
            else:
                messagebox.showwarning("No data error", "No data to append, enter data first")
        else:
            messagebox.showerror("No file error", "Please select a file first")

    def send_data(self):
        if not self.file_path:
            messagebox.showerror("No file error", "Please select a file first")
            return

        self.interval = askinteger("Interval", "Enter the interval (in seconds) between sending data:", minvalue=1, maxvalue=60)
        if self.interval is None:
            return

        data = file_utils.read_file(self.file_path).splitlines()
        if not data:
            messagebox.showwarning("No Data", "The file is empty. Nothing to send.")
            return

        # Ensure you have serial port opened and configured here
        try:
            self.serial_port = serial.Serial('/dev/ttyUSB0', 115200)  # Replace 'COM1' with your actual COM port and baud rate
        except serial.SerialException as e:
            messagebox.showerror("Serial Port Error", f"Could not open serial port: {e}")
            return

        # Start sending data in a new thread
        self.thread = threading.Thread(target=self.send_lines, args=(data,))
        self.thread.start()

    def send_lines(self, lines):
        
        
        data_to_send = [255,3]
        try:
            for line in lines:
                print(line.encode('utf-8') + b'\n')
                data_to_send.append(int((line.encode('utf-8')),16))
          
            data_to_send[1] = len(data_to_send)
            print(data_to_send)
            values = bytearray(data_to_send)
            
            #values = bytearray([255,3,19,255,0])
            print(values)
            self.serial_port.write(values)
            messagebox.showinfo("Sending Complete", "Data has been sent to the microcontroller")
        except serial.SerialException as e:
            messagebox.showerror("Serial Communication Error", f"Error during serial communication: {e}")
        finally:
            if self.serial_port and self.serial_port.is_open:
                self.serial_port.close()
        
        

if __name__ == "__main__":
    root = ttk.Window(themename='superhero')
    DAQFileUI(root)
    root.protocol("WM_DELETE_WINDOW", lambda: sys.exit(0))  # Ensure clean exit
    root.mainloop()
