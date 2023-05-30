import requests
import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import timedelta, date

def get_korean_movie_data(start_year, end_year, start_month, end_month):
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

    start_date = date(int(start_year), int(start_month), 1)
    end_date = date(int(end_year), int(end_month), 1)

    try:
        while start_date <= end_date:
            params["primary_release_date.gte"] = f"{start_date.year}-{str(start_date.month).zfill(2)}-01"
            params["primary_release_date.lte"] = f"{start_date.year}-{str(start_date.month).zfill(2)}-31"

            response = requests.get(base_url, params=params)
            response.raise_for_status()

            data = response.json()
            total_results = data.get("total_results", 0)

            if str(start_date.year) not in movie_count:
                movie_count[str(start_date.year)] = {}
            movie_count[str(start_date.year)][str(start_date.month).zfill(2)] = total_results

            start_date = start_date.replace(day=1)
            start_date += timedelta(days=31)

        return movie_count

    except requests.exceptions.RequestException as e:
        print("An error occurred while making API request:", e)
    except Exception as e:
        print("An error occurred:", e)

    return None

def plot_data(movie_count):
    years = sorted(list(movie_count.keys()))
    months = list(range(1, 13))

    data = []
    for year in years:
        year_counts = []
        for month in months:
            count = movie_count.get(year, {}).get(str(month), 0)
            year_counts.append(int(count) if int(count) >= 0 else 0)
        data.append(year_counts)

    df = pd.DataFrame(data, index=years, columns=months)

    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(df.values, cmap="YlGnBu")

    ax.set_xticks(range(12))
    ax.set_yticks(range(len(years)))
    ax.set_xticklabels(months)
    ax.set_yticklabels(years)
    ax.set_xlabel("Month")
    ax.set_ylabel("Year")
    ax.set_title("Korean Movies - Yearly & Monthly Release Count")

    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel("Number of Movies Released", rotation=-90, va="bottom")

    return fig

def create_gui():
    global entry_start_year, entry_end_year, entry_start_month, entry_end_month

    def on_button_click():
        start_year = entry_start_year.get()
        start_month = entry_start_month.get()
        end_year = entry_end_year.get()
        end_month = entry_end_month.get()

        try:
            movie_count = get_korean_movie_data(start_year, end_year,
            end_month)
            figure = plot_data(movie_count)

            # Create Tkinter window
            root = tk.Tk()
            root.title("Korean Movies - Yearly & Monthly Release Count")

            # Create FigureCanvasTkAgg instance and add figure to it
            canvas = FigureCanvasTkAgg(figure, master=root)
            canvas.draw()

            # Add canvas to Tkinter window
            canvas.get_tk_widget().pack()

            # Start Tkinter event loop
            root.mainloop()
        except:
            messagebox.showerror("Error", "An error occurred while fetching data.")

    root = tk.Tk()
    root.title("Korean Movies - Yearly & Monthly Release Count")

    label_start_year = tk.Label(root, text="Start Year")
    label_start_year.grid(row=0, column=0)
    entry_start_year = tk.Entry(root)
    entry_start_year.grid(row=0, column=1)

    label_start_month = tk.Label(root, text="Start Month")
    label_start_month.grid(row=1, column=0)
    entry_start_month = tk.Entry(root)
    entry_start_month.grid(row=1, column=1)

    label_end_year = tk.Label(root, text="End Year")
    label_end_year.grid(row=2, column=0)
    entry_end_year = tk.Entry(root)
    entry_end_year.grid(row=2, column=1)

    label_end_month = tk.Label(root, text="End Month")
    label_end_month.grid(row=3, column=0)
    entry_end_month = tk.Entry(root)
    entry_end_month.grid(row=3, column=1)

    button_get_data = tk.Button(root, text="Get Data", command=on_button_click)
    button_get_data.grid(row=4, column=0, columnspan=2)

    root.mainloop()

create_gui()
