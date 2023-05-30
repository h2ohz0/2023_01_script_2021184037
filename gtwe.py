import requests
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from datetime import timedelta, date

def get_korean_movie_data(start_year, end_year):
    api_key = "191bceef021f24c785530fc8364dcc11"
    base_url = "https://api.themoviedb.org/3/discover/movie"

    params = {
        "api_key": api_key,
        "language": "ko-KR",
        "region": "KR",
        "with_original_language": "ko",
        "page": 1
    }

    movie_count = {}

    start_date = date(int(start_year), 1, 1)
    end_date = date(int(end_year), 12, 31)

    while start_date <= end_date:
        params["primary_release_date.gte"] = f"{start_date.year}-01-01"
        params["primary_release_date.lte"] = f"{start_date.year}-12-31"

        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            total_results = data.get("total_results", 0)
        else:
            print(f"API request failed with status code {response.status_code}.")
            total_results = 0

        movie_count[str(start_date.year)] = total_results
        start_date += timedelta(days=365)  # ensure moving to the next year
        start_date = date(start_date.year, 1, 1)  # reset month and day to 1

    return movie_count

def plot_data_line(movie_count):
    years = sorted(list(movie_count.keys()))

    fig, ax = plt.subplots(figsize=(8, 6))

    counts = [movie_count.get(year, 0) for year in years]
    line, = ax.plot(years, counts, marker='o')

    for i, txt in enumerate(counts):
        ax.annotate(txt, (years[i], counts[i]),
                    textcoords="offset points",  # how to position the text
                    xytext=(0,10),  # distance from text to points (x,y)
                    ha='center')  # horizontal alignment can be left, right or center

    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Movies Released")
    ax.set_title("Korean Movies - Yearly Release Count")

    return fig

def create_gui():
    global entry_start_year, entry_end_year

    def on_button_click():
        start_year = entry_start_year.get()
        end_year = entry_end_year.get()

        try:
            movie_count = get_korean_movie_data(start_year, end_year)
            figure = plot_data_line(movie_count)

            # Clear the previous plot in the canvas
            for widget in root.winfo_children():
                if isinstance(widget, FigureCanvasTkAgg):
                    widget.get_tk_widget().destroy()

            canvas = FigureCanvasTkAgg(figure, master=root)
            canvas.draw()
            canvas.get_tk_widget().grid(row=3, column=2, columnspan=2)

        except Exception as e:
            print(e)
            messagebox.showerror("Error", "An error occurred while fetching data.")

    root = tk.Tk()
    root.title("Korean Movies - Yearly Release Count")

    label_start_year = tk.Label(root, text="Start Year")
    label_start_year.grid(row=0, column=0)
    entry_start_year = tk.Entry(root)
    entry_start_year.grid(row=0, column=1)

    label_end_year = tk.Label(root, text="End Year")
    label_end_year.grid(row=1, column=0)
    entry_end_year = tk.Entry(root)
    entry_end_year.grid(row=1, column=1)

    button_get_data = tk.Button(root, text="Get Data", command=on_button_click)
    button_get_data.grid(row=2, column=0)

    root.mainloop()

create_gui()

