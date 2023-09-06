from datetime import date
from django.utils import timezone
from django.shortcuts import render
from django.core.paginator import Paginator
# Create your views here.
from django.views.generic import ListView, DetailView
from .models import Post
from .filters import PostFilter 


class PostList(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'newspaper/posts.html'  # указываем имя шаблона, 
    # в котором будет лежать HTML, в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'posts'  # это имя списка, в котором будут лежать все объекты,
    # его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    ordering = ['-data_post_creation']
    paginate_by = 2

       # метод get_context_data нужен нам для того, 
       # чтобы мы могли передать переменные в шаблон. 
       # В возвращаемом словаре context будут храниться 
       # все переменные. Ключи этого словари и есть 
       # переменные, к которым мы сможем потом обратиться 
       # через шаблон
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # добавим переменную текущей даты time_now
        context['time_now'] = timezone.localtime(timezone.now())
        # добавим ещё одну пустую переменную, чтобы на её примере посмотреть работу другого фильтра
        context['value'] = None
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'newspaper/post.html'
    context_object_name = 'post'

