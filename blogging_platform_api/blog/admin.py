from django.contrib import admin
from django.apps import apps

Category = apps.get_model('blog', 'Category')
Tag = apps.get_model('blog', 'Tag')
Post = apps.get_model('blog', 'Post')
Comment = apps.get_model('blog', 'Comment')
LikeAndRating = apps.get_model('blog', 'LikeAndRating')

admin.site.register([Category, Tag, Post, Comment, LikeAndRating])
