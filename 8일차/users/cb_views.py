from django.contrib.auth import get_user_model, login
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls.base import reverse_lazy
from django.views.generic import FormView, CreateView
from django.core.signing import TimestampSigner, SignatureExpired
from django.core import signing
from django.conf import settings

from users.forms import SignupForm, LoginForm
from utils.email import send_email


User = get_user_model()


class SignupView(CreateView) :
    template_name = 'registration/signup.html'
    form_class = SignupForm

    def form_valid(self, form) :
        user = form.save()

        signer = TimestampSigner()
        signed_user_email = signer.sign(user.email)
        signer_dump = signing.dumps(signed_user_email)

        url = f'{self.request.scheme}://{self.request.META["HTTP_HOST"]}/users/verify/?code={signer_dump}'

        # if settings.DEBUG :
        #     print(url)
        # else :
        #     subject = '[Todo] 이메일 인증을 완료해주세요'
        #     message = f'다음 링크를 클릭해주세요. <a href="{url}">{url}</a>'
        #
        #     send_email(subject, message, user.email)

        subject = '[Todo] 이메일 인증을 완료해주세요'
        message = f'다음 링크를 클릭해주세요. <a href="{url}">{url}</a>'

        send_email(subject, message, user.email)

        return render(
            request = self.request,
            template_name='registration/signup_done.html',
            context= {'user' : user,}
        )

def verify_email(request):
    code = request.GET.get('code', '')
    # code가 없을때 None 대신 공백 문자열 넣어줌

    signer = TimestampSigner()
    try :
        decoded_user_email = signing.loads(code)
        email = signer.unsign(decoded_user_email, max_age=60*30)
    except (TypeError, SignatureExpired) :
        return render(request, 'registration/verify_failed.html')

    user = get_object_or_404(User, email=email, is_active=False)
    user.is_active = True
    user.save()
    return render(request, template_name='registration/verify_success.html', context={'user' : user})


class LoginView(FormView) :
    template_name = 'registration/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('cbv_todo_list')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)

        next_page = self.request.GET.get('next')
        if next_page:
            return HttpResponseRedirect(next_page)

        return HttpResponseRedirect(self.get_success_url())