import time
import telepot
import requests
from datetime import date

TOKEN = '6162134309:AAErOQOG9MK7Bpu3YHjlcMI89qcW6O7L_dE'
TMDB_API_KEY = '191bceef021f24c785530fc8364dcc11'
bot = telepot.Bot(TOKEN)

def get_now_playing_movies():
    url = f"https://api.themoviedb.org/3/movie/now_playing?api_key={TMDB_API_KEY}&language=ko-KR&region=KR&page=1"
    response = requests.get(url)
    data = response.json()
    movies = data.get('results', [])
    return movies

def get_today_release_movies():
    today = date.today().isoformat()
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&primary_release_date.gte={today}&primary_release_date.lte={today}&region=KR"
    response = requests.get(url)
    data = response.json()
    movies = data.get('results', [])
    return movies

def send_movies_info(chat_id, movies):
    for movie in movies:
        title = movie.get('title')
        release_date = movie.get('release_date')
        overview = movie.get('overview')
        movie_id = movie.get('id')
        tmdb_url = f"https://www.themoviedb.org/movie/{movie_id}"
        message = f"Title: {title}\nRelease Date: {release_date}\nOverview: {overview}\nLink: {tmdb_url}"
        bot.sendMessage(chat_id, message)

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        bot.sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return

    text = msg['text']

    if text == '상영 영화 정보':
        movies = get_now_playing_movies()
        send_movies_info(chat_id, movies)
    elif text == '오늘 개봉 영화':
        movies = get_today_release_movies()
        send_movies_info(chat_id, movies)
    else:
        bot.sendMessage(chat_id, "모르는 명령어입니다. '상영 영화 정보' 또는 '오늘 개봉 영화' 중 하나의 명령을 입력하세요.")

bot.message_loop(handle)

print('Listening...')

while 1:
  time.sleep(10)