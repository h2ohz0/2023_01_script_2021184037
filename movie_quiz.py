import tkinter as tk
from tkinter import messagebox
import requests
import random

# TMDB API 키
API_KEY = "191bceef021f24c785530fc8364dcc11"


class MovieQuizApplication:
    def __init__(self, master):
        self.master = master
        self.master.title("영화 히스토리 퀴즈")
        self.master.geometry("300x200")

        self.label = tk.Label(master, text="출시 연도에 따른 영화 퀴즈를 선택하세요.")
        self.label.pack()

        self.button1 = tk.Button(master, text="2000년대 이전", command=self.get_quiz_pre_2000s)
        self.button1.pack()

        self.button2 = tk.Button(master, text="2000-2010년", command=self.get_quiz_2000s_to_2010s)
        self.button2.pack()

        self.button3 = tk.Button(master, text="2011년 이후", command=self.get_quiz_after_2011)
        self.button3.pack()

    def get_movies_by_release_year(self, year_start, year_end):
        # 특정 연도 범위에 해당하는 한국 영화 목록을 가져오는 함수
        response = requests.get(
            f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&region=KR&primary_release_date.gte={year_start}-01-01&primary_release_date.lte={year_end}-12-31")
        movies = response.json()['results']

        return movies

    def get_movie_details(self, movie_id):
        # 특정 영화의 상세 정보를 가져오는 함수
        response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}")
        movie_details = response.json()

        return movie_details

    def create_quiz(self, movies):
        # 영화 목록에서 무작위로 하나를 선택하고 퀴즈를 만드는 함수
        movie = random.choice(movies)
        movie_details = self.get_movie_details(movie['id'])

        question = f"이 영화의 감독은 {movie_details['director']}입니다. 내용은 {movie_details['overview']}입니다. 최초 개봉일은 {movie_details['release_date']}입니다. 이 영화의 이름은 무엇인가요?"
        answer = movie_details['title']

        return question, answer

    def get_quiz_pre_2000s(self):
        movies = self.get_movies_by_release_year(1900, 1999)
        quiz_question, quiz_answer = self.create_quiz(movies)
        messagebox.showinfo("Quiz", quiz_question)

    def get_quiz_2000s_to_2010s(self):
        movies = self.get_movies_by_release_year(2000, 2010)
        quiz_question, quiz_answer = self.create_quiz(movies)
        messagebox.showinfo("Quiz", quiz_question)

    def get_quiz_after_2011(self):
        movies = self.get_movies_by_release_year(2011, 2023)
        quiz_question, quiz_answer = self.create_quiz(movies)
        messagebox.showinfo("Quiz", quiz_question)


root = tk.Tk()
app = MovieQuizApplication(root)
root.mainloop()
