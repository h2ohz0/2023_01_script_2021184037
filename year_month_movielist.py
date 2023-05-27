import requests
from tkinter import ttk, messagebox
from tkinter import *
from PIL import Image, ImageTk
from io import BytesIO


movie_details = None
label_poster = None

def get_movie_details(movie_id):
    api_key = "191bceef021f24c785530fc8364dcc11"
    movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"

    params = {
        "api_key": api_key,
        "region": "KR",
        "language": "ko-KR"  # Set the language parameter to "ko-KR"
    }

    # get movie details
    response = requests.get(movie_url, params=params)
    data = response.json()
    title = data.get("title", "")
    poster_path = data.get("poster_path", "")
    release_date = data.get("release_date", "")

    # get genres
    genres = [genre.get('name') for genre in data.get('genres', [])]

    # get credits details
    response = requests.get(credits_url, params=params)
    data = response.json()

    director = ''
    for crew_member in data.get('crew', []):
        if crew_member.get('job') == 'Director':
            director = crew_member.get('name')
            break

    cast = [member.get('name') for member in data.get('cast', [])[:5]]

    return title, poster_path, director, cast, release_date, genres  # Updated to return genres


def create_scrollable_list(data, year, month):
    root = Toplevel()
    root.title("Movie List")
    root.geometry("1000x700")  # Change the size of the window here

    label_info = Label(root, text=f"Year: {year}   Month: {month}")
    label_info.pack(pady=10)

    scrollbar = Scrollbar(root)
    scrollbar.pack(side=RIGHT, fill=Y)

    listbox = Listbox(root, yscrollcommand=scrollbar.set, width=50)
    listbox.pack(side=LEFT, fill=BOTH)

    scrollbar.config(command=listbox.yview)

    movie_details = Text(root, width=50)
    movie_details.pack(side=LEFT)

    label_poster = Label(root)
    label_poster.pack(side=LEFT)

    def on_movie_select(event):
        index = listbox.curselection()
        if index:
            movie_id = data[index[0]]["id"]
            title, poster_path, director, cast, release_date, genres = get_movie_details(
                movie_id)  # Updated to get genres

            movie_details.config(state=NORMAL)
            movie_details.delete(1.0, END)

            movie_details.insert(END,
                                 f'Title: {title}\nRelease Date: {release_date}\nDirector: {director}\nCast: {", ".join(cast)}\nGenres: {", ".join(genres)}')  # Updated to display genres

            # Update movie poster
            if poster_path:
                response = requests.get(f"https://image.tmdb.org/t/p/w200{poster_path}")
                image = Image.open(BytesIO(response.content))
                photo = ImageTk.PhotoImage(image)
                label_poster.image = photo  # Keep a reference to the image
                label_poster.config(image=photo)
            else:
                label_poster.config(image='')  # Clear the label if no image

    listbox.bind("<<ListboxSelect>>", on_movie_select)

    for item in data:
        listbox.insert(END, item["title"])

    root.mainloop()


def get_monthly_movie_list(year, month):
    api_key = "191bceef021f24c785530fc8364dcc11"
    base_url = "https://api.themoviedb.org/3/discover/movie"

    params = {
        "api_key": api_key,
        "language": "ko-KR",
        "region": "KR",
        "with_original_language": "ko",
        "primary_release_year": year,
        "primary_release_date.gte": f"{year}-{month:02d}-01",
        "primary_release_date.lte": f"{year}-{month:02d}-31",
        "page": 1
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    movie_list = data["results"]

    return movie_list

def create_gui():
    def on_button_click():
        try:
            year = int(entry_year.get())
            month = int(entry_month.get())
            if 1 <= month <= 12:
                movie_list = get_monthly_movie_list(year, month)
                create_scrollable_list(movie_list, year, month)
            else:
                messagebox.showerror("Error", "Month must be between 1 and 12.")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid year and month.")

    root = Tk()
    root.title("Movie List")

    label_year = Label(root, text="Year")
    label_year.grid(row=0, column=0)
    entry_year = Entry(root)
    entry_year.grid(row=0, column=1)

    label_month = Label(root, text="Month")
    label_month.grid(row=1, column=0)
    entry_month = Entry(root)
    entry_month.grid(row=1, column=1)

    button_get_data = Button(root, text="Get Movie List", command=on_button_click)
    button_get_data.grid(row=2, column=0, columnspan=2)

    root.mainloop()

create_gui()
