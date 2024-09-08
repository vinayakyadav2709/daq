import ttkbootstrap as ttk
import serial.tools.list_ports
import serial
import sys
import threading
from tkinter import messagebox, END

# Adjust static path for now
# sys.path.append(r'C:\Users\Lenovo\Desktop\DAQPersonal-main\DAQPersonal-main\hostui')
from utils import database_utils, csv_utils, text_utils

class DAQStoreUI:
    def __init__(self, root):
        self.root = root
        self.flag = False  # Flag to control background threads
        self.serial_connection = None  # To keep track of the serial connection
        self.lock = threading.Lock()  # To ensure thread-safe operations
        self.init_ui()

    def init_ui(self):
        self.create_frames()
        self.create_widgets()
        self.pack_frames()
        self.com_select()
        self.baud_select()

    def create_frames(self):
        self.frame1 = ttk.Frame(self.root)
        self.frame2 = ttk.Frame(self.root)
        self.frame3 = ttk.Frame(self.root)
        self.frame4 = ttk.Frame(self.root)
        self.frame5 = ttk.Frame(self.root)
        self.frame6 = ttk.Frame(self.root)
        self.frame7 = ttk.Frame(self.root)

    def create_widgets(self):
        self.create_port_widgets()
        self.create_baud_widgets()
        self.create_control_buttons()
        self.create_store_buttons()
        self.create_data_displayer()

    def create_port_widgets(self):
        self.port_label = ttk.Label(self.frame1, text="Available Port(s): ", font='Calibri 16')
        self.port_label.pack(side='left', padx=10)

    def create_baud_widgets(self):
        self.bd_label = ttk.Label(self.frame2, text="Baud Rate: ", font='Calibri 16')
        self.bd_label.pack(side='left', padx=10)

    def create_control_buttons(self):
        self.connect_btn = ttk.Button(self.frame3, text="Connect", state='disabled', command=self.connect)
        self.connect_btn.pack(side='left', padx=10)
        self.default_btn = ttk.Button(self.frame3, text="Set to default", command=self.default)
        self.default_btn.pack(side='left', padx=10)
        self.refresh_btn = ttk.Button(self.frame3, text="Refresh", command=self.com_select)
        self.refresh_btn.pack(side='left', padx=10)

    def create_store_buttons(self):
        self.store_btn = ttk.Button(self.frame4, text="Store to DB", state='disabled', command=self.start_store_thread)
        self.store_btn.pack(side='left', padx=10)
        self.stop_store_btn = ttk.Button(self.frame4, text="Stop", state='disabled', command=self.stop_store)
        self.stop_store_btn.pack(side='left', padx=10)
        self.csv_store_btn = ttk.Button(self.frame5, text="Store to CSV", state='disabled', command=self.start_csv_store_thread)
        self.csv_store_btn.pack(side='left', padx=10)
        self.csv_stop_btn = ttk.Button(self.frame5, text="Stop", state='disabled', command=self.csv_stop_store)
        self.csv_stop_btn.pack(side='left', padx=10)
        self.text_store_btn = ttk.Button(self.frame6, text="Store to Text file", state='disabled', command=self.start_text_store_thread)
        self.text_store_btn.pack(side='left', padx=10)
        self.text_stop_btn = ttk.Button(self.frame6, text="Stop", state='disabled', command=self.text_stop_store)
        self.text_stop_btn.pack(side='left', padx=10)

    def create_data_displayer(self):
        self.data_displayer = ttk.Text(self.frame7, height=20, width=80)
        self.data_displayer.pack()

    def pack_frames(self):
        self.frame1.pack(pady=10)
        self.frame2.pack(pady=10)
        self.frame3.pack(pady=20)
        self.frame4.pack(pady=10)
        self.frame5.pack(pady=10)
        self.frame6.pack(pady=10)
        self.frame7.pack(pady=30)

    def baud_select(self):
        self.clicked_bd = ttk.StringVar()
        bds = ["-", "300", "600", "1200", "2400", "4800", "9600", "14400", "19200", "28800", "38400", "56000", "57600", "115200", "128000", "256000"]
        self.clicked_bd.set(bds[0])
        self.drop_bd = ttk.OptionMenu(self.frame2, self.clicked_bd, *bds, command=self.connect_check)
        self.drop_bd.config(width=20)
        self.drop_bd.pack(side='left', padx=10)

    def com_select(self):
        self.clicked_com = ttk.StringVar()
        self.ports = serial.tools.list_ports.comports()
        self.coms = [com.device for com in self.ports]
        print(f"Detected ports: {self.coms}")
        self.coms.insert(0, "-")
        self.clicked_com.set(self.coms[0])
        try:
            self.drop_com.destroy()
        except AttributeError:
            pass
        self.drop_com = ttk.OptionMenu(self.frame1, self.clicked_com, *self.coms, command=self.connect_check)
        self.drop_com.config(width=20)
        self.drop_com.pack(side='left', padx=10)

    def connect_check(self):
        if "-" in self.clicked_com.get() or "-" in self.clicked_bd.get():
            self.connect_btn["state"] = "disabled"
        else:
            self.connect_btn["state"] = "active"

    def default(self):
        if len(self.coms) > 1:
            self.clicked_bd.set("115200")
            self.connect_btn["state"] = "active"
            self.clicked_com.set(self.coms[1])
        else:
            messagebox.showerror("Port error", "No device was detected, please make sure device is properly connected")

    def connect(self):
        if self.connect_btn.cget('text') == "Connect":
            try:
                self.serial_connection = serial.Serial(self.clicked_com.get(), self.clicked_bd.get())
                self.connect_btn['text'] = "Disconnect"
                self.refresh_btn['state'] = 'disabled'
                self.default_btn['state'] = 'disabled'
                self.drop_bd['state'] = 'disabled'
                self.drop_com['state'] = 'disabled'
                self.store_btn['state'] = 'active'
                self.csv_store_btn['state'] = 'active'
                self.text_store_btn['state'] = 'active'
            except serial.SerialException as e:
                messagebox.showerror("Connection Error", f"Failed to connect to {self.clicked_com.get()}.\nError: {e}")
        else:
            self.disconnect()

    def disconnect(self):
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
        self.connect_btn['text'] = "Connect"
        self.refresh_btn['state'] = 'active'
        self.default_btn['state'] = 'active'
        self.drop_bd['state'] = 'active'
        self.drop_com['state'] = 'active'
        self.csv_store_btn['state'] = 'disabled'
        self.text_store_btn['state'] = 'disabled'
        self.store_btn['state'] = 'disabled'

    def start_store_thread(self):
        if not self.flag:
            self.flag = True
            self.store_thread = threading.Thread(target=self.store)
            self.store_thread.start()

    def store(self):
        self.stop_store_btn['state'] = 'active'
        self.store_btn['state'] = 'disabled'
        serial_port = self.clicked_com.get()
        baud_rate = self.clicked_bd.get()
        try:
            ser = serial.Serial(serial_port, baud_rate)
        except serial.SerialException as e:
            messagebox.showerror("Serial Error", f"Failed to connect to {serial_port}. Error: {e}")
            self.stop_store_btn['state'] = 'disabled'
            self.store_btn['state'] = 'active'
            return

        messagebox.showinfo("Storing initiated", "Storing pin data into the database ...")
        database_utils.database_connect()
        while self.flag:
            data = self.read_serial(ser)
            self.display(data)
            database_utils.database_store(data)
            self.root.update()
        database_utils.database_disconnect()
        ser.close()
        self.stop_store_btn['state'] = 'disabled'
        self.store_btn['state'] = 'active'

    def stop_store(self):
        with self.lock:
            self.flag = False

    def start_csv_store_thread(self):
        if not self.flag:
            self.flag = True
            self.csv_store_thread = threading.Thread(target=self.csv_store)
            self.csv_store_thread.start()

    def csv_store(self):
        self.csv_stop_btn['state'] = 'active'
        self.csv_store_btn['state'] = 'disabled'
        serial_port = self.clicked_com.get()
        baud_rate = self.clicked_bd.get()
        try:
            ser = serial.Serial(serial_port, baud_rate)
        except serial.SerialException as e:
            messagebox.showerror("Serial Error", f"Failed to connect to {serial_port}. Error: {e}")
            self.csv_stop_btn['state'] = 'disabled'
            self.csv_store_btn['state'] = 'active'
            return

        messagebox.showinfo("Storing initiated", "Storing pin data into the output.csv ...")
        while self.flag:
            data = self.read_serial(ser)
            self.display(data)
            csv_utils.store(data)
            self.root.update()
        ser.close()
        self.csv_stop_btn['state'] = 'disabled'
        self.csv_store_btn['state'] = 'active'

    def csv_stop_store(self):
        with self.lock:
            self.flag = False

    def start_text_store_thread(self):
        if not self.flag:
            self.flag = True
            self.text_store_thread = threading.Thread(target=self.text_store)
            self.text_store_thread.start()

    def text_store(self):
        self.text_stop_btn['state'] = 'active'
        self.text_store_btn['state'] = 'disabled'
        serial_port = self.clicked_com.get()
        baud_rate = self.clicked_bd.get()
        try:
            ser = serial.Serial(serial_port, baud_rate)
        except serial.SerialException as e:
            messagebox.showerror("Serial Error", f"Failed to connect to {serial_port}. Error: {e}")
            self.text_stop_btn['state'] = 'disabled'
            self.text_store_btn['state'] = 'active'
            return

        messagebox.showinfo("Storing initiated", "Storing pin data into the output.txt ...")
        while self.flag:
            data = self.read_serial(ser)
            self.display(data)
            text_utils.store(data)
            self.root.update()
        ser.close()
        self.text_stop_btn['state'] = 'disabled'
        self.text_store_btn['state'] = 'active'

    def text_stop_store(self):
        with self.lock:
            self.flag = False

    def read_serial(self, ser):
        try:
            line = ser.readline()
            decoded_line = line.decode('utf-8')
            return decoded_line
        except serial.SerialException as e:
            messagebox.showerror("Serial Error", f"Failed to read from serial port. Error: {e}")
            self.disconnect()
            return ""

    def display(self, data):
        self.root.after(0, lambda: self.data_displayer.insert(END, data))
        self.root.after(0, lambda: self.data_displayer.yview(END))

if __name__ == "__main__":
    root = ttk.Window(themename='superhero')
    DAQStoreUI(root)
    root.protocol("WM_DELETE_WINDOW", lambda: sys.exit(0))  # Ensure clean exit
    root.mainloop()
