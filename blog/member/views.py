from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def sign_up(request):
    username = request.POST.get('username')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')

    print('username:', username)
    print('password1:', password1)
    print('password2:', password2)

    # username 중복확인작업
    # 패스워드가 맞는지 , 그리고 패스워드 정책에 올바른지 (대소문자)

    if request.methed == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/accousts/login/')
    else:
        form = UserCreationForm()

    context = {
        'from':form
    }
    return render(request, 'registration/signup.html')