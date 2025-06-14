from django.shortcuts import render, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404

# Create your views here.
def index(request):
    """Домашняя страница приложения django_girls_app"""
    return render(request, 'django_girls_app/index.html')

@login_required
def topics(request):
    """Вывод списка тем"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics':topics}

    return render(request, 'django_girls_app/topics.html', context)

@login_required
def topic(request, topic_id):
    """Выводит одну тему и все ее записи"""
    topic = Topic.objects.get(id=topic_id)
    
    # Проверка того, что тема принадлежит текущему пользователю
    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic':topic, 'entries':entries}

    return render(request, 'django_girls_app/topic.html', context)

@login_required
def new_topic(request):
    """Определяет новую тему"""
    if request.method != 'POST':
        # Данные не отправлены, создается пустая форма
        form = TopicForm()
    else:
        # Отправляем данные POST, 
        # обработать данные
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('django_girls_app:topics')

    # Вывести пустую или недействительную форму
    context = {'form':form}
    return render(request, 'django_girls_app/new_topic.html', context)


    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic':topic, 'entries':entries}

    return render(request, 'django_girls_app/topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Добавляем новую запись по конкретной теме"""
    topic = Topic.objects.get(id=topic_id)

    # Проверка того, что тема принадлежит текущему пользователю
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Данные не отправлены, создается пустая форма
        form = EntryForm()
    else:
        # Отправляем данные POST, 
        # обработать данные
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('django_girls_app:topic', topic_id=topic_id)

    # Вывести пустую или недействительную форму
    context = {'topic':topic, 'form':form}
    return render(request, 'django_girls_app/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Редактирует существующую запись"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    # Проверка того, что тема принадлежит текущему пользователю
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Данные не отправлены
        # Исходный запрос, форма заполняется данными текущей записи
        form = EntryForm(instance=entry)
    else:
        # Отправляем данные POST, 
        # обработать данные
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('django_girls_app:topic', topic_id=topic.id)

    # Вывести пустую или недействительную форму
    context = {'entry':entry, 'topic':topic, 'form':form}
    return render(request, 'django_girls_app/edit_entry.html', context)

