
import sys
import time
import sqlite3
import telepot
import requests
import traceback
from datetime import date

TOKEN = '6162134309:AAErOQOG9MK7Bpu3YHjlcMI89qcW6O7L_dE'
TMDB_KEY = '191bceef021f24c785530fc8364dcc11'
BASE_URL = f'https://api.themoviedb.org/3/movie/now_playing?api_key={TMDB_KEY}&language=ko-KR&page=1&region=KR'
bot = telepot.Bot(TOKEN)


def getMovieData():
    res = requests.get(BASE_URL)
    if res.status_code == 200:
        return res.json()['results']
    else:
        return []


def sendMessage(user, msg):
    try:
        bot.sendMessage(user, msg)
    except:
        traceback.print_exc(file=sys.stdout)


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return

    text = msg['text']

    if text.startswith('영화'):
        movie_data = getMovieData()
        if movie_data:
            for movie in movie_data:
                sendMessage(chat_id,
                            f"제목: {movie['title']}\n개봉일: {movie['release_date']}\n평점: {movie['vote_average']}\n설명: {movie['overview']}")
        else:
            sendMessage(chat_id, '개봉 예정인 영화가 없습니다.')
    else:
        sendMessage(chat_id, "모르는 명령어입니다.\n영화 명령어를 입력하세요.")


print('Listening...')

bot.message_loop(handle)

while 1:
    time.sleep(10)
