import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk, messagebox

def fetch_hot_100():
    url = "https://www.billboard.com/charts/hot-100/"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch Billboard chart:\n{e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    songs = soup.find_all("li", class_="o-chart-results-list__item")

    chart = []
    count = 0
    for item in songs:
        title = item.find("h3", id="title-of-a-story")
        artist = item.find("span", class_="c-label")
        if title and artist:
            chart.append(f"{count + 1}. {title.text.strip()} — {artist.text.strip()}")
            count += 1
        if count >= 100:
            break
    return chart

def show_chart():
    listbox.delete(0, tk.END)
    chart = fetch_hot_100()
    for entry in chart:
        listbox.insert(tk.END, entry)

# --- GUI Setup ---
root = tk.Tk()
root.title("🎵 Billboard Hot 100 Viewer")
root.geometry("700x700")
root.configure(bg="#1e1e1e")  # Dark background

# --- Style Configuration ---
style = ttk.Style()
style.theme_use("clam")

style.configure("TLabel", background="#1e1e1e", foreground="#f1f1f1", font=("Segoe UI", 18, "bold"))
style.configure("TButton", background="#2e2e2e", foreground="#f1f1f1", font=("Segoe UI", 12), padding=6)
style.map("TButton", background=[('active', '#3e3e3e')])
style.configure("TFrame", background="#1e1e1e")
style.configure("Vertical.TScrollbar", gripcount=0, background="#3e3e3e", troughcolor="#2e2e2e")

# --- Title ---
title_label = ttk.Label(root, text="🎶 Billboard Hot 100", anchor="center")
title_label.pack(pady=15)

# --- Frame & Scrollable Listbox ---
frame = ttk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

listbox = tk.Listbox(
    frame,
    font=("Segoe UI", 11),
    bg="#2a2a2a",
    fg="#f1f1f1",
    selectbackground="#44475a",
    selectforeground="#ffffff",
    activestyle="none",
    bd=0,
    highlightthickness=1,
    relief="flat"
)

scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=listbox.yview)
listbox.config(yscrollcommand=scrollbar.set)

listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# --- Load Button (optional) ---
button = ttk.Button(root, text="📡 Reload Chart", command=show_chart)
button.pack(pady=15)

# --- Footer ---
footer = ttk.Label(root, text="Data provided by billboard.com", font=("Segoe UI", 9), anchor="center")
footer.pack(pady=5)

# ✅ Auto-load chart on startup
root.after(100, show_chart)

# --- Run App ---
root.mainloop()
