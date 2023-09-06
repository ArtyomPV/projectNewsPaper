from django.urls import path
from .views import PostList, PostDetailView # импортируем представление

appname = 'newspaper'

urlpatterns = [
    path('', PostList.as_view()),
    # т.к. сам по себе это класс, то нам надо представить этот класс в виде view. Для этого вызываем метод as_view
    path('<int:pk>', PostDetailView.as_view()),
]