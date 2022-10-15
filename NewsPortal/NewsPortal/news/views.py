from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import render, redirect

from datetime import timedelta, timezone

from .filters import PostFilter
from .forms import PostForm, UserForm
from .models import *


def post_filter(request):
    f = PostFilter(request.GET, queryset=Post.objects.all())
    return render(request, 'post_filter.html', {'filter': f})


class NewsList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'news_list.html'
    context_object_name = 'news_list'
    ordering = ['-id']
    paginate_by = 8
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Post_all'] = Post.objects.all()
        context['form'] = PostForm()
        return context

    def news(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

        return super().get(request, *args, **kwargs)


class NewsDetails(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'news_detail'


class CategoriesList(ListView):
    model = Category
    template_name = 'categories_list.html'
    context_object_name = 'categories_list'


class PostListByCategories(ListView):
    model = Post
    template_name = 'categories_detail.html'
    context_object_name = 'categories_detail'

    def add_subscribe(request):
        user = request.user
        id = request.META.get('HTTP_REFERER')[-2]
        category = Category.objects.get(id=id)
        category.subscribers.add(user)
        return redirect(request.META.get('HTTP_REFERER'))

    def dell_subscribe(request):
        user = request.user
        id = request.META.get('HTTP_REFERER')[-2]
        category = Category.objects.get(id=id)
        category.subscribers.remove(user)
        return redirect(request.META.get('HTTP_REFERER'))

    def get_queryset(self):
        cat = self.request.resolver_match.kwargs['pk']
        return PostCategory.objects.filter(categoryThrough=cat)

    def get_context_data(self, **kwargs):
        id = self.kwargs.get('pk')
        context = super().get_context_data(**kwargs)
        cat = self.request.resolver_match.kwargs['pk']
        que = PostCategory.objects.filter(categoryThrough=cat)
        context['category_self'] = que[0].categoryThrough
        context['is_subscribers'] = UserCategory.objects.filter(subCategory=id, subUser=self.request.user).exists()
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    template_name = 'post_create.html'
    form_class = PostForm
    permission_required = ('News.add_post',)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    template_name = 'post_create.html'
    form_class = PostForm
    permission_required = ('News.change_post',)

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDelete(PermissionRequiredMixin, DeleteView):
    template_name = 'post_delete.html'
    context_object_name = 'post_delete'
    queryset = Post.objects.all()
    success_url = '/news/'
    permission_required = ('News.delete_post',)


class UserDetails(DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'user_detail'


class UserUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'user_update.html'
    context_object_name = 'user_update'
    form_class = UserForm
    success_url = '/news/'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return User.objects.get(pk=id)

