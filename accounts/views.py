from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.utils.encoding import force_str
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives

from .forms import UserCreationWithEmailForm, UserUpdateForm, PasswordChangeForm

User = get_user_model()

def register_view(request):
    if request.method == "POST":
        user_form = UserCreationWithEmailForm(request.POST)
        if user_form.is_valid():
            email = user_form.cleaned_data['email']
            # Verifique se o email já existe
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Este e-mail já está em uso. Por favor, use um e-mail diferente.')
                return render(request, 'register.html', {'user_form': user_form})

            user = user_form.save(commit=False)
            user.is_active = False  # O usuário não pode logar até confirmar o email
            user.save()

            # Gerar link de confirmação
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            confirmation_link = request.build_absolute_uri(
                reverse('confirm_email', kwargs={'uidb64': uid, 'token': token})
            )

            # Mensagem de email
            email_body = (
                f"Olá {user.username},\n\n"
                "Obrigado por se registrar em nosso sistema. Para ativar sua conta, "
                f"por favor, clique no link abaixo:\n\n{confirmation_link}\n\n"
                "Atenciosamente,\n"
                "Equipe Lobo Multimarcas ©"
            )

            # Enviar o e-mail
            send_mail(
                'Confirmação de Cadastro',
                email_body,
                'noreply@seusite.com',
                [user.email],
                fail_silently=False,
            )

            messages.success(request, 'Registro realizado com sucesso! Verifique seu e-mail para ativar sua conta.')
            return redirect('login')
    else:
        user_form = UserCreationWithEmailForm()

    return render(request, 'register.html', {'user_form': user_form})

def confirm_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Sua conta foi confirmada com sucesso! Você agora pode fazer login.')
            return redirect('login')
        else:
            messages.error(request, 'O link de confirmação é inválido.')
    except (TypeError, ValueError, OverflowError):
        messages.error(request, 'O link de confirmação é inválido.')
    except User.DoesNotExist:
        messages.error(request, 'Usuário não encontrado.')

    return redirect('login')

user = get_user_model()

class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return super().form_valid(form)

        # Gerar uid e token
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        confirmation_link = self.request.build_absolute_uri(
            reverse_lazy('password_reset_confirm', kwargs={
                'uidb64': uid,
                'token': token,
            })
        )

        email_body = (
            f"<p>Olá {user.get_username()},</p>"
            "<p>Agradecemos por utilizar nosso sistema. Recebemos uma solicitação para redefinir sua senha.</p>"
            f"<p>Para continuar, por favor, clique no link abaixo:</p>"
            f"<p><a href='{confirmation_link}'>Redefinir Senha</a></p>"
            "<p>Se você não solicitou esta alteração, ignore este email e sua senha permanecerá inalterada.</p>"
            "<p>Atenciosamente,<br>Equipe Lobo Multimarcas</p>"
        )

        email = EmailMultiAlternatives(
            subject='Redefinição de Senha',
            body='Este é o corpo do email em texto simples',
            from_email='noreply@seusite.com',
            to=[email],
        )
        email.attach_alternative(email_body, "text/html")
        email.send()

        return super().form_valid(form)

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

    def get_form_class(self):
        return SetPasswordForm

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'

    def get_success_url(self):
        return reverse_lazy('login')
    
def check_email_exists(request):
    email = request.GET.get('email', None)
    data = {
        'is_taken': User.objects.filter(email__iexact=email).exists()
    }
    return JsonResponse(data)


def login_view(request):
    if request.method == "POST":
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('cars_list')
    else:
        login_form = AuthenticationForm()
    
    return render(request, 'login.html', {'login_form': login_form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def update_profile_view(request):
    user_form = UserUpdateForm(instance=request.user)
    password_form = PasswordChangeForm(user=request.user)

    if request.method == 'POST':
        if 'user_form_submit' in request.POST:
            user_form = UserUpdateForm(request.POST, instance=request.user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Perfil atualizado com sucesso!')
                return redirect('update_profile')  # Redirecione para a URL desejada

        elif 'password_form_submit' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Mantenha a sessão do usuário
                messages.success(request, 'Senha alterada com sucesso!')
                return redirect('update_profile')  # Redirecione para a URL desejada
            else:
                # Mensagens de erro específicas do formulário
                for error in password_form.errors.values():
                    for err in error:
                        messages.error(request, err)

    return render(request, 'update_profile.html', {
        'user_form': user_form,
        'password_form': password_form
    })