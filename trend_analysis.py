import requests
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from datetime import timedelta, date
import tkinter.filedialog


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

    while start_date <= end_date:
        params["primary_release_date.gte"] = f"{start_date.year}-{str(start_date.month).zfill(2)}-01"
        params["primary_release_date.lte"] = f"{start_date.year}-{str(start_date.month).zfill(2)}-31"

        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            total_results = data.get("total_results", 0)
        else:
            print(f"API request failed with status code {response.status_code}.")
            total_results = 0

        if str(start_date.year) not in movie_count:
            movie_count[str(start_date.year)] = {}
        movie_count[str(start_date.year)][str(start_date.month).zfill(2)] = total_results

        start_date += timedelta(days=32) # ensure moving to the next month
        start_date = date(start_date.year, start_date.month, 1)  # reset day to 1

    return movie_count


def plot_data_line(movie_count):
    years = sorted(list(movie_count.keys()))
    months = list(range(1, 13))
    month_labels = [str(month).zfill(2) for month in months]

    fig, ax = plt.subplots(figsize=(8, 6))

    for year in years:
        counts = [movie_count.get(year, {}).get(month, 0) for month in month_labels]
        line, = ax.plot(month_labels, counts, marker='o', label=year)

        for i, txt in enumerate(counts):
            ax.annotate(txt, (month_labels[i], counts[i]),
                        textcoords="offset points",  # how to position the text
                        xytext=(0, 10),  # distance from text to points (x,y)
                        ha='center')  # horizontal alignment can be left, right or center

    ax.set_xlabel("Month")
    ax.set_ylabel("Number of Movies Released")
    ax.set_title("Korean Movies - Yearly & Monthly Release Count")
    ax.legend()

    return fig


def plot_data_heatmap(movie_count):
    years = sorted(list(movie_count.keys()))
    months = list(range(1, 13))
    counts = []

    for year in years:
        year_counts = []
        for month in months:
            month_str = str(month).zfill(2)
            count = movie_count.get(year, {}).get(month_str, 0)
            year_counts.append(int(count) if int(count) >= 0 else 0)
        counts.append(year_counts)

    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(counts, cmap="YlGnBu")

    ax.set_xticks(range(12))
    ax.set_yticks(range(len(years)))
    ax.set_xticklabels(months)
    ax.set_yticklabels(years)
    ax.set_xlabel("Month")
    ax.set_ylabel("Year")
    ax.set_title("Korean Movies - Yearly & Monthly Release Count")

    # Loop over data dimensions and create text annotations.
    for i in range(len(years)):
        for j in range(len(months)):
            text = ax.text(j, i, counts[i][j], ha="center", va="center", color="black")

    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel("Number of Movies Released", rotation=-90, va="bottom")

    return fig

def data_to_dataframe(movie_count):
    years = sorted(list(movie_count.keys()))
    months = list(range(1, 13))
    month_labels = [str(month).zfill(2) for month in months]
    data_dict = {}

    for year in years:
        counts = [movie_count.get(year, {}).get(month, 0) for month in month_labels]
        data_dict[year] = counts

    df = pd.DataFrame(data_dict, index=month_labels)
    df.index.name = "Month"
    df.columns.name = "Year"

    return df
def save_data_to_excel(dataframe):
    file_name = tkinter.filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                     filetypes=(("Excel file", "*.xlsx"),
                                                                ("All files", "*.*")))
    if file_name:
        dataframe.to_excel(file_name)
def save_plot(figure):
    file_name = tkinter.filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=(("PNG file", "*.png"),
                                                                ("JPEG file", "*.jpg"),
                                                                ("All files", "*.*")))
    if file_name:
        figure.savefig(file_name)
def create_gui():
    global entry_start_year, entry_end_year, entry_start_month, entry_end_month, var_plot_type

    def on_button_click():
        start_year = entry_start_year.get()
        start_month = entry_start_month.get()
        end_year = entry_end_year.get()
        end_month = entry_end_month.get()

        try:
            movie_count = get_korean_movie_data(start_year, end_year, start_month, end_month)
            # Save the movie count data in a global variable so that it can be accessed by save_button_click
            global current_data
            current_data = data_to_dataframe(movie_count)

            plot_type = var_plot_type.get()
            if plot_type == 'Line':
                figure = plot_data_line(movie_count)
            elif plot_type == 'Heatmap':
                figure = plot_data_heatmap(movie_count)

            # Save the figure in a global variable so that it can be accessed by save_button_click
            global current_figure
            current_figure = figure

            # Clear the previous plot in the canvas
            for widget in root.winfo_children():
                if isinstance(widget, FigureCanvasTkAgg):
                    widget.get_tk_widget().destroy()

            canvas = FigureCanvasTkAgg(figure, master=root)
            canvas.draw()
            canvas.get_tk_widget().grid(row=5, column=3, columnspan=3)

        except Exception as e:
            print(e)
            messagebox.showerror("Error", "An error occurred while fetching data.")

    def save_button_click():
        if 'current_data' in globals():
            save_data_to_excel(current_data)
        else:
            messagebox.showinfo("Info", "No data to save. Please get data first.")

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
    button_get_data.grid(row=4, column=0)

    var_plot_type = tk.StringVar(root)
    var_plot_type.set("Heatmap")  # default value
    plot_types = ["Heatmap", "Line"]
    dropdown = tk.OptionMenu(root, var_plot_type, *plot_types)
    dropdown.grid(row=4, column=1)

    button_save_plot = tk.Button(root, text="Save Plot", command=save_button_click)
    button_save_plot.grid(row=4, column=2)

    button_save_data = tk.Button(root, text="Save Data", command=save_button_click)
    button_save_data.grid(row=4, column=3)

    root.mainloop()

create_gui()