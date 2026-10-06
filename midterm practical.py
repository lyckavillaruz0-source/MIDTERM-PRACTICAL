import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Database setup
conn = sqlite3.connect("artists.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS artists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    genre TEXT NOT NULL
)
""")
conn.commit()

# CREATE
def add_artist():
    name = name_entry.get()
    age = age_entry.get()
    genre = genre_entry.get()

    if name == "" or age == "" or genre == "":
        messagebox.showwarning("Warning", "Please fill in all fields.")
        return

    try:
        age = int(age)
    except ValueError:
        messagebox.showerror("Error", "Age must be a number.")
        return

    cursor.execute("INSERT INTO artists (name, age, genre) VALUES (?, ?, ?)", (name, age, genre))
    conn.commit()

    messagebox.showinfo("Success", "Artist added successfully.")
    clear_fields()
    display_artists()

# READ
def display_artists():
    for item in tree.get_children():
        tree.delete(item)

    cursor.execute("SELECT name, age, genre FROM artists")  # only select needed columns
    artists = cursor.fetchall()

    for artist in artists:
        tree.insert("", tk.END, values=artist)

# UPDATE
def update_artist():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Please select an artist to update.")
        return

    name = name_entry.get()
    age = age_entry.get()
    genre = genre_entry.get()

    if name == "" or age == "" or genre == "":
        messagebox.showwarning("Warning", "Please fill in all fields.")
        return

    try:
        age = int(age)
    except ValueError:
        messagebox.showerror("Error", "Age must be a number.")
        return

    old_values = tree.item(selected[0])["values"]
    old_name, old_age, old_genre = old_values

    cursor.execute("""
    UPDATE artists
    SET name = ?, age = ?, genre = ?
    WHERE name = ? AND age = ? AND genre = ?
    """, (name, age, genre, old_name, old_age, old_genre))
    conn.commit()

    messagebox.showinfo("Success", "Artist updated successfully.")
    clear_fields()
    display_artists()

# DELETE
def delete_artist():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Please select an artist to delete.")
        return

    values = tree.item(selected[0])["values"]
    name, age, genre = values

    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this artist?")
    if confirm:
        cursor.execute("DELETE FROM artists WHERE name = ? AND age = ? AND genre = ?", (name, age, genre))
        conn.commit()
        messagebox.showinfo("Success", "Artist deleted successfully.")
        clear_fields()
        display_artists()

# CLEAR INPUTS
def clear_fields():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    genre_entry.delete(0, tk.END)

# SELECT ARTIST
def select_artist(event):
    selected = tree.selection()
    if selected:
        artist = tree.item(selected[0])["values"]
        clear_fields()
        name_entry.insert(0, artist[0])
        age_entry.insert(0, artist[1])
        genre_entry.insert(0, artist[2])

# GUI Setup
root = tk.Tk()
root.title("Song Artist Information")
root.geometry("700x500")

BG_COLOR = "#EAF4FB"
root.configure(bg=BG_COLOR)

# Title
title_label = tk.Label(root, text="Song Artist Information",
                       font=("Arial", 18, "bold"), bg=BG_COLOR, fg="black")
title_label.pack(pady=10)

# Input Frame
input_frame = tk.Frame(root, bg="white")
input_frame.pack(pady=10)

tk.Label(input_frame, text="Artist Name:", bg="white").grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(input_frame, width=30, bg="#FFFFFF", fg="#212121")
name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Age:", bg="white").grid(row=1, column=0, padx=5, pady=5)
age_entry = tk.Entry(input_frame, width=30, bg="#FFFFFF", fg="#212121")
age_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Genre:", bg="white").grid(row=2, column=0, padx=5, pady=5)
genre_entry = tk.Entry(input_frame, width=30, bg="#FFFFFF", fg="#212121")
genre_entry.grid(row=2, column=1, padx=5, pady=5)

# Buttons
button_frame = tk.Frame(root, bg=BG_COLOR)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Add", width=10, bg="#228B22", fg="white", command=add_artist).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Update", width=10, bg="#191970", fg="white", command=update_artist).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Delete", width=10, bg="#800020", fg="white", command=delete_artist).grid(row=0, column=2, padx=5)
tk.Button(button_frame, text="Clear", width=10, bg="#36454F", fg="white", command=clear_fields).grid(row=0, column=3, padx=5)
tk.Button(button_frame, text="Exit", width=10, bg="#FF4500", fg="white", command=root.destroy).grid(row=0, column=4, padx=5)

# Table Styling
style = ttk.Style()
style.theme_use("clam")

style.configure("Treeview.Heading", background="#808080", foreground="black", font=("Arial", 11, "bold"))
style.configure("Treeview", background="white", foreground="#212121", fieldbackground="white", rowheight=25)
style.map("Treeview", background=[("selected", "#5DADE2")], foreground=[("selected", "white")])

# Table (no ID column)
tree = ttk.Treeview(root, columns=("Name", "Age", "Genre"), show="headings")
tree.heading("Name", text="Artist Name")
tree.heading("Age", text="Age")
tree.heading("Genre", text="Genre")

tree.column("Name", width=200)
tree.column("Age", width=100)
tree.column("Genre", width=200)

tree.pack(fill="both", expand=True, padx=10, pady=10)
tree.bind("<<TreeviewSelect>>", select_artist)

# Display existing records
display_artists()

root.mainloop()
conn.close()
