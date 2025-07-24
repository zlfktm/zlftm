"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.http import HttpResponse, Http404
from django.contrib import admin
from django.urls import path
from django.shortcuts import render

# 영화 리스트
movies_list = [
    {'title': '파묘', 'directer': '장재현'},
    {'title': '윙카', 'directer': '폴 킴'},
    {'title': '튠: 파트2', 'directer': '드니 발뇌브'},
    {'title': '시민덕희', 'directer': '박영주'},
]

# 기본 인덱스
def index(request):
    return HttpResponse('<h1>hello</h1>')

# 책 리스트 출력
def blog_list(request):
    book_text = ''
    for i in range(10):
        book_text += f'book {i}<br>'
    return HttpResponse(book_text)

# 개별 책
def book(request, num):
    return HttpResponse(f'book {num}번 페이지입니다.')

# 영화 목록 페이지
def movies(request):
    return render(request, 'movies.html', {'movie_list': movies_list})

# 영화 상세 페이지
def movie_detail(request, index):
    if index < 0 or index >= len(movies_list):
        raise Http404("해당 영화가 존재하지 않습니다.")

    movie = movies_list[index]
    return render(request, 'movie.html', {'movie': movie})

# 언어 페이지
def language(request, lang):
    return HttpResponse(f'<h1>{lang} 언어 페이지입니다.</h1>')







def gugu(request, dan):
    context ={
        'dan' : dan,
        'results' : [dan * i for i in range(1, 10)]

    }

    return render(request, 'gugu.html',context)











# URL 패턴
urlpatterns = [
    path("admin/", admin.site.urls),
    path('', index),
    path('book_list/', blog_list),
    path('book_list/<int:num>/', book),
    path('language/<str:lang>/', language),
    path('movies/', movies),
    path('movies/<int:index>/', movie_detail),
    path('gugu/<int:dan>/', gugu),
]
