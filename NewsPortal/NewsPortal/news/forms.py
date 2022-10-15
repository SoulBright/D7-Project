from django.forms import ModelForm, BooleanField
from .models import Post, User


class PostForm(ModelForm):
    check_box = BooleanField(label='Подтвердить')
    postCategory = Post.postCategory.through

    class Meta:
        model = Post
        fields = ['author', 'categoryType', 'title', 'text', 'postCategory', 'check_box']


class UserForm(ModelForm):
    check_box = BooleanField(label='Подтвердить')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'check_box']
