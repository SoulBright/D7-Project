from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from .resources import CATEGORY_CHOICES, ARTICLE


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.authorUser}"

    def update_rating(self):
        post_rat = self.post_set.aggregate(postRating=Sum('rating'))
        p_rat = 0
        p_rat += post_rat.get('postRating')

        comment_rat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        c_rat = 0
        c_rat += comment_rat.get('commentRating')

        self.ratingAuthor = p_rat * 3 + c_rat
        self.save()


class Post(models.Model):
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField('Category', through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return f'/news/{self.id}'

    def preview(self):
        return f'{self.text[0:128]}... rating:{str(self.rating)}'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=512)
    subscribers = models.ManyToManyField(User, through='UserCategory')

    def __str__(self):
        return f"{self.name}"


class UserCategory(models.Model):
    subUser = models.ForeignKey(User, on_delete=models.CASCADE)
    subCategory = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"Пользователь - {self.subUser} подписан на категорию: {self.subCategory}"


class PostCategory(models.Model):
    postThrough = models.ForeignKey('Post', on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return f'Пост: "{self.postThrough}" - Категория: "{self.categoryThrough}"'


class Comments(models.Model):
    commentPost = models.ForeignKey('Post', on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
