from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Tovar, Category
from .filters import ProductFilter
from .forms import PostForm
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category

from django.contrib.auth.mixins import PermissionRequiredMixin

import logging
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied

# Получаем разные логгеры
logger = logging.getLogger('django')
logger_request = logging.getLogger('django.request')
logger_security = logging.getLogger('django.security')
logger_db = logging.getLogger('django.db.backends')


def test_logging(request):
    # 1. Проверка Консоли (DEBUG=True) и General.log (DEBUG=False)
    logger.debug("Тест DEBUG: виден в консоли")
    logger.info("Тест INFO: виден в консоли и general.log")
    logger.warning("Тест WARNING: + путь к файлу")

    # 2. Проверка Errors.log и Почты
    try:
        raise ValueError("Тестовая ошибка")
    except ValueError as e:
        # Должно попасть в errors.log (со стеком) и на почту (без стека)
        logger_request.error("Ошибка запроса!", exc_info=True)

    # 3. Проверка Security.log
    logger_security.info("Событие безопасности: вход выполнен")

    # 4. Проверка фильтрации уровней (SQL ошибка)
    logger_db.error("Ошибка базы данных!")

    return HttpResponse("Логи сгенерированы. Проверьте консоль и файлы.")

# Create your views here.
def index(request):
    all_news = Tovar.objects.order_by('-data')[:3]
    context={
        'main_post': all_news[0] if all_news else None,
        'side_news': all_news[1:3]
    }
    return render(request, 'index.html', context)

class ProductsList(ListView):
    model=Tovar
    template_name = 'news.html'
    context_object_name = 'post'
    paginate_by = 10



class TovarDetailView(DetailView):
    model = Tovar
    template_name = 'news_detail.html'
    context_object_name = 'article'


class Searh(ListView):
    model = Tovar
    template_name = 'news_search.html'
    context_object_name = 'news'

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ProductFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsCreate(PermissionRequiredMixin, CreateView):
    model = Tovar
    form_class = PostForm
    template_name = 'edit.html'
    success_url = '/news/'
    #fields = '__all__'
    permission_required = ('news.add_tovar',)

    def form_valid(self, form):
        post = form.save(commit = False)
        category_obj, created = Category.objects.get_or_create(name='Новости')

        post.category = category_obj  # Присваиваем объект, а не строку
        return super().form_valid(form)

class NewsUpdate(PermissionRequiredMixin, UpdateView):
    model = Tovar
    form_class = PostForm
    template_name = 'edit.html'
    success_url = '/news/'
    #fields = '__all__'
    permission_required = ('news.add_tovar',)


class NewsDelete(PermissionRequiredMixin, DeleteView):
    model = Tovar
    template_name = 'delete.html'
    success_url = '/news/'
    #fields = '__all__'
    permission_required = ('news.add_tovar',)

#-----------------

class ArticleCreate(PermissionRequiredMixin, CreateView):
    model=Tovar
    form_class = PostForm
    template_name = 'edit.html'
    success_url = '/news/'
    #fields = '__all__'
    permission_required = ('news.add_tovar',)


    def form_valid(self, form):
        post = form.save(commit= False)
        category_obj, created = Category.objects.get_or_create(name='Статьи')

        post.category = category_obj
        return super().form_valid(form)

class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    model = Tovar
    form_class = PostForm
    template_name = 'edit.html'
    success_url = '/news/'
    #fields = '__all__'
    permission_required = ('news.add_tovar',)

class ArticleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.add_tovar',)
    model = Tovar
    template_name = 'delete.html'
    success_url = '/news/'
    #fields = '__all__'

@login_required
def subscribe(request, pk):
    category = get_object_or_404(Category, id=pk)
    category.subscribers.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', '/')) # Возвращает туда, где был пользователь

@login_required
def unsubscribe(request, pk):
    category = get_object_or_404(Category, id=pk)
    category.subscribers.remove(request.user)
    return redirect(request.META.get('HTTP_REFERER', '/'))