from django.shortcuts import get_object_or_404, render
from .models import Blog  # Blog 모델을 임포트해야 합니다.

def blog_list(request):
    blogs = Blog.objects.all()  # 모델명은 대문자 Blog

    visits = int(request.COOKIES.get('visits', 9)) +1

    request.session['count'] = request.session.get('count', 0) + 1

    context = {
        'blogs': blogs,
        'count': request.session['count'],
    }

    response = render(request, 'blog_list.html', context)

    response.set_cookie('visits', visits)

    return response

    # return render(request, 'blog_list.html', context)  # 템플릿 이름도 일반적으로 언더스코어 사용
    #


def blog_detail(request, pk):
    get_object_or_404(Blog, pk=pk)
    context = {'blog' : Blog}
    return render(request, 'blog_detail.html' , context )
