import requests
from tkinter import ttk, messagebox
from tkinter import *
from PIL import Image, ImageTk
from io import BytesIO
import webbrowser
import requests
from tkinter import messagebox
import matplotlib.pyplot as plt
import pandas as pd
from datetime import timedelta, date
import tkinter.filedialog

api_key = "191bceef021f24c785530fc8364dcc11"

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
def on_button_click():
    try:
        year = int(entry_year.get())
        month = int(entry_month.get())
        if 1 <= month <= 12:
            movie_list = get_monthly_movie_list(year, month)
            create_scrollable_list(movie_list, year, month)  # remove kofic_api_key
        else:
            messagebox.showerror("Error", "Month must be between 1 and 12.")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid year and month.")


def code2():
    year = int(entry_year.get())
    month = int(entry_month.get())

    if 1 <= month <= 12:
        movie_list = get_monthly_movie_list(year, month)
        create_scrollable_list(movie_list, year, month)
    else:
        messagebox.showerror("Error", "Month must be between 1 and 12.")

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

                start_date += timedelta(days=32)  # ensure moving to the next month
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


# GUI를 생성합니다.
root = Tk()
root.title("Movie List")

# 코드 1에 대한 프레임을 생성합니다.
frame1 = Frame(root)
frame1.grid(row=0, column=0)

label_year = Label(frame1, text="Year", font = ("한컴 말랑말랑 Bold", 10))
label_year.grid(row=0, column=0)
entry_year = Entry(frame1)
entry_year.grid(row=0, column=1)

label_month = Label(frame1, text="Month", font = ("한컴 말랑말랑 Bold", 10))
label_month.grid(row=1, column=0)
entry_month = Entry(frame1)
entry_month.grid(row=1, column=1)

button_get_data = Button(frame1, text="Get Movie List", font = ("한컴 말랑말랑 Bold", 10), command=on_button_click)
button_get_data.grid(row=2, column=0, columnspan=2)

# 코드 2에 대한 프레임을 생성합니다.
frame2 = Frame(root)
frame2.grid(row=0, column=1)

button_code2 = Button(frame2, text="Code 2", font = ("한컴 말랑말랑 Bold", 10), command=code2)
button_code2.pack()

root.mainloop()