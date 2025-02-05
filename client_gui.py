import tkinter as tk
from tkinter import scrolledtext

def count_words():
    # Placeholder function for counting words
    text_display.insert(tk.END, "Count words function called\n")

def translate_text():
    # Placeholder function for translating text
    text_display.insert(tk.END, "Translate text function called\n")

# Create the main window
root = tk.Tk()
root.title("Client Interface")

# Create a frame for the buttons
frame = tk.Frame(root)
frame.pack(pady=10)

# Create and pack the buttons
count_button = tk.Button(frame, text="Count Words", command=count_words)
count_button.pack(side=tk.LEFT, padx=5)

translate_button = tk.Button(frame, text="Translate Text", command=translate_text)
translate_button.pack(side=tk.LEFT, padx=5)

# Create and pack the text display area
text_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
text_display.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()