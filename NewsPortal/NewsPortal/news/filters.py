from django_filters import FilterSet, DateFilter
import django.forms
from .models import Post


class PostFilter(FilterSet):
    dateCreation = DateFilter(lookup_expr='lte', widget=django.forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'author__authorUser': ['exact'],
            'categoryType': ['exact'],
            'postCategory__name': ['icontains'],
        }