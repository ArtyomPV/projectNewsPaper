from django_filters import FilterSet
from .models import Post


class PostFilter(FilterSet):
    class Meta:
        model = Post
        # fields = ('data_post_creation', 'title','author')
        fields = {
            'data_post_creation': ['gt'],
            'title': ['icontains'],
            'author': ['exact'],
            'category':['exact'],
        }
