import tkinter as tk
from tkinter import Label, Button
import time

class TransparentClock(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Transparent Digital Clock")
        self.geometry("200x80")

        self.overrideredirect(True)  # Remove window decorations (title bar, close button, etc.)
        self.wm_attributes("-topmost", True)  # Keep the window on top of all other windows
        self.wm_attributes("-alpha", 0.8)  # Set the window transparency (0.0 is fully transparent, 1.0 is fully opaque)

        self.time_label = Label(self, font=('Helvetica', 20), fg='white', bg='black')
        self.time_label.pack(expand=True, fill='both')

        self.close_button = Button(self, text="Close", command=self.close_window)
        self.close_button.pack()

        self.update_clock()

        # Bind mouse events to enable dragging
        self.time_label.bind("<Button-1>", self.start_move)
        self.time_label.bind("<B1-Motion>", self.do_move)

    def update_clock(self):
        current_time = time.strftime('%H:%M:%S')
        self.time_label.config(text=current_time)
        self.after(1000, self.update_clock)  # Update the clock every 1000 milliseconds (1 second)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        x = self.winfo_pointerx() - self.x
        y = self.winfo_pointery() - self.y
        self.geometry(f"+{x}+{y}")

    def close_window(self):
        self.destroy()  # Destroy the window
        self.master.destroy()  # Destroy the root (main) window
        import sys; sys.exit()  # Exit the script

def create_clock():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    clock = TransparentClock(master=root)
    clock.mainloop()

if __name__ == "__main__":
    create_clock()
