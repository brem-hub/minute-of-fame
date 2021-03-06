"""импортируем все необходимые модули """
import random
import string

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.conf import settings
from django.views.decorators.cache import cache_control
import requests

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import RegisterFormView, LoginForm, ReportForm, ChangePhotoForm
from .models import *


def stream_test(request, num):
    """создание стрима"""
    item = PollStat(poll_result=0, likes=0, dislikes=0)
    item.save()
    return render(request, 'page{}.html'.format(num))


def screen_share(request):
    """общий доступ к экрану"""
    return render(request, 'screen_share_test.html')


def get_menu_context():
    """меню"""
    return [
        {'url': '/', 'name': 'Home'},
        # {'url': '/categories', 'name': 'Categories'},
        {'url': '/top/', 'name': 'Top'},
        {'url': '/about/', 'name': 'About'},
    ]


def partition(arr, low, high):
    i = (low - 1)  # index of smaller element
    pivot = arr[high][0]  # pivot

    for j in range(low, high):

        # If current element is smaller than or
        # equal to pivot
        if arr[j][0] > pivot:
            # increment index of smaller element
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


# The main function that implements QuickSort
# arr[] --> Array to be sorted,
# low  --> Starting index,
# high  --> Ending index

# Function to do Quick sort
def quickSort(arr, low, high):
    if low < high:
        # pi is partitioning index, arr[p] is now
        # at right place
        pi = partition(arr, low, high)

        # Separately sort elements before
        # partition and after partition
        quickSort(arr, low, pi - 1)
        quickSort(arr, pi + 1, high)


def top_page(req):
    users = []
    all_users = [[0, i] for i in User.objects.all()]
    for user in all_users:
        streams = Stream.objects.filter(publisher=user[1])
        for stream in streams:
            user[0] += stream.views
    quickSort(all_users, 0, len(all_users) - 1)
    if len(all_users) < 10:
        for i in range(len(all_users)):
            likes_count = 0
            dislikes_count = 0
            streams = Stream.objects.filter(publisher=all_users[i][1])
            for j in streams:
                for k in PollStat.objects.filter(stream=j):
                    if k.vote == 1:
                        likes_count += 1
                    else:
                        dislikes_count += 1
            users.append([i + 1, all_users[i][1].username, likes_count, dislikes_count, all_users[i][0]])
    elif len(all_users) < 40:
        for i in range(10):
            likes_count = 0
            dislikes_count = 0
            streams = Stream.objects.filter(publisher=all_users[i][1])
            for j in streams:
                for k in PollStat.objects.filter(stream=j):
                    if k.vote == 1:
                        likes_count += 1
                    else:
                        dislikes_count += 1
            users.append([i + 1, all_users[i][1].username, likes_count, dislikes_count, all_users[i][0]])
    else:
        for i in range(40):
            likes_count = 0
            dislikes_count = 0
            streams = Stream.objects.filter(publisher=all_users[i][1])
            for j in streams:
                for k in PollStat.objects.filter(stream=j):
                    if k.vote == 1:
                        likes_count += 1
                    else:
                        dislikes_count += 1
            users.append([i + 1, all_users[i][1].username, likes_count, dislikes_count, all_users[i][0]])
    # Формат передачи ин-фы о пользователе:
    # [*Номер в топе*, *Ник*, *Общее кол-во лайков*, *Общее кол-во дизлайков*, *Общее кол-во просмотров*]

    context = {"pagename": "Топ пользователей", 'menu': get_menu_context(),
               "userbase": users
               }
    return render(req, 'pages/top.html', context)


def stream_page(request):
    """страница стрима"""
    context = {'pagename': 'Главная', 'menu': get_menu_context(),
               'test': 1,
               # 'Regform': RegisterFormView(),
               # 'Logform': LoginForm(),
               'stream_id': ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16)),
               'emotes_list': [['Ricardo', '.png'], ['AbsoluteLegend', '.png'], ['ThumbUp', '.png'],
                               ['SmugDance', '.gif'], ['Doge', '.png'], ['DogeDS', '.gif'], ['LatchBall', '.gif'],
                               ['Cry', '.png'], ['HamsterCam', '.png'], ['JudgeLook', '.png']]
               }
    return render(request, 'pages/stream.html', context)


def login_page(request):
    """вход пользователя в кабинет  """
    context = {'pagename': 'Вход',
               'menu': get_menu_context()}
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.data['username']
            password = login_form.data['password']
            if User.objects.filter(email=login_form.data['username']).exists():
                user = User.objects.get(email=login_form.data['username'])
                username = str(user.username)

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.add_message(
                    request, messages.SUCCESS, "Авторизация успешна")
                return redirect('index')
            else:
                messages.add_message(
                    request, messages.ERROR,
                    "Неправильный логин или пароль")
        else:
            messages.add_message(
                request, messages.ERROR,
                "Некорректные данные в форме авторизации")
    else:
        login_form = LoginForm()
        context['form'] = login_form
    return render(request, 'pages/stream.html', context)


def logout_page(request):
    """функция для выхода пользователя"""
    logout(request)
    messages.add_message(request, messages.INFO,
                         "Вы успешно вышли из аккаунта")
    return redirect('index')


def get_client_ip(request):
    """получение ip пользователей """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def register_page(request):
    """страница регистрации"""
    context = dict()
    context['menu'] = get_menu_context()
    context['site_key'] = settings.RECAPTCHA_SITE_KEY
    if request.method == 'POST':
        form = RegisterFormView(request.POST)
        context['form'] = form
        if form.is_valid():
            if form.unique_email():
                form.save()
                if not settings.DEBUG:
                    # captcha verification
                    secret_key = settings.RECAPTCHA_SECRET_KEY
                    data = {
                        'response': request.POST.get('g-recaptcha-response'),
                        'secret': secret_key,
                        'remoteip': get_client_ip(request)
                    }
                    resp = requests.post(
                        'https://www.google.com/recaptcha/api/siteverify', data=data)
                    result_json = resp.json()
                    success = result_json.get('success')
                else:
                    success = True

                if not success:
                    return render(request, 'pages/stream.html', {'is_robot': True})

                new_user = form.save()
                username = form.cleaned_data.get('username')
                my_password = form.cleaned_data.get('password1')
                _user = authenticate(username=username, password=my_password)

                if _user.is_active:
                    login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
                    messages.add_message(
                        request, messages.SUCCESS,
                        'Вы успешно зарегистрировались')
                    new_variable = Profile()
                    new_variable.name = request.user
                    new_variable.user = request.user
                    new_variable.save()
                    return redirect('index')
            else:
                messages.add_message(
                    request, messages.ERROR,
                    'Аккаунт с этой почтой уже существует')
        else:
            messages.add_message(request, messages.ERROR,
                                 'Вы ввели неверные данные')
        # return render(request, 'registration/register.html', context)
    else:
        form = RegisterFormView()
        context['form'] = form
    return redirect('index')


@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
def profile_page(req, id):
    """страница пользователа и все что на ней есть """
    context = {
        'menu': get_menu_context()
    }
    real_name = User.objects.filter(username=id)
    if len(real_name) > 0:
        id = real_name[0].id
        if len(Profile.objects.filter(user=id)) > 0:
            item = Profile.objects.filter(user_id=id)[len(Profile.objects.filter(user_id=id)) - 1]
            context['item'] = item
            context['likes_count'] = 0
            context['dislikes_count'] = 0
            context['views'] = 0
            streams = Stream.objects.filter(publisher=real_name[0])
            for stream in streams:
                context['views'] += stream.views
                for i in PollStat.objects.filter(stream=stream):
                    if i.vote == 1:
                        context['likes_count'] += 1
                    else:
                        context['dislikes_count'] += 1
        else:
            item = Profile(quotes='No description', name=real_name[0].username)
    else:
        return render(req, 'pages/no_profile.html', context)

    context['item'] = item

    return render(req, 'pages/profile.html', context)


@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
def profile_settings_page(req):
    """редактирование страницы пользователя"""
    context = {
        'menu': get_menu_context()
    }
    if req.user.is_authenticated:
        if len(Profile.objects.filter(user=req.user)) == 0:
            new_profile = Profile()
            new_profile = Profile(user=req.user, name=req.user.username)
            new_profile.save()

        num_of_profiles = len(Profile.objects.filter(user=req.user))
        current_profile = Profile()

        if num_of_profiles >= 1:
            current_profile = Profile.objects.filter(user=req.user)[num_of_profiles - 1]

        context['item'] = current_profile

        if req.method == 'POST':
            fields_names = ['quotes', 'location',
                            'email', 'Vk', 'instagram',
                            'facebook', 'twitter', 'odnoklassniki',
                            'youtube_play', 'name']
            fields_content = dict()

            for field in fields_names:
                fields_content[field] = str(req.POST.get(field))

            new_item = Profile(user=req.user, quotes=fields_content['quotes'],
                               email=fields_content['email'],
                               location=fields_content['location'],
                               Vk=fields_content['Vk'],
                               instagram=fields_content['instagram'],
                               facebook=fields_content['facebook'],
                               twitter=fields_content['twitter'],
                               odnoklassniki=fields_content['odnoklassniki'],
                               youtube_play=fields_content['youtube_play'],
                               name=fields_content['name'])
            new_item.save()
    else:
        return redirect('index')
    return render(req, 'pages/profile_settings.html', context)


def change_name(req):
    """Модал смены имени"""
    context = {
        'menu': get_menu_context()
    }
    if req.user.is_authenticated:
        if req.method == 'POST':
            new_name = req.POST.get('new_name')
            print(req.POST)
            for k in req.POST:
                print(k)
            num_of_profiles = len(Profile.objects.filter(user=req.user))
            current_profile = Profile()

            if num_of_profiles >= 1:
                current_profile = Profile.objects.filter(user=req.user)[num_of_profiles - 1]
            new_profile = Profile(user=req.user, quotes=current_profile.quotes,
                                  email=current_profile.email,
                                  location=current_profile.location,
                                  Vk=current_profile.Vk,
                                  instagram=current_profile.instagram,
                                  facebook=current_profile.facebook,
                                  twitter=current_profile.twitter,
                                  odnoklassniki=current_profile.odnoklassniki,
                                  youtube_play=current_profile.youtube_play,
                                  name=new_name)
            new_profile.save()
    return redirect('/profile_' + req.user.username)


def about_page(req):
    """страница описывающяя сайт """
    context = {
        'menu': get_menu_context()
    }

    return render(req, 'pages/about.html', context)


@login_required()
def report_page(request, badass_id):
    """страница отчета"""
    context = {
        'menu': get_menu_context(),
        'Form': ReportForm(initial={'badass': badass_id, 'sender': request.user.id}),
    }
    if request.method == 'GET':
        return render(request, 'pages/report.html', context)
    if request.method == 'POST':
        report = ReportForm(request.POST)
        if report.is_valid():
            report.cleaned_data['sender'] = request.user.id
            report.save()
            messages.add_message(request, messages.SUCCESS,
                                 'report was sent to moders team of (=^･ｪ･^=)')
            return render(request, 'pages/stream.html', context)
        else:
            messages.add_message(request, messages.ERROR, 'Form is not valid')
            return render(request, 'pages/report.html', context)


def get_data_for_charts(request, id):
    real_name = User.objects.filter(username=id)
    likes = []
    labels = []
    dislikes = []
    if len(real_name) > 0:
        id = real_name[0].id
        if len(Profile.objects.filter(user=id)) > 0:
            streams_temp = list()
            for i in Stream.objects.filter(publisher=real_name[0]):
                streams_temp.append(i)
            streams = streams_temp
            likes = []
            dislikes = []
            for i in streams:
                labels.append(i.title)
                pollstats = PollStat.objects.filter(stream=i)
                likes_count = 0
                dislikes_count = 0
                for j in pollstats:
                    if j.vote == 1:
                        likes_count += 1
                    else:
                        dislikes_count += 1
                likes.append(likes_count)
                dislikes.append(dislikes_count)
    data = {
        'labels': labels,
        'likes': likes,
        'dislikes': dislikes
    }
    return JsonResponse(data)
