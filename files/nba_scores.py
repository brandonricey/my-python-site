from nba_api.stats.endpoints import ScoreboardV2
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import os

# Get yesterday's date
yesterday = datetime.now() - timedelta(days=1)
date_str = yesterday.strftime('%m/%d/%Y')

# Setup loading window
loading_root = tk.Tk()
loading_root.title("NBA Scores")
loading_label = tk.Label(loading_root, text="🏀 Fetching NBA scores...", font=("Helvetica", 14), padx=20, pady=20)
loading_label.pack()
loading_root.update_idletasks()
w = loading_root.winfo_width()
h = loading_root.winfo_height()
x = (loading_root.winfo_screenwidth() // 2) - (w // 2)
y = (loading_root.winfo_screenheight() // 2) - (h // 2)
loading_root.geometry(f"{w}x{h}+{x}+{y}")

def fetch_scores():
    try:
        scoreboard = ScoreboardV2(game_date=date_str)
        line_scores = scoreboard.get_normalized_dict().get('LineScore', [])
        games = []

        if not line_scores:
            games.append((None, "No games found", None, "or data not available yet"))
        else:
            for i in range(0, len(line_scores), 2):
                try:
                    team1 = line_scores[i]
                    team2 = line_scores[i + 1]
                    games.append((
                        team1['TEAM_ABBREVIATION'], f"{team1['TEAM_ABBREVIATION']} {team1['PTS']}",
                        team2['TEAM_ABBREVIATION'], f"{team2['TEAM_ABBREVIATION']} {team2['PTS']}"
                    ))
                except Exception as e:
                    games.append((None, "Error reading game", None, str(e)))
    except Exception as e:
        games = [(None, "Error fetching scores", None, str(e))]

    loading_root.after(0, show_results, games)

def load_logo(team_abbr):
    try:
        logo_path = os.path.join("logos", f"{team_abbr}.png")
        print(f"Trying to load: {logo_path}")
        img = Image.open(logo_path).resize((50, 50), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Failed to load logo for {team_abbr}: {e}")
        return None

def show_results(games):
    loading_root.destroy()
    result_root = tk.Tk()
    result_root.title("🏀 NBA Scores")

    # Colors
    bg_color = "#1e1e1e"
    fg_color = "#f5f5f5"
    accent_color = "#4CAF50"

    result_root.configure(bg=bg_color)

    # Header
    header = tk.Label(result_root, text=f"NBA Scores for {date_str}", font=("Helvetica", 16, "bold"),
                      fg=accent_color, bg=bg_color, pady=10)
    header.pack()

    # Scrollable frame setup
    canvas = tk.Canvas(result_root, bg=bg_color, highlightthickness=0)
    scrollbar = ttk.Scrollbar(result_root, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg=bg_color)
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scroll_frame.bind("<Configure>", on_frame_configure)

    # Store image references
    logo_images = []

    # Display games
    for i, (abbr1, score1, abbr2, score2) in enumerate(games):
        row_bg = "#2a2a2a" if i % 2 == 0 else "#333333"
        row_frame = tk.Frame(scroll_frame, bg=row_bg, pady=5)
        row_frame.pack(fill="x", padx=10, pady=5)

        # Team 1
        if abbr1:
            logo1 = load_logo(abbr1)
            logo_images.append(logo1)  # Prevent garbage collection
            if logo1:
                tk.Label(row_frame, image=logo1, bg=row_bg).pack(side="left", padx=10)
        tk.Label(row_frame, text=score1, font=("Helvetica", 13), fg=fg_color, bg=row_bg).pack(side="left", padx=10)

        # VS separator
        tk.Label(row_frame, text="🆚", font=("Helvetica", 13, "bold"), fg=accent_color, bg=row_bg).pack(side="left", padx=10)

        # Team 2
        if abbr2:
            logo2 = load_logo(abbr2)
            logo_images.append(logo2)
            if logo2:
                tk.Label(row_frame, image=logo2, bg=row_bg).pack(side="left", padx=10)
        tk.Label(row_frame, text=score2, font=("Helvetica", 13), fg=fg_color, bg=row_bg).pack(side="left", padx=10)

    # Update window layout and resize
    result_root.update_idletasks()
    w = result_root.winfo_reqwidth()
    h = min(result_root.winfo_reqheight(), 800)  # Cap height if too tall
    x = (result_root.winfo_screenwidth() // 2) - (w // 2)
    y = (result_root.winfo_screenheight() // 2) - (h // 2)
    result_root.geometry(f"{w}x{h}+{x}+{y}")
    
    result_root.mainloop()

# Start thread
threading.Thread(target=fetch_scores).start()
loading_root.mainloop()