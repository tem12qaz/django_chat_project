from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import LoginForm, RegForm
from django.db import connection
from .models import Chat, Message, Blocked_user
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

def is_blocked(request):
    try:
        b = Blocked_user.objects.get(User = request.user)
    except Exception as e:
        return False
    else:
        if b == None:
            return False
        else:
            logout(request)
            return True


def index(request, error = None):
    if not request.user.is_authenticated:

        if error == None:
            error = ''

        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                user = authenticate(username = request.POST['username'], password = request.POST['password'])
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect('/search/')
                else:
                    error += 'Неверное имя пользователя или пароль'
        form = LoginForm()
        data = {
            'form': form,
            'error': error
        }
        return render(request, 'chat.html', data)
    else:
        return (HttpResponseRedirect('/search/'))

@login_required
def logout_f(request):
    logout(request)
    return HttpResponseRedirect('/')

def register(request):
    if not request.user.is_authenticated:
        error1 = ''
        error2 = ''
        error3 = ''
        if request.method == 'POST':
            form = RegForm(request.POST)
            if form.is_valid():
                if len(request.POST['username']) <3:
                    error1 += 'Имя пользователя не должно быть короче 3 символов\n'

                if len(request.POST['password']) < 8:
                    error2 += 'Пароль не должен быть короче 8 символов\n'

                if request.POST['password'] != request.POST['password_c']:
                    error3 += 'Пароли не совпадают\n'

                if error1 == '' and error2 == '' and error3 == '':
                    try:
                        u = User.objects.get(username = request.POST['username'])
                    except ObjectDoesNotExist:
                        user = User.objects.create_user(username =request.POST['username'],password = request.POST['password'])
                        user.save()
                        data = {
                            'form': form,
                            'error': ''
                        }
                        return HttpResponseRedirect('/')
                    else:
                        error1 += 'Имя пользователя занято'

            else:
                pass
        else:
            form = RegForm()
        data = {
            'form': form,
            'error1': error1,
            'error2': error2,
            'error3': error3
        }
        return render(request, 'reg.html', data)
    else:
        return (HttpResponseRedirect('/search/'))

@login_required
def search(request):
    if is_blocked(request):
        err = 'Ваш аккаунт заблокирован'
        return(index(request, err))
    error = ''
    if request.method == 'POST':
        nik = request.POST['poisk']
        try:
            u = User.objects.get(username = nik)
        except ObjectDoesNotExist:
            error = 'Пользователь не найден'
        else:
            if u == request.user:
                error = 'Чат с собой недоступен'
            else:
                try:
                    u2 = request.user
                    chat = Chat.objects.get(user1 = u, user2 = u2)
                except ObjectDoesNotExist:
                    try:
                        chat = Chat.objects.get(user1 = u2, user2 = u)
                    except ObjectDoesNotExist:
                        chat = Chat(user1 = u, user2 = u2)
                        chat.save()

                return HttpResponseRedirect(f'/{chat.id}/')

    data = {
        'error': error
    }
    return render(request, 'poisk.html', data)

@login_required
def chat(request, chat_id):
    if is_blocked(request):
        err = 'Ваш аккаунт заблокирован'
        return(index(request, err))
    try:
        chat = Chat.objects.get(id = chat_id)

    except ObjectDoesNotExist:
        return (HttpResponseRedirect('/search/'))

    else:
        if request.method == 'POST':
            message = Message(
                chat = chat,
                user_from = request.user,
                text = request.POST['text']
            )
            message.save()
            return JsonResponse({}, status=200)

        if request.method == 'GET':
            if request.is_ajax():
                name = []
                time = []
                text = []
                message_list1 = chat.message.order_by('id')
                message_list =message_list1[int(request.GET['id']):]
                id = str(len(message_list1))
                if len(message_list) >0:
                    for message in message_list:
                        name.append(message.user_from)
                        time.append(message.date())
                        text.append(message.text)
                    return JsonResponse({'name':name, 'time':time, 'text':text, 'id':id}, status=200)
                return JsonResponse({'id':id}, status=200)

            message_list = chat.message.order_by('id')

            data = {
            'message_list': message_list,
            'last_message':(len(message_list))
            }
            return (render(request, 'message.html', data))
