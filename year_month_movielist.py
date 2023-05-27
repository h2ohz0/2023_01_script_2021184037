import requests
from tkinter import ttk, messagebox
from tkinter import *
from PIL import Image, ImageTk
from io import BytesIO

kofic_api_key = "f4ebe0c546de8755777b5f9ad9244615"

movie_details = None
label_poster = None

def get_movie_details(movie_id, kofic_api_key):
    api_key = "191bceef021f24c785530fc8364dcc11"
    movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"

    params = {
        "api_key": api_key,
        "region": "KR",
        "language": "ko-KR"
    }

    # Get movie details from TMDB API
    response = requests.get(movie_url, params=params)
    data = response.json()
    title = data.get("title", "")
    poster_path = data.get("poster_path", "")
    release_date = data.get("release_date", "")
    genres = [genre.get('name') for genre in data.get('genres', [])]

    # Get credits details from TMDB API
    response = requests.get(credits_url, params=params)
    data = response.json()

    director = ''
    for crew_member in data.get('crew', []):
        if crew_member.get('job') == 'Director':
            director = crew_member.get('name')
            break

    cast = [member.get('name') for member in data.get('cast', [])[:5]]

    # Get KOFIC movie ID
    kofic_url = f"http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key={kofic_api_key}&movieNm={title}"
    response = requests.get(kofic_url)
    kofic_data = response.json()
    kofic_movie_list = kofic_data.get("movieListResult", {}).get("movieList", [])

    kofic_movie_id = ""
    if kofic_movie_list:
        kofic_movie_id = kofic_movie_list[0].get("movieCd", "")

    # Get watch grade from KOFIC API
    watch_grade = "N/A"
    if kofic_movie_id:
        movie_id_str = str(kofic_movie_id)
        watch_grade = get_watch_grade(movie_id_str, kofic_api_key)

    return title, poster_path, director, cast, release_date, genres, watch_grade


def get_watch_grade(movie_id_str, kofic_api_key):
    kofic_url = f"http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?key={kofic_api_key}&movieCd={movie_id_str}"
    response = requests.get(kofic_url)
    kofic_data = response.json()
    audits = kofic_data.get("movieInfoResult", {}).get("movieInfo", {}).get("audits", [])
    watch_grade = audits[0].get("watchGradeNm", "N/A") if audits else "N/A"
    return watch_grade


def get_watch_grade(movie_id, kofic_api_key):
    url = f"http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json"
    params = {
        "key": kofic_api_key,
        "movieCd": movie_id
    }

    response = requests.get(url, params=params)
    data = response.json()

    movie_info = data.get("movieInfoResult", {}).get("movieInfo", {})
    watch_grade = movie_info.get("audits", [{}])[0].get("watchGradeNm", "N/A")

    return watch_grade

def create_scrollable_list(data, year, month, kofic_api_key):
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
            movie_info = get_movie_details(movie_id, kofic_api_key)

            movie_details.config(state=NORMAL)
            movie_details.delete(1.0, END)

            movie_details.insert(END,
                                 f'Title: {movie_info[0]}\nRelease Date: {movie_info[4]}\nDirector: {movie_info[2]}\nCast: {", ".join(movie_info[3])}\nGenres: {", ".join(movie_info[5])}\nWatch Grade: {movie_info[6]}')

            # Update movie poster
            if movie_info[1]:
                response = requests.get(f"https://image.tmdb.org/t/p/w200{movie_info[1]}")
                image = Image.open(BytesIO(response.content))
                photo = ImageTk.PhotoImage(image)
                label_poster.image = photo  # Keep a reference to the image
                label_poster.config(image=photo)
            else:
                label_poster.config(image='')

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
            kofic_api_key = "영화진흥위원회 발급한 API 키"
            if 1 <= month <= 12:
                movie_list = get_monthly_movie_list(year, month)
                create_scrollable_list(movie_list, year, month, kofic_api_key)
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