from django_filters import FilterSet
from .models import Post


# создаём фильтр
class PostFilter(FilterSet):
    class Meta:
         model = Post
         fields = {
             'dateCreation': ['gt'],
             'author': ['exact'],
         }



