import requests
import matplotlib.pyplot as plt

# API 키
api_key = 'f4ebe0c546de8755777b5f9ad9244615'
year = '2023'

# 연도별 영화 출시 통계
def get_yearly_movie_statistics():
    url = f'https://api.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key={api_key}&curPage=1&itemPerPage=10&openStartDt={year}-01-01&openEndDt={year}-12-31'
    response = requests.get(url)
    data = response.json()

    print(data)  # API 응답 확인용

    total_count = data['movieListResult']['totCnt']
    return total_count


# 월별 영화 출시 통계
def get_monthly_movie_statistics():
    monthly_counts = {}

    for month in range(1, 13):
        url = f'https://api.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key={api_key}&curPage=1&itemPerPage=10&openStartDt={year}-{month:02d}-01&openEndDt={year}-{month:02d}-31'
        response = requests.get(url)
        data = response.json()

        print(data)  # API 응답 확인용

        total_count = data['movieListResult']['totCnt']
        monthly_counts[month] = total_count

    return monthly_counts

# 특정 감독의 인기 지표 분석
def get_director_popularity(director_name):
    url = f'https://api.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json?key={api_key}&peopleNm={director_name}'
    response = requests.get(url)
    data = response.json()

    print(data)  # API 응답 확인용

    if data['peopleListResult']['totCnt'] == 0:
        return 'Director not found.'

    director_code = data['peopleListResult']['peopleList'][0]['peopleCd']

    url = f'https://api.kobis.or.kr/kobisopenapi/webservice/rest/people/popularMovies.json?key={api_key}&peopleCd={director_code}'
    response = requests.get(url)
    data = response.json()

    popular_movies = data['peopleListResult']['peopleList'][0]['filmoNames']
    return popular_movies

# 연도별 영화 출시 통계 시각화
def plot_yearly_movie_statistics():
    years = range(2010, 2023)
    movie_counts = []

    for year in years:
        total_count = get_yearly_movie_statistics(year)
        movie_counts.append(total_count)

    plt.plot(years, movie_counts)
    plt.xlabel('Year')
    plt.ylabel('Number of Movies')
    plt.title('Yearly Movie Release Statistics')
    plt.show()

# 월별 영화 출시 통계 시각화
def plot_monthly_movie_statistics():
    monthly_counts = get_monthly_movie_statistics()
    months = list(monthly_counts.keys())
    counts = list(monthly_counts.values())

    plt.bar(months, counts)
    plt.xlabel('Month')
    plt.ylabel('Number of Movies')
    plt.title('Monthly Movie Release Statistics')
    plt.show()

# 특정 감독의 인기 지표 분석 및 시각화
def analyze_director_popularity(director_name):
    movies = get_director_popularity(director_name)

    if movies == 'Director not found.':
        print(movies)
    else:
        movie_list = movies.split(',')

        # 영화별 인기 지표
        movie_scores = []
        for movie in movie_list:
            url = f'https://api.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?key={api_key}&movieNm={movie}'
            response = requests.get(url)
            data = response.json()

            movie_score = data['movieInfoResult']['movieInfo']['audiCnt']
            movie_scores.append(int(movie_score))

        # 영화 인기 지표 시각화
        plt.bar(movie_list, movie_scores)
        plt.xlabel('Movie')
        plt.ylabel('Popularity Score')
        plt.title(f'Popularity Score of Movies by {director_name}')
        plt.xticks(rotation=90)
        plt.show()

# 연도별 영화 출시 통계 시각화
plot_yearly_movie_statistics()

# 월별 영화 출시 통계 시각화
plot_monthly_movie_statistics()

# 특정 감독의 인기 지표 분석 및 시각화
director_name = '이명세'  # 원하는 감독 이름으로 변경
analyze_director_popularity(director_name)
