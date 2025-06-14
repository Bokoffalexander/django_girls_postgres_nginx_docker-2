from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm

def register(request):
    """Редактирует нового пользователя"""
    if request.method != 'POST':
        # Выводит пустую форму регистрации
        form = UserCreationForm()
    else:
        # Обработка заполненной формы
        # Отправляем данные POST 
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            # Выполнение входа и перенаправление на домашнюю страницу
            login(request, new_user)
            return redirect('django_girls_app:index')

    # Вывести пустую или недействительную форму
    context = {'form':form}
    return render(request, 'users/register.html', context)

def logout_view(request):
    logout(request)
    # Optionally, redirect to a success page
    return render(request, "registration/logged_out.html", {"Done":"Done!"})
