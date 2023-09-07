from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.urls import reverse_lazy, resolve
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import EmailMultiAlternatives
from datetime import datetime
from django.utils import timezone


class PostList(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'newspaper/posts.html'  # указываем имя шаблона, 
    # в котором будет лежать HTML, в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'posts'  # это имя списка, в котором будут лежать все объекты,
    # его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    ordering = ['-data_post_creation']
    paginate_by = 2
    form_class = PostForm

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
        context['form'] = PostForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST) 
        if form.is_valid:
            form.save()
        return super().get(request, *args, **kwargs)


class PostDetailView(DetailView):
    model = Post
    template_name = 'newspaper/post.html'
    context_object_name = 'post'


class PostCreateView(CreateView):
    template_name = 'newspaper/post_create.html'
    permission_required = 'newspaper.add_post'
    form_class = PostForm


class PostUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'newspaper/post_create.html'
    permission_required = 'newspaper.change_post'
    form_class = PostForm

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте который мы
    # собираемся редактировать
    def get_object(self, **rwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления товара
class PostDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'newspaper/post_delete.html'
    permission_required = 'newspaper.delete_post'
    queryset = Post.objects.all()
    success_url = reverse_lazy('newspaper:posts')

