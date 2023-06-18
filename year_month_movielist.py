import requests
from tkinter import ttk, messagebox
from tkinter import *
from PIL import Image, ImageTk
from io import BytesIO
import webbrowser


movie_details = None
label_poster = None

def get_movie_details(movie_id):
    api_key = "191bceef021f24c785530fc8364dcc11"
    movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    release_dates_url = f"https://api.themoviedb.org/3/movie/{movie_id}/release_dates"

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

    # Get watch grade from TMDB API
    response = requests.get(release_dates_url, params=params)
    data = response.json()
    releases = data.get('results', [])
    watch_grade = 'N/A'
    for release in releases:
        if release.get('iso_3166_1') == 'KR':
            certifications = release.get('release_dates', [])
            for certification in certifications:
                if certification.get('type') == 3:  # 3 is for theatrical release
                    watch_grade = certification.get('certification')
                    break
            break

    videos_url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos"
    response = requests.get(videos_url, params=params)
    data = response.json()
    youtube_key = None
    for video in data.get('results', []):
        if video.get('site') == 'YouTube' and video.get('type') == 'Trailer':
            youtube_key = video.get('key')
            break

    return title, poster_path, director, cast, release_date, genres, watch_grade, youtube_key

def create_scrollable_list(data, year, month):
    root = Toplevel()
    root.title("Movie List")
    root.geometry("1100x800")  # Change the size of the window here
    root.configure(background='#c5d6eb')

    movie_count = len(data)

    label_info = Label(root, text=f"\"{year}년 {month}월\" 개봉 국내 영화 개수: {movie_count}", font=('한컴 말랑말랑 Regular', 18, "bold"))
    label_info.configure(background='#c5d6eb')
    label_info.pack(pady = 15)

    frame = Frame(root)
    frame.pack()

    scrollbar = Scrollbar(frame)
    scrollbar.pack(side=RIGHT, fill=Y)

    label_movie_list = Label(frame, text = "개봉 영화",font=('한컴 말랑말랑 Bold',15))
    label_movie_list.pack()

    listbox = Listbox(frame, yscrollcommand=scrollbar.set, width=40, font=('한컴 말랑말랑 Regular', 15))
    listbox.pack(side=LEFT, fill=BOTH, padx = 10, pady = 10)

    scrollbar.config(command=listbox.yview)

    movie_details = Text(root, width=40, font=('한컴 말랑말랑 Regular', 15))
    movie_details.pack(side=LEFT, padx = 100, pady = 25)


    label_poster = Label(root)
    label_poster.pack(side=LEFT, pady =20)


    def on_movie_select(event):
        index = listbox.curselection()
        if index:
            movie_id = data[index[0]]["id"]
            movie_info = get_movie_details(movie_id)

            movie_details.config(state=NORMAL)
            movie_details.delete(1.0, END)

            movie_details.insert(END,
                                 f'<{movie_info[0]}>\n개봉일: {movie_info[4]}\n감독: {movie_info[2]}\n출연: {", ".join(movie_info[3])}\n장르: {", ".join(movie_info[5])}\n관람 등급: {movie_info[6]}')

            # Update movie poster
            if movie_info[1]:
                response = requests.get(f"https://image.tmdb.org/t/p/w200{movie_info[1]}")
                image = Image.open(BytesIO(response.content))

                photo = ImageTk.PhotoImage(image)
                label_poster.image = photo  # Keep a reference to the image
                label_poster.config(image=photo)
            else:
                label_poster.config(image='')

            if movie_info[7]:  # If there is a Youtube key
                youtube_url = f"https://www.youtube.com/watch?v={movie_info[7]}"
                trailer_button.config(command=lambda: webbrowser.open(youtube_url), state=NORMAL,font=('한컴 말랑말랑 Regular', 10))
            else:
                # If there is no trailer, disable the button
                trailer_button.config(command=None, state=DISABLED,font=('한컴 말랑말랑 Regular', 10))
    listbox.bind("<<ListboxSelect>>", on_movie_select)

    for item in data:
        listbox.insert(END, item["title"])

    trailer_button = Button(root, text="예고편 보러가기", state=DISABLED,font=('한컴 말랑말랑 Regular', 15))
    trailer_button.pack(side=LEFT, padx = 50, pady=10)

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

    all_movies = []  # 모든 영화를 저장할 리스트

    page = 1
    while True:
        params["page"] = page

        response = requests.get(base_url, params=params)
        data = response.json()

        movie_list = data["results"]
        all_movies.extend(movie_list)  # 현재 페이지의 영화를 전체 리스트에 추가

        # 다음 페이지가 없으면 반복 종료
        if page >= data["total_pages"]:
            break

        page += 1
    return all_movies


def create_gui(root):
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

    label_year = Label(root, text="Year",background = '#c5d6eb', font = ("한컴 말랑말랑 Bold", 10))
    label_year.grid(row=0, column=0)
    entry_year = Entry(root)
    entry_year.grid(row=0, column=1)

    label_month = Label(root, text="Month", background = '#c5d6eb', font = ("한컴 말랑말랑 Bold", 10))
    label_month.grid(row=1, column=0)
    entry_month = Entry(root)
    entry_month.grid(row=1, column=1)

    button_get_data = Button(root, text="Get Movie List", font = ("한컴 말랑말랑 Bold", 10), command=on_button_click)
    button_get_data.grid(row=2, column=0, columnspan=2)

if __name__ == "__main__":
    root = Tk()
    root.title("Movie List")
    root.resizable(False, False)
    root.configure(background='#c5d6eb')
    create_gui(root)
    root.mainloop()
