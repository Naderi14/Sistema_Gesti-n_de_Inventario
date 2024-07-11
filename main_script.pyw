from GUI.gui_script import SGIgui
from tkinter import Tk
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

if __name__ == "__main__":
    root = Tk()
    root.title("SGI Manager")
    root.geometry("1080x780")
    root.resizable(0,0)
    app = SGIgui(root)
    root.mainloop()
    
    
    