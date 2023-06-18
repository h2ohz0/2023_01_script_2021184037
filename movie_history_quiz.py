import requests
import random
from tkinter import *
from tkinter import messagebox

class Quiz:

    def __init__(self, root):
        self.asked_movies = []

        self.root = root
        self.root.geometry('800x200')
        self.root.title('영화 히스토리 퀴즈')
        self.api_key = '191bceef021f24c785530fc8364dcc11'
        self.language = 'ko'
        self.movies = self.get_korean_movies()
        self.quiz_number = 1
        self.score = 0
        self.current_movie = None

        self.question_label = Label(self.root, text="")
        self.question_label.pack()

        self.answer_entry = Entry(self.root)
        self.answer_entry.pack()

        self.next_button = Button(self.root, text="다음 문제", command=self.next_quiz, font=('한컴 말랑말랑 Regular', 10))
        self.next_button.pack()

        self.score_label = Label(self.root, text="")
        self.score_label.pack()

        self.generate_quiz()



    def get_korean_movies(self):
        url = f'https://api.themoviedb.org/3/discover/movie?api_key={self.api_key}&language={self.language}&region=KR&with_original_language=ko'
        response = requests.get(url)
        data = response.json()
        return data['results']

    def get_movie_details(self, movie_id):
        url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={self.api_key}&language={self.language}&append_to_response=credits,release_dates'
        response = requests.get(url)
        data = response.json()
        return data

    def get_director(self, crew):
        for member in crew:
            if member['job'] == 'Director':
                return member['name']
        return ''

    def get_age_rating(self, release_dates):
        for release in release_dates:
            if release['iso_3166_1'] == 'KR':
                return release['release_dates'][0]['certification'] if release['release_dates'] and release['release_dates'][0]['certification'] else 'NR'
        return 'NR'

    def generate_quiz(self):
        self.current_movie = random.choice(self.movies)
        self.movies.remove(self.current_movie)  # 현재 영화를 영화 리스트에서 제거
        self.asked_movies.append(self.current_movie['title'])  # 현재 영화 제목을 asked_movies 목록에 추가
        details = self.get_movie_details(self.current_movie['id'])
        director = self.get_director(details['credits']['crew'])
        age_rating = self.get_age_rating(details['release_dates']['results'])
        self.question_label.config(
            text=f'[문제 {self.quiz_number}]\n {self.current_movie["release_date"]}에 개봉\n {", ".join([genre["name"] for genre in details["genres"]])} 장르\n 주요 배우로는 {", ".join([cast["name"] for cast in details["credits"]["cast"][:5]])}이 출연했습니다.\n 감독은 {director}입니다.\n 이 영화의 등급은 {age_rating}입니다.\n이 영화의 제목은 무엇인가요?', background='#c5d6eb', font=('한컴 말랑말랑 Regular', 10, "bold"))

    def next_quiz(self):
        user_answer = self.answer_entry.get().replace(" ", "").lower()
        correct_answer = self.current_movie['title'].replace(" ", "").lower()
        if user_answer == correct_answer:
            self.score += 1
            messagebox.showinfo("정답", "정답입니다!")
        else:
            messagebox.showinfo("오답", f"오답입니다. 정답은 {self.current_movie['title']}입니다.")

        if self.quiz_number == 5:
            movie_list = '\n'.join(self.asked_movies)
            messagebox.showinfo("퀴즈 종료", f"당신의 점수는 {self.score}/5입니다. 출제된 영화들은 다음과 같습니다:\n\n{movie_list}")
            self.root.quit()
        else:
            self.quiz_number += 1
            self.score_label.config(text=f'현재 점수: {self.score}', font=('한컴 말랑말랑 Regular', 10, "bold"))
            self.answer_entry.delete(0, 'end')
            self.generate_quiz()


root = Tk()
quiz = Quiz(root)
root.configure(background='#c5d6eb')
root.mainloop()
