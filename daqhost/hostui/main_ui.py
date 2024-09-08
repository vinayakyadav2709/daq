import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import sys
#new
# Add the path to your custom UI classes
sys.path.append('/home/vishwajitsarnobat/workspace/DAQPersonal/hostui')

# Import your custom UI classes
from file.file_ui import DAQFileUI
from store.store_ui import DAQStoreUI

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.state('normal')
        self.init_ui()

    def init_ui(self):
        self.root.title("DAQ Management System")
        self.root.geometry("1200x800")

        # Create a Notebook widget
        tab_control = ttk.Notebook(self.root)

        # Create tabs
        self.store_tab = ttk.Frame(tab_control)
        self.file_tab = ttk.Frame(tab_control)

        # Add tabs to the notebook
        tab_control.add(self.store_tab, text='Storage Management')
        tab_control.add(self.file_tab, text='File Management')

        # Pack the notebook
        tab_control.pack(expand=1, fill="both", padx=10, pady=10)

        # Initialize the UIs in their respective tabs
        DAQFileUI(self.file_tab)
        DAQStoreUI(self.store_tab)

if __name__ == "__main__":
    root = ttk.Window(themename='superhero')
    MainApplication(root)
    root.mainloop()
