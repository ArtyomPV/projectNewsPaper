from django.contrib.auth.decorators import login_required
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy, resolve
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Author, Post, Category
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import EmailMultiAlternatives
from datetime import datetime
from django.utils import timezone

from django.db.models.signals import post_save
from django.core.mail import mail_managers
from django.core.cache import cache


def send_message(username, email, title, text):
    html_content = render_to_string(
        'email/new_post.html',
        {
            'username': username,
            'title':title,
            'text': text
        }
    )
    msg = EmailMultiAlternatives(
        subject=title,
        body=text,
        from_email='artyom.pv@yandex.ru',
        to=[email]
    )
    msg.attach_alternative(html_content,'text/html')
    msg.send()

def notify_managers_appointment(sender, instance, created, **kwargs):
    # # в зависимости от того, есть ли такой объект уже в базе данных или нет, тема письма будет разная
    # if created:
    #     subject = f'{instance.author} {instance.title}'
    # else:
    #     subject = f'Post changed for {instance.author} {instance.title}'
    
    title=f'Новый пост: {instance.title}' if created else f'Пост {instance.title} был изменен'
    text = instance.text[:50]
    subscribers_data=dict()
    for category in instance.category:
        subscribers = category.subscribers.all()
        for user in subscribers:
            if user.username not in subscribers_data:
                subscribers_data[user.username] = user.email
    for username, email in subscribers_data.items():
        send_message(username, email, title, text)
    
    # text = instance.text[0:123] + '...'
    # mail_managers(
    #     subject=subject,
    #     message=text,
    # )



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

    def get_object(self, *args, **kwargs): # переопределяем метод получения объекта, как ни странно
        obj = cache.get(f'post-{self.kwargs["pk"]}', None) # кэш очень похож на словарь, и метод get действует также. Он забирает значение по ключу, если его нет, то забирает None.
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj

class PostCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'newspaper/post_create.html'
    permission_required = 'newspaper.add_post'
    form_class = PostForm




class PostUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = 'newspaper/post_create.html'
    permission_required = 'newspaper.change_post'
    form_class = PostForm

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте который мы
    # собираемся редактировать
    def get_object(self, **rwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления товара
class PostDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    template_name = 'newspaper/post_delete.html'
    permission_required = 'newspaper.delete_post'
    queryset = Post.objects.all()
    success_url = reverse_lazy('newspaper:posts')

class CategoryListView(ListView):
    model = Post
    template_name = 'newspaper/category.html'
    context_object_name = 'posts'
    ordering = ['-data_post_creation']
    paginate_by = 3

    def get_queryset(self):
        self.id = resolve(self.request.path_info).kwargs['pk']
        # print(resolve(self.request.path_info))
        c = Category.objects.get(id=self.id)
        queryset = Post.objects.filter(category=c)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # print(user.email)
        category = Category.objects.get(id=self.id)
        subscribed = category.subscribers.filter(email=user.email)
        is_subscribed = False
        context['category'] = category
        context['is_subscribed'] = False
        if not subscribed:
            is_subscribed = True
        context['is_subscribed'] = is_subscribed
        return context


def subscribe_to_category(request, pk):
    user = request.user
    print('======user=========')
    print(user)
    category = Category.objects.get(id=pk)
    print(category.subscribers)
    if not category.subscribers.filter(id=user.id).exists():
        category.subscribers.add(user)
        print(category.subscribers)
        email = user.email
        html_content = render_to_string(
            'newspaper/subscribed.html',
            {
                'category': category,
                'user': user
            }
        )
        msg = EmailMultiAlternatives(
            subject=f'{category} subscription',
            body='',
            from_email='artyom.pv@yandex.ru',
            to=[email, ],
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
    return redirect('newspaper:posts')


@login_required
def unsubscribe_from_category(request, pk):
    user = request.user

    category = Category.objects.get(id=pk)

    if category.subscribers.filter(id=user.id).exists():

        category.subscribers.remove(user)
    return redirect('newspaper:posts')
