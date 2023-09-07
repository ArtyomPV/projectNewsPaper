from django.urls import path
from .views import PostList, PostDetailView, PostCreateView, PostDeleteView, PostUpdateView # импортируем представление

app_name = 'newspaper'

urlpatterns = [
    path('', PostList.as_view(), name='posts'),
    # т.к. сам по себе это класс, то нам надо представить этот класс в виде view. Для этого вызываем метод as_view
    path('<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('update/<int:pk>/', PostUpdateView.as_view(), name='post_update'),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name='post_delete'),
]